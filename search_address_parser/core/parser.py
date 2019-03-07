from search_address_parser.core.parser_result import ParserResult
from search_address_parser.core.parsing_entity import ParsingEntity


class Parser:
    entity: ParsingEntity = None
    parser_result: ParserResult

    def parse(self, value: str) -> ParserResult:
        self.parser_result = ParserResult()
        for definition in self.entity.definitions:
            assume_results = definition.assume(value)
            if assume_results:
                for assume_result in assume_results:
                    self.parser_result.add(assume_result)
        return self.parser_result










