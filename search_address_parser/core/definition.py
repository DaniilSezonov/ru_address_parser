import re
from typing import Pattern


class MatchPosition:
    LEFT = 0
    RIGHT = 1
    #MIDDLE = 2


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
            result_expr = rf"[\w|-]+\s{self.value}"
        elif self.match_position == MatchPosition.RIGHT:
            result_expr = rf"{self.value}\s?[\w+|-]+"
        for abbr in self.abbreviations:
            result_expr += rf"|{abbr}[\.|\s]+[\w+|-]+"
        return re.compile(result_expr, flags=re.IGNORECASE)
