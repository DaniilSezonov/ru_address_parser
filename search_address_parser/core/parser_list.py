from search_address_parser.core.parser import Parser, ParserResult


class MultipleParserResult:
    value: dict = {}
    fields: [] = []

    def __init__(self, parsers: []):
        self.fields = [parser.entity.name for parser in parsers]
        for field_name in self.fields:
            self.value.setdefault(field_name, ParserResult())

    def add(self, result: ParserResult):
        self.value[result.entity_name] = result.parsed_data


class ParserList:
    parsers: [Parser] = []

    def parse(self, value: str) -> MultipleParserResult:
        result = MultipleParserResult(self.parsers)
        result.not_parsed_data = value
        for parser in self.parsers:
            result.add(parser.parse(result.not_parsed_data))
        return result
