from search_address_parser.core.parsing_entity import ParsingEntity
from search_address_parser.difinitions import REGION_DEFINITIONS, CITY_DEFINITIONS, STREET_DEFINITIONS


class RegionEntity(ParsingEntity):
    name = "region"
    definitions = REGION_DEFINITIONS


class CityEntity(ParsingEntity):
    name = "city"
    definitions = CITY_DEFINITIONS


class StreetEntity(ParsingEntity):
    name = "street"
    definitions = STREET_DEFINITIONS


class AddressEntity(ParsingEntity):
    name = "address"
    definitions = []
