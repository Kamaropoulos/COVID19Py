from typing import Dict, List
import requests
import json

# COVID19 class but with the application of the Singleton Creational Design Pattern
class COVID19(object):
    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None
    _valid_data_sources = []

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    # Declaration of single private static instance of the class. Done to fulfill requirement for the Singleton Creational Design Pattern.
    __singlePrivateInstance = None

    # Constructor. Already privated, meaning that its already fulfills a requirement for the Singleton Creational Design Pattern.
    def __init__(self, url="https://covid-tracker-us.herokuapp.com", data_source='jhu'):

	# Checks to see if an instance has already been created. If it has, we put out an error message. Otherwise, we create a new instance.
        if COVID19.__singlePrivateInstance != None:
	    raise Exception("Singleton pattern has been applied. An instance was previously created, hence new instance cannot be created. Use getCOVID19Instance() to access the instance.")
        else:
            COVID19.__singlePrivateInstance = self

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
                    result = self._getSources()
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

        self._valid_data_sources = self._getSources()
        if data_source not in self._valid_data_sources:
            raise ValueError("Invalid data source. Expected one of: %s" % self._valid_data_sources)
        self.data_source = data_source


    # Public method that allows access to the single instance. Requirement for Singleton Creation Design Pattern.
    @staticmethod
    def getCOVID19Instance():
        if COVID19.__singlePrivateInstance == None
            COVID19()
        return COVID19.__singlePrivateInstance


    # Updates to latest data
    def _update(self, timelines):
        latest = self.getLatest()
        locations = self.getLocations(timelines)
        if self.latestData:
            self.previousData = self.latestData
        self.latestData = {
            "latest": latest,
            "locations": locations
        }


    # Gets data sources
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


    # Gets all data at once
    def getAll(self, timelines=False):
        self._update(timelines)
        return self.latestData


    # Gets the latest changes in COVID-19 case data since last request
    def getLatestChanges(self):
        changes = None
        if self.previousData:
            changes = {
                "confirmed": self.latestData["latest"]["confirmed"] - self.previousData["latest"]["confirmed"],
                "deaths": self.latestData["latest"]["deaths"] - self.previousData["latest"]["deaths"],
                "recovered": self.latestData["latest"]["recovered"] - self.previousData["latest"]["recovered"],
            }
        else:
            changes = {
                "confirmed": 0,
                "deaths": 0,
                "recovered": 0,
            }
        return changes


    # Gets the latest COVID-19 case data
    def getLatest(self) -> List[Dict[str, int]]:
        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        data = self._request("/v2/latest")
        return data["latest"]


    # Get COVID-19 case data relating to all locations with COVID-19
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


    # Get COVID-19 case data by method of country code
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
    

    # Get COVID-19 case data by method of country name
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


    # Get COVID-19 case data by method of country id
    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        data = self._request("/v2/locations/" + str(country_id))
        return data["location"]