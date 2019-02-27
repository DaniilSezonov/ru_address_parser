from search_address_parser.core.parsing_entity import ParsingEntity


class ParsedData:
    entity_name: str
    match: str

    def __init__(self, entity_name, match):
        self.entity_name = entity_name
        self.match = match

    def __repr__(self):
        return f"{self.entity_name} : {self.match}"


class NotParsedData:
    _value: str

    def __init__(self, value: str = None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value.strip()

    def __repr__(self):
        return self._value


class ParserResult:
    _parsed_data: [ParsedData]
    _not_parsed_data: NotParsedData

    def __init__(self):
        self._parsed_data = []
        self._not_parsed_data = NotParsedData()

    @property
    def parsed_data(self):
        return self._parsed_data

    @parsed_data.setter
    def parsed_data(self, value: ParsedData):
        if isinstance(value, list):
            self._parsed_data = self._parsed_data + value
        else:
            self._parsed_data.append(value)

    @property
    def not_parsed_data(self):
        return self._not_parsed_data

    @not_parsed_data.setter
    def not_parsed_data(self, value: NotParsedData):
        if isinstance(value, str):
            self._not_parsed_data = NotParsedData(value)
        elif isinstance(value, NotParsedData):
            self._not_parsed_data = value
        else:
            raise TypeError()

    def merge(self, value):
        self.parsed_data = value.parsed_data
        self.not_parsed_data = value.not_parsed_data

    def __repr__(self):
        return f"{self._parsed_data}"


class Parser:
    entity: ParsingEntity = None

    def parse(self, value: str) -> ParserResult:
        result = ParserResult()
        result.not_parsed_data = value
        for definition in self.entity.definitions:
            matches = definition.to_regular_expr().findall(result.not_parsed_data.value)
            if matches:
                for match in matches:
                    result.parsed_data = ParsedData(entity_name=self.entity.name, match=match)
                    result.not_parsed_data = result.not_parsed_data.value.replace(match, '').strip()
                break
        return result


class ParserList(Parser):
    parsers: [Parser] = []

    def parse(self, value: str) -> ParserResult:
        result = ParserResult()
        result.not_parsed_data = value
        for parser in self.parsers:
            result.merge(parser.parse(result.not_parsed_data))
        return result











