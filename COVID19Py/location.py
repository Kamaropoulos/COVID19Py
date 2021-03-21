from typing import Dict, List
from .getData import GetData

from .covid19 import COVID19
class Location(object):
    def __init__(self,Covid19=getData.GetData());
        self.locationObj = Covid19

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
