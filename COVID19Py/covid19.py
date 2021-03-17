from typing import Dict, List
import requests
import json

class COVID19(object):
    default_url = "https://covid-tracker-us.herokuapp.com"

    def __init__(self, url="default_url", data_source='jhu'):
        self.url = url
        self.data_source = data_source
        self.obj = base(self.url, self.data_source)

    def getAll(self, timelines=False):
        """
        :return: All available data with one command
        """
        timelines = timelines
        return self.obj.getAll(timelines)

    def getLatestChanges(self):
        """
        :return: The change between current, and previous version of the retreived data
        """
        return self.obj.getLatestChanges()

    def getLatest(self) -> List[Dict[str, int]]:
        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        return self.obj.getLatest()

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        timelines = timelines
        return self.obj.getLocations(timelines, rank_by)

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        country_code = country_code
        return self.obj.getLocationByCountryCode(country_code, rank_by)
    
    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        country = country
        timelines = timelines
        return self.obj.getLocationByCountry(country, timelines)

    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        country_id = country_id
        return self.obj.getLocationById(country_id)