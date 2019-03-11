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
    include_definition_part: bool = True

    def __init__(self, value: str, abbreviations: [str], match_pos: MatchPosition = DEFAULT_MATCH_POS, include_definition_part: bool = True):
        self.value = value
        self.abbreviations = abbreviations
        self.match_position = match_pos
        self.include_definition_part = include_definition_part

    def to_regular_expr(self) -> (Pattern, Pattern):
        value_expr = r""
        abbreviation_expr = r""
        if self.match_position == MatchPosition.LEFT:
            value_expr = rf"([\s|\w|-]+)\s{self.value}"
        elif self.match_position == MatchPosition.RIGHT:
            value_expr = rf"{self.value}\s([\s|\w|-]+)"
        for index, abbr in enumerate(self.abbreviations):
            abbreviation_expr += rf"{abbr}[\.|\s]+([\s|\w|-]+)|"
        return re.compile(value_expr, flags=re.IGNORECASE), re.compile(abbreviation_expr[:-1], flags=re.IGNORECASE)

    def assume(self, value: str) -> [SuitableDefinition] or None:
        value_expr, abbr_expr = self.to_regular_expr()
        value_match = value_expr.search(value)
        abbr_match = abbr_expr.search(value)
        if value_match and value_match.groups():
            suitable_definitions = []
            for index, match_value in enumerate(value_match.groups()):
                if not match_value:
                    break
                suitable_value = match_value
                if self.include_definition_part:
                    if self.match_position == MatchPosition.RIGHT:
                        suitable_value = f'{self.value} {suitable_value}'
                    elif self.match_position == MatchPosition.LEFT:
                        suitable_value = f'{suitable_value} {self.value}'
                suitable_definitions.append(
                    SuitableDefinition(
                        suit_value=suitable_value,
                        def_value=self.value,
                        match_span=value_match.span(index)
                    )
                )
            return suitable_definitions
        elif abbr_match and abbr_match.groups():
            suitable_definitions = []
            for index, match_value in enumerate(abbr_match.groups()):
                if not match_value:
                    break
                suitable_definitions.append(
                    SuitableDefinition(
                        suit_value=match_value,
                        def_value=self.value,
                        match_span=abbr_match.span(index)
                    )
                )
            return suitable_definitions
        return None


