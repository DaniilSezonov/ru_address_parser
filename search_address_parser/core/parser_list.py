from typing import List

from search_address_parser.core.parser import Parser
from search_address_parser.core.parser_result import ParserResult, EmptyResult


class MultipleParserResult:
    value: dict = {}
    fields: [] = []

    def __init__(self, parsers: []):
        self.fields = [parser.entity.name for parser in parsers]
        for field_name in self.fields:
            self.value.setdefault(field_name, EmptyResult())

    def add(self, result: ParserResult or List[ParserResult]):
        if isinstance(result, list):
            for res in result:
                self.value[res.entity_name] = res.value
        else:
            self.value[result.entity_name] = result.value


class ParserList:
    parsers: [Parser] = []
    result: MultipleParserResult = None

    def parse(self, value: str) -> MultipleParserResult:
        self.result = MultipleParserResult(self.parsers)
        for parser in self.parsers:
            self.result.add(parser.parse(value))
        return self.result
