from typing import Dict, List
import requests
from .DataClass import _request
from .covid19singleton import covid19singleton

import json


class COVID19(object,covid19singleton):
    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None
    _valid_data_sources = []

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    def __init__(self, url="https://covid-tracker-us.herokuapp.com", data_source='jhu'):
        # Skip mirror checking if custom url was passed
        if url == self.default_url:
            # Load mirrors
            response = requests.get(self.mirrors_source)
            response.raise_for_status()
            self.mirrors = response.json()

            # Try to get sources as a test
            for mirror in self.mirrors:
                # Set URL of mirror
                self.url = mirror["url"]
                result = None
                try:
                    endpoint = '/v2/sources'
                    mydata = _request(self.url, self.data_source, endpoint)
                    result = mydata.getSources()
                except Exception as e:
                    # URL did not work, reset it and move on
                    self.url = ""
                    continue

                # TODO: Should have a better health-check, this is way too hacky...
                if "jhu" in result:
                    # We found a mirror that worked just fine, let's stick with it
                    break

                # None of the mirrors worked. Raise an error to inform the user.
                raise RuntimeError("No available API mirror was found.")

        else:
            self.url = url
        mydata = _request(self.url, self.data_source, endpoint)
        self._valid_data_sources = mydata.getSources()

        if data_source not in self._valid_data_sources:
            raise ValueError("Invalid data source. Expected one of: %s" % self._valid_data_sources)
        self.data_source = data_source

    def _update(self, timelines):
        latest = self.getLatest()
        locations = self.getLocations(timelines)
        if self.latestData:
            self.previousData = self.latestData
        self.latestData = {
            "latest": latest,
            "locations": locations
        }

    def getAll(self, timelines=False):
        self._update(timelines)
        return self.latestData

    def getLatestChanges(self):
        changes = None
        if self.previousData:
            changes = {
                "confirmed": self.latestData["latest"]["confirmed"] - self.latestData["latest"]["confirmed"],
                "deaths": self.latestData["latest"]["deaths"] - self.latestData["latest"]["deaths"],
                "recovered": self.latestData["latest"]["recovered"] - self.latestData["latest"]["recovered"],
            }
        else:
            changes = {
                "confirmed": 0,
                "deaths": 0,
                "recovered": 0,
            }
        return changes

    def getLatest(self) -> List[Dict[str, int]]:
        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        endpoint = "/v2/latest"
        mydata = _request(self.url, self.data_source, endpoint, params=None)
        result = mydata._request()
        return result



    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        mydata = None
        endpoint = "/v2/locations"
        if timelines:

            mydata = _request(self.url, self.data_source, endpoint, params={"timelines": str(timelines).lower()})
            mydata = mydata._request()
        else:
            mydata = _request(self.url, self.data_source, endpoint, params=None)
            mydata = mydata._request()

        mydata = mydata["locations"]

        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError("Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(mydata, key=lambda i: i['latest'][rank_by], reverse=True)
            mydata = ranked

        return mydata

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        mydata = None
        endpoint = "/v2/locations"
        if timelines:
            mydata = _request(self.url, self.data_source, endpoint, params={"timelines": str(timelines).lower()})
            mydata = mydata._request()
        else:
            mydata = _request(self.url, self.data_source, endpoint, params=None)
            mydata = mydata._request()
        return mydata["locations"]

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        mydata = None
        endpoint = "/v2/locations"
        if timelines:
            mydata = _request(self.url, self.data_source, endpoint, params={"timelines": str(timelines).lower()})
            mydata = mydata._request()
        else:
            mydata = _request(self.url, self.data_source, endpoint, params=None)
            mydata = mydata._request()
        return mydata["locations"]


    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        mydata = None
        endpoint = "/v2/locations/" +  str(country_id)
        mydata = _request(self.url, self.data_source, endpoint, params=None)
        mydata = mydata._request()
        
        return mydata["locations"]
