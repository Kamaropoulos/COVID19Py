from typing import Dict, List
import requests
import json
from analysis import Analysis

class COVID19(object):

    default_url = "https://covid-tracker-us.herokuapp.com"
    default_data_source = 'jhu'
    #not sure if it will compile, if not change url below back to url = "https://covid-tracker-us.herokuapp.com"

    def __init__(self, url=default_url, data_source=default_data_source):

        self.url = url
        self.data_source = data_source   
        self.obj = Analysis(self.url, self.data_source) 

    #hiding all private methods in another file, the user of this package does not need to interact with them

    def getAll(self, timelines=False):
        
        timelines = timelines
        return self.obj.getAll(timelines)

    def getLatestChanges(self):
        
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
        rank_by = rank_by
        return self.obj.getLocations(timelines, rank_by)

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        country_code = country_code
        timelines = timelines
        return self.obj.getLocationByCountryCode(country_code, timelines)
    
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
