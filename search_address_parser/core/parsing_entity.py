from typing import List, Pattern

from search_address_parser.core.definition import Definition


class ParsingEntity:
    name: str = ""
    definitions: List[Definition]

    def get_patterns(self) -> List[Pattern]:
        return [definition.to_regular_expr() for definition in self.definitions]
