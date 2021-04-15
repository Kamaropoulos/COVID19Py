from typing import Dict, List
import requests
import json


class COVID19(object):
    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None
    source = None
    _valid_data_sources = []

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    def __init__(self):
        source = Source()

    def getAll(self, timelines=False):
        source._update(timelines)
        return self.latestData

    def getLatestChanges(self):
        changes = None
        if self.previousData:
            changes = {
                "confirmed": source.latestData["latest"]["confirmed"] - source.latestData["latest"]["confirmed"],
                "deaths": source.latestData["latest"]["deaths"] - source.latestData["latest"]["deaths"],
                "recovered": source.latestData["latest"]["recovered"] - source.latestData["latest"]["recovered"],
            }
        else:
            changes = {
                "confirmed": 0,
                "deaths": 0,
                "recovered": 0,
            }
        return changes

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            data = source._request(
                "/v2/locations", {"country_code": country_code, "timelines": str(timelines).lower()})
        else:
            data = source._request(
                "/v2/locations", {"country_code": country_code})
        return data["locations"]

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            data = source._request(
                "/v2/locations", {"country": country, "timelines": str(timelines).lower()})
        else:
            data = source._request("/v2/locations", {"country": country})
        return data["locations"]

    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        data = source._request("/v2/locations/" + str(country_id))
        return data["location"]


class Source(object):
    __instance = None

    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None
    _valid_data_sources = []

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    def __init__(cls, url="https://covid-tracker-us.herokuapp.com", data_source='jhu'):
        # Skip mirror checking if custom url was passed
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        if url == cls.default_url:
            # Load mirrors
            response = requests.get(cls.mirrors_source)
            response.raise_for_status()
            cls.mirrors = response.json()

            # Try to get sources as a test
            for mirror in cls.mirrors:
                # Set URL of mirror
                cls.url = mirror["url"]
                result = None
                try:
                    result = cls._getSources()
                except Exception as e:
                    # URL did not work, reset it and move on
                    cls.url = ""
                    continue

                # TODO: Should have a better health-check, this is way too hacky...
                if "jhu" in result:
                    # We found a mirror that worked just fine, let's stick with it
                    break

                # None of the mirrors worked. Raise an error to inform the user.
                raise RuntimeError("No available API mirror was found.")

        else:
            cls.url = url

        cls._valid_data_sources = cls._getSources()
        if data_source not in cls._valid_data_sources:
            raise ValueError(
                "Invalid data source. Expected one of: %s" % cls._valid_data_sources)
        cls.data_source = data_source

    def _update(cls, timelines):
        latest = cls.getLatest()
        locations = cls.getLocations(timelines)
        if cls.latestData:
            cls.previousData = cls.latestData
        cls.latestData = {
            "latest": latest,
            "locations": locations
        }

    def _getSources(cls):
        response = requests.get(cls.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]

    def _request(cls, endpoint, params=None):
        if params is None:
            params = {}
        response = requests.get(cls.url + endpoint,
                                {**params, "source": cls.data_source})
        response.raise_for_status()
        return response.json()

    def getLatest(cls) -> List[Dict[str, int]]:
        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        data = cls._request("/v2/latest")
        return data["latest"]

    def getLocations(cls, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        data = None
        if timelines:
            data = cls._request(
                "/v2/locations", {"timelines": str(timelines).lower()})
        else:
            data = cls._request("/v2/locations")

        data = data["locations"]

        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError(
                    "Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(
                data, key=lambda i: i['latest'][rank_by], reverse=True)
            data = ranked

        return data
