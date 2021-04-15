from abc import ABC,abstractmethod
from typing import Dict, List
import requests
import json

class AbstractAPI(ABC):
    def __init__(self,implementation):
        self.implementation = implementation
        self.previousData = None
        self.latestData = None
    @abstractmethod
    def _update(self, timelines):
        pass

    @abstractmethod
    def _request(self, endpoint, params=None):
        pass


    @abstractmethod
    def getAll(self, timelines=False):
        pass


    @abstractmethod
    def getLatestChanges(self):
        pass

    @abstractmethod
    def getLatest(self) -> List[Dict[str, int]]:
        pass

    @abstractmethod
    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        pass


    @abstractmethod
    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        pass


    @abstractmethod
    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        pass

    @abstractmethod
    def getLocationById(self, country_id: int):
        pass


class COVIDAPI(AbstractAPI):

    def __init__(self,implementation):
        super().__init__(implementation)
    def _update(self, timelines):
        latest = self.getLatest()
        locations = self.getLocations(timelines)
        if self.latestData:
            self.previousData = self.latestData
        self.latestData = {
            "latest": latest,
            "locations": locations
        }

    def _request(self, endpoint, params=None):
        if params is None:
            params = {}
        response = requests.get(self.implementation.url+endpoint,{**params,"source":self.implementation.data_source})
        response.raise_for_status()
        return response.json()

    def getAll(self,timelines=False):
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
        endpoint = self.implementation.getEndLatest()
        data = self._request(endpoint)
        return data["latest"]

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        data = None

        endpoint = self.implementation.getEndLocations()
        if timelines:
            data = self._request(endpoint, {"timelines": str(timelines).lower()})
        else:
            data = self._request(endpoint)

        data = data["locations"]
        
        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError("Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(data, key=lambda i: i['latest'][rank_by], reverse=True)
            data = ranked

        return data

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        data = None
        endpoint = self.implementation.getEndLocations()

        if timelines:
            data = self._request(endpoint, {"country_code": country_code, "timelines": str(timelines).lower()})
        else:
            data = self._request(endpoint, {"country_code": country_code})
        return data["locations"]

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        data = None
        endpoint = self.implementation.getEndLocations()

        if timelines:
            data = self._request(endpoint, {"country": country, "timelines": str(timelines).lower()})
        else:
            data = self._request(endpoint, {"country": country})
        return data["locations"]


    
    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        endpoint = self.implementation.getEndLocations()

        data = self._request(endpoint + str(country_id))
        return data["location"]
