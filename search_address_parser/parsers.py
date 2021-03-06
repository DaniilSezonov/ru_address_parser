from search_address_parser.core.data_store import DataStore
from search_address_parser.core.parser import Parser
from search_address_parser.core.parser_list import ParserList
from search_address_parser.entities import RegionEntity, CityEntity, StreetEntity, AddressEntity


class RegionParser(Parser):
    entity = RegionEntity()


class CityParser(Parser):
    entity = CityEntity()


class StreetParser(Parser):
    entity = StreetEntity()
    #todo
    store = None


class AddressParser(ParserList):
    parsers = [RegionParser(), CityParser(), StreetParser()]
    entity = AddressEntity()
