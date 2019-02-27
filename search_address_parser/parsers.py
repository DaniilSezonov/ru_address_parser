from search_address_parser.core.parser import Parser
from search_address_parser.entitys import RegionEntity, CityEntity, StreetEntity, AddressEntity


class RegionParser(Parser):
    entity = RegionEntity()


class CityParser(Parser):
    entity = CityEntity()


class StreetParser(Parser):
    entity = StreetEntity()


class AddressParser(ParserList):
    parsers = [RegionParser(), CityParser(), StreetParser()]
    entity = AddressEntity()
