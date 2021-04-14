from typing import Dict, List
import requests
import json

class COVID19(object):
    data = None

    def __init__(self, data=None):
        if data is not None:
            self.data = data

    def _update(self, timelines):
        latest = self.getLatest()
        locations = self.getAllLocations(timelines)
        if self.data.latestData:
            self.data.previousData = self.data.latestData
        self.data.latestData = {
            "latest": latest,
            "locations": locations
        }

    def _request(self, endpoint, params=None):
        if params is None:
            params = {}
        response = requests.get(self.data.url + endpoint, {**params, "source":self.data.data_source})
        response.raise_for_status()
        return response.json()

    def getAll(self, timelines=False):
        self._update(timelines)
        return self.data.latestData

    def getLatestChanges(self):
        changes = None
        if self.data.previousData:
            changes = {
                "confirmed": self.data.latestData["latest"]["confirmed"] - self.data.latestData["latest"]["confirmed"],
                "deaths": self.data.latestData["latest"]["deaths"] - self.data.latestData["latest"]["deaths"],
                "recovered": self.data.latestData["latest"]["recovered"] - self.data.latestData["latest"]["recovered"],
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

    def getAllLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
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

    # def getLocationData(self, location, timelines=False):
    #     """
    #     :param location: Location containing any combination of strings denoting...
    #         - the name of the country
    #         - the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
    #         - the country id, an int
    #     :param timelines: Whether timeline information should be returned as well.
    #     :return: Either a list of areas that correspond to the location, or a dictionary with case information for the specified location.
    #     """
    #     # retrieve by country name
    #     if location.country != "":
    #         data = None
    #         if timelines:
    #             data = self._request("/v2/locations", {"country": location.country, "timelines": str(timelines).lower()})
    #         else:
    #             data = self._request("/v2/locations", {"country": location.country})
    #         return data["locations"]

    #     # retrieve by country code
    #     if location.country_code != "":
    #         data = None
    #         if timelines:
    #             data = self._request("/v2/locations", {"country_code": location.country_code, "timelines": str(timelines).lower()})
    #         else:
    #             data = self._request("/v2/locations", {"country_code": location.country_code})
    #         return data["locations"]

    #     # retrieve by country id
    #     if location.country_id != "":
    #         data = self._request("/v2/locations/" + str(location.country_id))
    #         return data["location"]

    def getLocationData(self, locationGroup, timelines=False):
        """
        :param location: Location containing any combination of strings denoting...
            - the name of the country
            - the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
            - the country id, an int
        :param timelines: Whether timeline information should be returned as well.
        :return: Either a list of areas that correspond to the location, or a dictionary with case information for the specified location.
        """

        output = []

        for location in locationGroup.locList:
            # retrieve by country name
            if location.country != "":
                data = None
                if timelines:
                    data = self._request("/v2/locations", {"country": location.country, "timelines": str(timelines).lower()})
                else:
                    data = self._request("/v2/locations", {"country": location.country})
                output += data["locations"]

            # retrieve by country code
            elif location.country_code != "":
                data = None
                if timelines:
                    data = self._request("/v2/locations", {"country_code": location.country_code, "timelines": str(timelines).lower()})
                else:
                    data = self._request("/v2/locations", {"country_code": location.country_code})
                output += data["locations"]

            # retrieve by country id
            elif location.country_id != "":
                data = self._request("/v2/locations/" + str(location.country_id))
                output += data["location"]
        
        return output

class Data:
    __instance = None

    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None
    _valid_data_sources = []

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    def __init__(self, url="https://covid-tracker-us.herokuapp.com", data_source="jhu"):
        if Data.__instance != None:
            raise Exception("Singleton!")
        else:
            Data.__instance = self

            # Skip mirror checking if custom url was passed
            if url == Data.__instance.default_url:
                # Load mirrors
                response = requests.get(Data.__instance.mirrors_source)
                response.raise_for_status()
                Data.__instance.mirrors = response.json()

                # Try to get sources as a test
                for mirror in Data.__instance.mirrors:
                    # Set URL of mirror
                    Data.__instance.url = mirror["url"]
                    result = None
                    try:
                        result = Data._getSources()
                    except Exception as e:
                        # URL did not work, reset it and move on
                        Data.__instance.url = ""
                        continue

                    # TODO: Should have a better health-check, this is way too hacky...
                    if "jhu" in result:
                        # We found a mirror that worked just fine, let's stick with it
                        break

                    # None of the mirrors worked. Raise an error to inform the user.
                    raise RuntimeError("No available API mirror was found.")

            else:
                Data.__instance.url = url

            Data.__instance._valid_data_sources = Data._getSources()
            if data_source not in Data.__instance._valid_data_sources:
                raise ValueError("Invalid data source. Expected one of: %s" % Data.__instance._valid_data_sources)
            Data.__instance.data_source = data_source

    def Instance():
        if Data.__instance == None:
            Data()
        return Data.__instance

    @staticmethod
    def _getSources():
        response = requests.get(Data.__instance.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]

class Location(object):
    country = ""
    country_code = ""
    country_id = ""

    def __init__(self, country=None, country_code=None, country_id=None):
        if country is not None:
            self.country = country
        if country_code is not None:
            self.country_code = country_code
        if country_id is not None:
            self.country_id = country_id

    def __str__(self):
        if self.country == "" and self.country_code == "" and self.country_id == "":
            return "Warning! Invalid location provided."
        
        return "{: <25} ({}) \tid:{}".format(self.country, self.country_code, self.country_id)

class LocationGroup(object):
    locList = []

    def __init__(self, locList=None):
        if locList is not None:
            self.locList = locList


# Testing
if __name__ == '__main__':
    print(COVID19(Data()).getLocationData(LocationGroup([Location(country_code="US"), Location(country_code="CA")])))