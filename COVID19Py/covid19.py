from typing import Dict, List
import requests
import json
from covidInterfaces import I_SOURCE, ABSTRACT_COUNTRIES

class COVID19(object):
    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None
    _valid_data_sources = []
    """Stores a dictionary of COUNTRIES which the user can access through a name to request covid19 stats"""
    _country_lists = {}

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
        response = requests.get(self.url + endpoint, {**params, "source":self.data_source})
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

    def getMultipleCountries(self, name, timelines = False):
        """
        :param name: A unique identifier for a COUNTRIES entity.
        :return: The covid19 information for a COUNTRIES entitiy denoted by name, else an empty list
        """
        if self._country_lists.get(name) == None:
            return []
        else:
            return self._country_lists.get(name).getCountries(timelines)
    
    def createCountryList(self, name, url = "https://covid-tracker-us.herokuapp.com", data_source = "jhu", countries = [], typeCall = -1):
        """
        :param name: A unique identifier for a COUNTRIES entity.
        :param url and data_source: The backend and data source you want a list of countries to use when
        getting information.
        :param countries: a list of countries you wish to get covid19 information on all at once.
        :param typeCall: This indicates the format countries are stored in. If the code does not match 
        the format when retreiving data an error will be thrown by the back end. The codes are as follows
        0 = Countries indicated by code
        1 = Countries indicated by name
        2 = Countries indicated by id
        -1 = no code provided. Will not call back end and will always produce an empty list.
        :return: An instance of COUNTRIES
        """
        if self._country_lists.get(name) == None:
            self._country_lists[name] = COUNTRIES(ALT_SOURCE(url, data_source), typeCall, countries)
            return self._country_lists.get(name).getCountries()
        else:
            self._country_lists.update({name: COUNTRIES(ALT_SOURCE(url, data_source), typeCall, countries)})
            return self._country_lists.get(name).getCountries()
        
    
class COUNTRIES(ABSTRACT_COUNTRIES, object):
    
    country_list = []
    source = None
    typeCall = -1
    
    def __init__(self,source: I_SOURCE, typeCall = -1, country_list = []):
        """
        We assume if no typeCall is passed then country_list is not specified or in inconcistent state,
        so we set it to -1 by default. When getCountries is called an empty list will be returned.
        """
        self.source = source
        self.typeCall = typeCall
        self.country_list = country_list
        
    def getCountries(self, timelines = False):
        """
        :param timelines: Will return timelines if true, else false
        :return: the covid19 information on the countries in country_list 
        """
        if self.typeCall == 0:
            return self._getCountriesByCode(timelines)
        elif self.typeCall == 1:
            return self._getCountriesByName(timelines)
        elif self.typeCall == 2:
            return self._getCountriesById()
        else:
            return []
    
    def accessList(self):
        """
        :return: A list with the first indec storing the type of country list
        with the remaining countries in country_list appended to it
        """
        countries = []
        countries.append(self.typeCall)
        countries.append(self.country_list)
        return countries
        
    
    def _getCountriesByCode(self, timelines = False):
        """Return a list of countries when given their codes"""
        countryStats = []

        for code in self.country_list:
            countryStats.append(self.source.accessAlt().getLocationByCountryCode(code, timelines))
        
        return countryStats
            
      
    def _getCountriesByName(self, timelines = False):
        """Return a list of countries when given their names"""
        countryStats = []

        for name in self.country_list:
            countryStats.append(self.source.accessAlt().getLocationByCountry(name, timelines))
        
        return countryStats
    
    def _getCountriesById(self):
        """Return a list of countries when given their ids"""
        countryStats = []

        for i in self.country_list:
            countryStats.append(self.source.accessAlt().getLocationById(i))
        
        return countryStats


class ALT_SOURCE(I_SOURCE, object):
    url = ""
    data_source = ""
    covid19_obj = None
    
    def __init__(self, url = "https://covid-tracker-us.herokuapp.com", data_source = "jhu"):
        """Create a new covid19 instance with the desired data source"""
        self.covid19_obj = COVID19(url, data_source)
        self.url = self.covid19_obj.url 
        self.data_source = self.covid19_obj.data_source
    
    def accessAlt(self):
        """Return alternate source"""
        return self.covid19_obj