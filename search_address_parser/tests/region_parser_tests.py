import unittest

from search_address_parser.parsers import RegionParser


class TestRegionParsers(unittest.TestCase):
    def setUp(self):
        self.region_parser = RegionParser()

    def