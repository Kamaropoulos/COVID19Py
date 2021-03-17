from typing import Dict, List
import requests
import json

#class acting as an aggregate for all operations related to setting up the user's data retrieval request
class UserRequestSetup(object):
    __default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    _valid_data_sources = []

    __mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
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


    def _getSources(self):
        response = requests.get(self.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]


    #originally _request, underscore removed as it is now referred to by class COVID19DataRetrieval and requires access. Underscore indicates protected status
    def request(self, endpoint, params=None):
        if params is None:
            params = {}
        response = requests.get(self.url + endpoint, {*params, "source": self.data_source}) #fixed a syntax error (originally **)
        response.raise_for_status()
        return response.json()
   
 

#class acting as an aggregate for generalized data retrieval operations
class COVID19GeneralizedDataRetrieval(object):
    #originally variables from the class COVID19. Variables are only used in the operations contained within the COVIDDataRetrieval class, hence they were moved here
    __previousData = None
    __latestData = None


    #"constructor" method that initializes data members of the class, where applicable
    def __init__(self, userrequestsetup)
	self.userrequestsetup = userrequestsetup #enables/allows us to access methods in the UserRequestSetup class, mainly the request method


    #updates to latest data
    def _update(self, timelines):
        latest = self.getLatest()
        locations = self.getLocations(timelines)
        if self.latestData:
            self.previousData = self.latestData
        self.latestData = {
            "latest": latest,
            "locations": locations
        }

#############################
# Generalized data searches
#############################

    #get all data at once
    def getAll(self, timelines=False):
        self._update(timelines)
        return self.latestData


    #gets the latest COVID-19 case data
    def getLatest(self) -> List[Dict[str, int]]:
        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        data = self.userrequestsetup.request("/v2/latest")
        return data["latest"]


    #get the latest changes (i.e.latest deltas)
    def getLatestChanges(self):
        changes = None
        if self.previousData:
            changes = {
                "confirmed": self.latestData["latest"]["confirmed"] - self.previousData["latest"]["confirmed"], #changed from latestData to previousData
                "deaths": self.latestData["latest"]["deaths"] - self.previousData["latest"]["deaths"],		#changed from latestData to previousData
                "recovered": self.latestData["latest"]["recovered"] - self.previousData["latest"]["recovered"], #changed from latestData to previousData
            }
        else:
            changes = {
                "confirmed": 0,
                "deaths": 0,
                "recovered": 0,
            }
        return changes


    #get case data relating all locations with COVID-19 
    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        data = None
        if timelines:
            data = self.userrequestsetup.request("/v2/locations", {"timelines": str(timelines).lower()})
        else:
            data = self.userrequestsetup.request("/v2/locations")

        data = data["locations"]
        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError("Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(data, key=lambda i: i['latest'][rank_by], reverse=True)
            data = ranked
        return data


#class acting as an aggregate for country-based data retrieval operations
class COVID19CountryBasedDataRetrieval(object):

    #"constructor" method that initializes data members of the class, where applicable
    def __init__(self, userrequestsetup)
	self.userrequestsetup = userrequestsetup #enables/allows us to access methods in the UserRequestSetup class, mainly the request method

###############################
# Country-based data searches
###############################

    #get case data by method of country name
    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            data = self.userrequestsetup.request("/v2/locations", {"country": country, "timelines": str(timelines).lower()})
        else:
            data = self.userrequestsetup.request("/v2/locations", {"country": country})
        return data["locations"]


    #get case data by method of country code
    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            data = self.userrequestsetup.request("/v2/locations", {"country_code": country_code, "timelines": str(timelines).lower()})
        else:
            data = self.userrequestsetup.request("/v2/locations", {"country_code": country_code})
        return data["locations"]


    #get case data by method of country id
    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        data = self.userrequestsetup.request("/v2/locations/" + str(country_id))
        return data["location"]
