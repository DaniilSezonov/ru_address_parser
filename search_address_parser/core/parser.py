from typing import List

from search_address_parser.core.data_store import DataStore
from search_address_parser.core.parser_result import ParserResult, AssumeResult
from search_address_parser.core.parsing_entity import ParsingEntity


class Parser:
    entity: ParsingEntity = None
    store: DataStore = None

    def parse(self, value: str) -> ParserResult or List[ParserResult]:
        result = None
        if not self.is_empty_store():
            result = self.find_in_store(value)
        if not result:
            assume_result = AssumeResult(entity=self.entity)
            for definition in self.entity.definitions:
                suitable_definitions = definition.assume(value)
                if suitable_definitions:
                    for suitable_definition in suitable_definitions:
                        assume_result.add(suitable_definition)
            result = assume_result.to_parser_result()
        return result

    def find_in_store(self, value: str) -> ParserResult or None:
        if self.is_empty_store():
            return None
        #todo
        for val in self.store.data.values():
            if value == val:
                return ParserResult(result=val, entity_name=self.entity.name, definition_name="")
        return None

    def is_empty_store(self):
        return self.store and len(self.store.data) == 0

