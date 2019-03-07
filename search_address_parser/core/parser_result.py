from typing import List

from search_address_parser.core.definition import SuitableDefinition


class ParserResult:
    _suitable_definitions: List[SuitableDefinition]
    _entity_name: str = ""

    def __init__(self):
        self._suitable_definitions = []

    @property
    def suitable_definitions(self):
        return self._suitable_definitions

    def add(self, assume_def: SuitableDefinition):
        self.merge_similar_definition(assume_def)

    def merge_similar_definition(self, assume_def: SuitableDefinition):
        if not self.suitable_definitions:
            self.suitable_definitions.append(assume_def)
        else:
            excepted_definitions = []
            included_definitions = []
            for suitable_definition in self.suitable_definitions:
                if suitable_definition.is_similar_on(assume_def):
                    break
                elif assume_def.is_similar_on(suitable_definition):
                    excepted_definitions.append(suitable_definition)
                    included_definitions.append(assume_def)
                else:
                    included_definitions.append(assume_def)
            for excepted in excepted_definitions:
                self.suitable_definitions.remove(excepted)
            self.suitable_definitions.extend(included_definitions)

    def merge_span_conflict(self):
        pass

    @property
    def entity_name(self):
        return self._entity_name

    def __repr__(self):
        return f"{self._suitable_definitions}"
