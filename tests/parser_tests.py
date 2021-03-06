import unittest

from search_address_parser.core.data_store import DataStore
from search_address_parser.core.definition import Definition, MatchPosition
from search_address_parser.core.parser import Parser
from search_address_parser.core.parsing_entity import ParsingEntity


class TestEntity(ParsingEntity):
    name = "Test entity"
    definitions = [
       # Definition(value="hello", match_pos=MatchPosition.RIGHT, abbreviations=[])
    ]


class TestParser(Parser):
    entity = None


class StoreParser(Parser):
    store =  DataStore(data={"1": "Орёл"})


class CoreParserTests(unittest.TestCase):
    def setUp(self):
        self.entity = TestEntity()
        self.parser = TestParser()

    def test_simple_parse_with_match_position_right(self):
        self.entity.definitions = [
            Definition(value="hello", match_pos=MatchPosition.RIGHT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("hello world")
        self.assertEqual("hello world", result[0].value)

    def test_simple_parse_with_match_position_left(self):
        self.entity.definitions = [
            Definition(value="hello", match_pos=MatchPosition.LEFT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("world hello")
        self.assertEqual("world hello", result[0].value)

    def test_parse_multiple_words_from_side_of_definition(self):
        expected_result = "hello beautiful world"
        self.entity.definitions = [
            Definition(value="hello", match_pos=MatchPosition.RIGHT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("hello beautiful world")
        self.assertEqual(expected_result, result[0].value)

    def test_parse_with_similar_definitions(self):
        self.entity.definitions = [
            Definition(value="посёлок", match_pos=MatchPosition.RIGHT, abbreviations=[]),
            Definition(value="посёлок городского типа", match_pos=MatchPosition.RIGHT, abbreviations=[], include_definition_part=False),
            Definition(value="посёлок городского", match_pos=MatchPosition.RIGHT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("посёлок городского типа Тихий дом")
        self.assertEqual(result[0].value, "Тихий дом")

    def test_parse_with_definitions_span_conflict(self):
        self.entity.definitions = [
            Definition(value="село", match_pos=MatchPosition.RIGHT, abbreviations=[]),
            Definition(value="вал", match_pos=MatchPosition.LEFT, abbreviations=[]),
        ]
        self.parser.entity = self.entity
        result1, result2 = self.parser.parse("село НазваниеСела 123 тест НазваниеВала вал")

        self.assertEqual(result1.value, "НазваниеСела")
        self.assertEqual(result2.value, "НазваниеВала")

    def test_with_store(self):
        #todo
        parser = StoreParser()
        parser.entity = self.entity
        result = parser.parse("Орёл")
        self.assertEqual(parser.parse("Орёл").value, "Орёл")