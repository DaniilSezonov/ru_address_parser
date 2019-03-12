from typing import List

from search_address_parser.core.parser_result import ParserResult, AssumeResult
from search_address_parser.core.parsing_entity import ParsingEntity


class Parser:
    entity: ParsingEntity = None

    def parse(self, value: str) -> ParserResult or List[ParserResult]:
        assume_result = AssumeResult(entity=self.entity)
        for definition in self.entity.definitions:
            suitable_definitions = definition.assume(value)
            if suitable_definitions:
                for suitable_definition in suitable_definitions:
                    assume_result.add(suitable_definition)
        return assume_result.to_parser_result()






