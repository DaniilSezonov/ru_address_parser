import unittest

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
        matches = [parser_res.suitable_value for parser_res in result._suitable_definitions]
        self.assertIn("world", matches)

    def test_simple_parse_with_match_position_left(self):
        self.entity.definitions = [
            Definition(value="hello", match_pos=MatchPosition.LEFT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("world hello")
        matches = [parser_res.suitable_value for parser_res in result._suitable_definitions]
        self.assertIn("world", matches)

    def test_parse_multiple_words_from_side_of_definition(self):
        expected_result = "beautiful world"
        self.entity.definitions = [
            Definition(value="hello", match_pos=MatchPosition.RIGHT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("hello beautiful world")
        matches = [parser_res.suitable_value for parser_res in result._suitable_definitions]
        self.assertIn(expected_result, matches)

    def test_parse_with_similar_definitions(self):
        self.entity.definitions = [
            Definition(value="посёлок", match_pos=MatchPosition.RIGHT, abbreviations=[]),
            Definition(value="посёлок городского типа", match_pos=MatchPosition.RIGHT, abbreviations=[]),
            Definition(value="посёлок городского", match_pos=MatchPosition.RIGHT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("посёлок городского типа Тихий дом")
        self.assertEqual(len(result.suitable_definitions), 1)
        self.assertEqual(result.suitable_definitions[0].suitable_value, "Тихий дом")

    def test_parse_with_definition_conflicts(self):
        self.entity.definitions = [
            Definition(value="село", match_pos=MatchPosition.RIGHT, abbreviations=[]),
            Definition(value="вал", match_pos=MatchPosition.LEFT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("село НазваниеСела НазваниеВала вал")
        matches = [parser_res.suitable_value for parser_res in result._suitable_definitions]
       # self.assertTrue(len(matches) == 2)
        self.assertEqual(matches[0], "НазваниеСела НазваниеВала")
        self.assertEqual(matches[1], "НазваниеСела НазваниеВала")
