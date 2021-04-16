from typing import Dict, List
import requests
import json
import threading


# This singleton class is a metaclass that make sure that there's only one system controlling the requests from the users

class Singleton(type):
    # This is a private, static dictionary instance that stores the cases for different countries
    _sourceInstance = {}
    # To ensure safety during multi-threading, we need to lock the object when creating it
    _objLock: Lock = Lock()

    @staticmethod
    def __call__(source, *args, **kwargs):
        # When the object is correctly locked during its creation
        with source._objLock:
            # If the object is not occured in the list
            if source not in source._sourceInstance:
                """ 
                then we can let the metaclass cover the inheritance 
                and create the singleton instance
                """
                singletonInstance = super().__call__(*args, **kwargs)
                source._sourceInstance[source] = singletonInstance
        return source._sourceInstance[source]


class COVID19(object, metaclass=Singleton):
    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    # Added _sourceInstance in the parameter
    def __init__(self, url="https://covid-tracker-us.herokuapp.com", data_source="jhu",
                 _sourceInstance={'jhu': "https://covid-tracker-us.herokuapp.com"}):
        # Skip mirror checking if custom url was passed
        if url == self.default_url:
            # Load mirrors
            response = requests.get(self.mirrors_source)
            response.raise_for_status()
            self.mirrors = response.json()

            # Add sources' urls and providers in the _sourceInstance dict
            for mirror in self.mirrors:
                _sourceInstance.add(mirror["provider"], mirror["url"])
                try:
                    # see if the url is from one of the providers
                    result = self._getSources()
                except Exception as e:
                    # url is not in the database, reset it and move on
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

        """ 
        if the input data_source is not in the dictionary 
        that contains all the vaild sources, raise error
        """
        if data_source not in self._sourceInstance:
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

    def _getSources(self):
        response = requests.get(self.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]

    def _request(self, endpoint, params=None):
        if params is None:
            params = {}
        response = requests.get(self.url + endpoint, {**params, "source": self.data_source})
        response.raise_for_status()
        return response.json()

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
        data = self._request("/v2/latest")
        return data["latest"]

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        data = None
        if timelines:
            data = self._request("/v2/locations", {"timelines": str(timelines).lower()})
        else:
            data = self._request("/v2/locations")

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
        if timelines:
            data = self._request("/v2/locations", {"country_code": country_code, "timelines": str(timelines).lower()})
        else:
            data = self._request("/v2/locations", {"country_code": country_code})
        return data["locations"]

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            data = self._request("/v2/locations", {"country": country, "timelines": str(timelines).lower()})
        else:
            data = self._request("/v2/locations", {"country": country})
        return data["locations"]

    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        data = self._request("/v2/locations/" + str(country_id))
        return data["location"]