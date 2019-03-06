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
        matches = [parser_res.match for parser_res in result.parsed_data]
        self.assertIn("world", matches)
        self.assertEqual(result.entity_name, self.entity.name)

    def test_simple_parse_with_match_position_left(self):
        self.entity.definitions = [
            Definition(value="hello", match_pos=MatchPosition.LEFT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("world hello")
        matches = [parser_res.match for parser_res in result.parsed_data]
        self.assertIn("world", matches)
        self.assertEqual(result.entity_name, self.entity.name)

    def test_parse_multiple_words_from_side_of_definition(self):
        expected_result = "beautiful world"
        self.entity.definitions = [
            Definition(value="hello", match_pos=MatchPosition.RIGHT, abbreviations=[])
        ]
        self.parser.entity = self.entity
        result = self.parser.parse("hello beautiful world")
        matches = [parser_res.match for parser_res in result.parsed_data]
        self.assertIn(expected_result, matches)
        self.assertEqual(result.entity_name, self.entity.name)
