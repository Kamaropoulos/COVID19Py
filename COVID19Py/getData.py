from typing import Dict, List
from .covid19 import COVID19


class GetData(object):

    default_url = "https://covid-tracker-us.herokuapp.com"

    def __init__(self, url=default_url, data_source='jhu'):
      self.url = url
      self.data_source = data_source
      self.obj = COVID19(self.url, self.data_source)

    def getAll(self, timelines=False):
        """
        :param timelines: Whether timeline information should be returned as well.
        :return: all Covid data numbers from around the world 
        """
       self.obj.getAll(timelines=timelines)


    def getLatestChanges(self):
          """
        :return: The difference between the current and the previously fetched covid numbers.
        """
        return self.obj.getLatestChanges()

    def getLatest(self) -> List[Dict[str, int]]:
          """
        :return: The latest total confirmed,deaths and recovered case numbers.
        """
        return self.obj.getLatest()

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
         """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        return self.obj.getLocations(timelines=timelines, rank_by=rank_by)
       

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        country_code = country_code
        return self.obj.getLocationByCountryCode(country_code=country_code, timelines=timelines)

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
    
        return self.obj.getLocationByCountry(country_code=country_code, timelines=timelines)

    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
   
        return self.obj.getLocationById(country_id=country_id)
