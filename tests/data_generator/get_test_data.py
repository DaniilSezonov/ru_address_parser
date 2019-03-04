import json
import random
from typing import Callable
import requests


class TestData:
    def __init__(self, **kwargs):
        self.inline_address = kwargs.get('inline_address', '')
        self.verified_city = kwargs.get('verified_city', '')
        self.verified_street = kwargs.get('verified_street', '')
        self.verified_region = kwargs.get('verified_region', '')

    inline_address: str = ""
    verified_region: str = ""
    verified_city: str = ""
    verified_street: str = ""


class GeocodingError(Exception):
    def __init__(self):
        super().__init__("Geocoder is dead :(")


class Geocoder:
    URL = ""
    GEOCODER_KEY: str = None
    SUCCESS_STATUS_CODE = 200

    def geocode(self, lat, lon, **kwargs):
        raise NotImplementedError()

    def inline_address_from_response(self, geocoder_response) -> str:
        raise NotImplementedError()

    def verified_region_from_response(self, geocoder_response) -> str:
        raise NotImplementedError()

    def verified_city_from_response(self, geocoder_response) -> str:
        raise NotImplementedError()

    def verified_street_from_response(self, geocoder_response) -> str:
        raise NotImplementedError()


class YandexGeocoder(Geocoder):
    from tests.data_generator.private_data import PRIVATE_GEOCODER_KEY
    GEOCODER_KEY = PRIVATE_GEOCODER_KEY
    URL = "https://geocode-maps.yandex.ru/1.x/"

    def geocode(self, lat, lon, **kwargs):
        kwargs['apikey'] = self.GEOCODER_KEY
        kwargs['geocode'] = f"{lon},{lat}"
        kwargs['format'] = "json"
        response = requests.get(self.URL, params=kwargs)
        if response.status_code != self.SUCCESS_STATUS_CODE:
            raise GeocodingError()
        return response.json()

    def inline_address_from_response(self, geocoder_response: dict):
        details_address = self.get_address_details(geocoder_response)
        inline_address = details_address.get('formatted')
        if not inline_address:
            return ""
        return inline_address

    def verified_city_from_response(self, geocoder_response):
        details_address = self.get_address_details(geocoder_response)
        address_components = details_address['Components']
        if not address_components:
            return ""
        for component in address_components:
            if component['kind'] == 'area' or component['kind'] == 'locality':
                return component['name']
        return ""

    def verified_region_from_response(self, geocoder_response):
        details_address = self.get_address_details(geocoder_response)
        address_components = details_address['Components']
        if not address_components:
            return ""
        for component in address_components:
            if component['kind'] == 'province' and component['name'].find('федеральный округ') == -1:
                return component['name']
        return ""

    def verified_street_from_response(self, geocoder_response):
        details_address = self.get_address_details(geocoder_response)
        address_components = details_address['Components']
        if not address_components:
            return ""
        for component in address_components:
            if component['kind'] == 'street':
                return component['name']
        return ""

    def get_address_details(self, geocoder_response: dict):
        assert isinstance(geocoder_response, dict), "geocoder_response must be a dict object."
        response = geocoder_response.get('response')
        if not response:
            print("\033[93m Yandex geocoder return empty response.'\033[0m'")
        return response['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']


def russian_coordinate_randomizer() -> tuple:
    """TODO очень посредственное решение"""
    east_side_point = (55.96056, 37.7097609)
    west_side_point = (70.982239, 156.572690)
    return (
        round(random.uniform(east_side_point[0], west_side_point[0]), 5),
        round(random.uniform(east_side_point[1], west_side_point[1]), 5)
    )


class AddressRandomizer:
    geocoder: Geocoder = None
    coordinate_randomizer: Callable = None

    def __init__(self, geocoder: Geocoder, coordinate_randomizer: Callable):
        assert isinstance(coordinate_randomizer, Callable), \
            "coordinate_randomizer parameter must be callable and return tuple of lat, lon"
        self.coordinate_randomizer = coordinate_randomizer
        self.geocoder = geocoder

    def get_random_address(self) -> TestData:
        lat, lon = self.coordinate_randomizer()
        geo_response = self.geocoder.geocode(lat, lon)
        test_data = TestData()
        test_data.inline_address = self.geocoder.inline_address_from_response(geo_response)
        test_data.verified_city = self.geocoder.verified_city_from_response(geo_response)
        test_data.verified_region = self.geocoder.verified_region_from_response(geo_response)
        test_data.verified_street = self.geocoder.verified_street_from_response(geo_response)
        return test_data


def generate_json_data(file_name="test_data.json", addresses_count=50):
    addresses = []
    ar = AddressRandomizer(YandexGeocoder(), russian_coordinate_randomizer)
    for _ in range(addresses_count):
        addresses.append(ar.get_random_address().__dict__)
    with open(file_name, 'w') as file:
        json.dump(addresses, file, ensure_ascii=False)

