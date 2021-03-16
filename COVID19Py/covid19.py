from typing import Dict, List
from .fetchdata import FetchData


class COVID19(object):
    def __init__(self, url="https://covid-tracker-us.herokuapp.com", data_source='jhu'):
        """
        Initialize the root entity

        :param url: str: url of the source to retrieve data
        :param data_source: str: name of the source to retrieve data from
        """
        try:
            self.rootIdentity = url
            self.dataSource = FetchData(self.rootIdentity, data_source)

        except:
            raise Exception("Error connecting to source!")

    def getAll(self, timelines=False):
        """
        This methods returns the all the latest data, optionally with the timeline too

        :param timelines: bool: True or False value to receive timeline of the data
        :return: Dict[str: int]: containing all the available data with one command.

        """
        return self.dataSource.getAll(timelines=timelines)

    def getLatestChanges(self):
        """
        :return: Dict[str: int]: returns the latest changes in number of confirmed, deaths, and recovered cases
                                 since the last retrieval of data.
        """
        return self.dataSource.getLatestChanges()

    def getLatest(self) -> List[Dict[str, int]]:

        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        return self.dataSource.getLatest()

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.

        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        return self.dataSource.getLocations(timelines=timelines, rank_by=rank_by)

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        return self.dataSource.getLocationByCountryCode(country_code=country_code, timelines=timelines)

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        return self.dataSource.getLocationByCountry(country=country, timelines=timelines)

    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        return self.dataSource.getLocationById(country_id=country_id)
