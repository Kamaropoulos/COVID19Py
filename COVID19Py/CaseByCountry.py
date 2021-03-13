from typing import Dict, List
import COVID19Py
class CaseByCountry:
    def __init__(self,Covid19Object):
        self.obj = Covid19Object
    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            data = self.obj._request("/v2/locations", {"country_code": country_code, "timelines": str(timelines).lower()})
        else:
            data = self.obj._request("/v2/locations", {"country_code": country_code})
        return data["locations"]
    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            data = self.obj._request("/v2/locations", {"country": country, "timelines": str(timelines).lower()})
        else:
            data = self.obj._request("/v2/locations", {"country": country})
        return data["locations"]

    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        data = self.obj._request("/v2/locations/" + str(country_id))
        return data["location"]



