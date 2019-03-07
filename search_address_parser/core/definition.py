import re
from typing import Pattern, Tuple


class MatchPosition:
    LEFT = 0
    RIGHT = 1


class SuitableDefinition:
    definition_value: str
    suitable_value: str
    match_span: Tuple[int, int]

    def __init__(self, def_value: str, suit_value: str, match_span: Tuple[int, int]):
        self.definition_value = def_value
        self.suitable_value = suit_value
        self.match_span = match_span

    def is_similar_on(self, value: 'SuitableDefinition'):
        return self.definition_value.lower().startswith(value.definition_value.lower())

    def __repr__(self):
        return f"{self.definition_value}: {self.suitable_value}"


class Definition:
    DEFAULT_MATCH_POS = MatchPosition.LEFT

    value: str = ""
    abbreviations: str = []
    match_position: MatchPosition

    def __init__(self, value: str, abbreviations: [str], match_pos: MatchPosition = DEFAULT_MATCH_POS):
        self.value = value
        self.abbreviations = abbreviations
        self.match_position = match_pos

    def to_regular_expr(self) -> Pattern:
        result_expr = r""
        if self.match_position == MatchPosition.LEFT:
            result_expr = rf"([\s|\w|-]+)\s{self.value}"
        elif self.match_position == MatchPosition.RIGHT:
            result_expr = rf"{self.value}\s([\s|\w|-]+)"
        for abbr in self.abbreviations:
            result_expr += rf"|{abbr}[\.|\s]+([\s|\w|-]+)"
        return re.compile(result_expr, flags=re.IGNORECASE)

    def assume(self, value: str) -> [SuitableDefinition] or None:
        match = self.to_regular_expr().match(value)
        if match.groups():
            return [
                SuitableDefinition(
                    suit_value=match_value,
                    def_value=self.value,
                    match_span=match.span(index)
                ) for index, match_value in enumerate(match.groups())
            ]
        return None


