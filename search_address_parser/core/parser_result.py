from typing import List

from search_address_parser.core.definition import SuitableDefinition
from search_address_parser.core.parsing_entity import ParsingEntity


class AssumeResult:
    _suitable_definitions: List[SuitableDefinition]
    _entity: ParsingEntity

    def __init__(self, entity: ParsingEntity):
        self._suitable_definitions = []
        self._entity = entity

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
        raise NotImplementedError()

    @property
    def entity_name(self):
        return self._entity.name

    def __repr__(self):
        return f"{self._suitable_definitions}"

    def to_parser_result(self):
        if not self.suitable_definitions:
            return EmptyResult()
        elif len(self.suitable_definitions) == 1:
            return ParserResult(
                result=self.suitable_definitions[0].suitable_value.strip(),
                entity_name=self.entity_name,
                definition_name=self.suitable_definitions[0].definition_value
            )
        else:
            return self.merge_span_conflict()


class ParserResult:
    _value: str = None
    _entity_name: str
    _definition_name: str

    def __init__(self, result: str, entity_name: str, definition_name: str):
        self._value = result
        self._entity_name = entity_name
        self._definition_name = definition_name

    @property
    def value(self):
        return self._value

    @property
    def entity_name(self):
        return self._entity_name

    @property
    def definition_name(self):
        return self._definition_name

    def __repr__(self):
        return f"{self._entity_name}: {self._value}"


class EmptyResult(ParserResult):
    def __init__(self):
        super().__init__("", "", "")
