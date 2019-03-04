import json
import unittest
from enum import Enum
from typing import Callable, List

from search_address_parser.parsers import RegionParser
from search_address_parser.tests.data_generator.get_test_data import TestData, AddressRandomizer, YandexGeocoder, \
    russian_coordinate_randomizer


class LoadType(Enum):
    JSON = 1
    GEOCODER = 2


class TestDataLoader:
    _data: List[TestData] = []
    DEFAULT_JSON_PATH = 'test_data.json'
    DEFAULT_GENERATED_ADDRESS_COUNT = 20

    def __init__(self, loading_type: LoadType, **kwargs):
        if loading_type == LoadType.JSON:
            path = kwargs.get('path', self.DEFAULT_JSON_PATH)
            with open(path, 'r') as file:
                for data_item in json.load(file):
                    self._data.append(TestData(**data_item))
        elif loading_type == LoadType.GEOCODER:
            address_generator: Callable = kwargs.get('address_generator')
            assert address_generator, "address_generator is not set in kwargs. "
            assert isinstance(address_generator, Callable), "Address generator is not callable."
            count: int = kwargs.get('count', self.DEFAULT_GENERATED_ADDRESS_COUNT)
            for _ in range(count):
                self._data.append(address_generator())
        else:
            raise TypeError("Unknown loading type")

    def get_data(self) -> [TestData]:
        return self._data


class TestRegionParsers(unittest.TestCase):
    data: List[TestData]

    def setUp(self):
        data_loader = TestDataLoader(loading_type=LoadType.JSON)
        # randomizer = AddressRandomizer(YandexGeocoder(), russian_coordinate_randomizer)
        # setup = {
        #     'address_generator': randomizer.get_random_address
        # }
        # data_loader = TestDataLoader(loading_type=LoadType.GEOCODER, **setup)
        self.data = data_loader.get_data()

    def test_region_parser(self):
        parser = RegionParser()
        for item in self.data:
            result = parser.parse(item.inline_address)
            for parsed_result in result.parsed_data:
                #TODO вдальнейшем данный тест должен проверять полное совпадение, наверное должен!
                self.assertTrue(item.verified_region.find(parsed_result.match) != -1)
