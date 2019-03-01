import json
import random
from typing import Callable
import requests


class GeocodingError(Exception):
    def __init__(self):
        super().__init__("Geocoder is dead :(")


class Geocoder():
    URL = ""
    GEOCODER_KEY: str = None
    SUCCESS_STATUS_CODE = 200

    def geocode(self, lat, lon, **kwargs):
        raise NotImplementedError()

    def address_from_response(self, geocoder_response) -> str:
        raise NotImplementedError()


class YandexGeocoder(Geocoder):
    from search_address_parser.tests.data_generator.private_data import PRIVATE_GEOCODER_KEY
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

    def address_from_response(self, geocoder_response: dict):
        assert isinstance(geocoder_response, dict), "geocoder_response must be a dict object."
        response = geocoder_response.get('response')
        if not response:
            print("\033[93m Yandex geocoder return empty response.'\033[0m'")
        geo_objects = response['GeoObjectCollection']['featureMember']
        address = geo_objects[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
        return address


def russian_coordinate_randomizer() -> tuple:
    """TODO очень посредственное решение"""
    east_side_point = (55.96056, 37.7097609)
    west_side_point = (70.982239, 156.572690)
    return (
        round(random.uniform(east_side_point[0], west_side_point[0]),5),
        round(random.uniform(east_side_point[1], west_side_point[1]),5)
    )


class AddressRandomizer:
    geocoder: Geocoder = None
    coordinate_randomizer: Callable = None

    def __init__(self, geocoder: Geocoder, coordinate_randomizer: Callable):
        assert isinstance(coordinate_randomizer, Callable), \
            "coordinate_randomizer parameter must be callable and return tuple of lat, lon"
        self.coordinate_randomizer = coordinate_randomizer
        self.geocoder = geocoder

    def get_random_address(self):
        lat, lon = self.coordinate_randomizer()
        return self.geocoder.address_from_response(self.geocoder.geocode(lat, lon))


def generate_json_data(file_name="test_data.json", addresses_count=50):
    addresses = []
    _ar = AddressRandomizer(YandexGeocoder(), russian_coordinate_randomizer)
    for _ in range(addresses_count):
        addresses.append({'address': _ar.get_random_address()})
    with open(file_name, 'w') as file:
        json.dump(addresses, file)

