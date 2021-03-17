from typing import List, Dict

from .sources import Reterivedata


class Location:
    def __init__(self, url, data_source):
        self.url = url
        self.data_source = data_source

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        data = None
        if timelines:
            retrieve = Reterivedata(self.url, self.data_source, "/v2/locations",
                                    {"timelines": str(timelines).lower()})
            data = retrieve.retreive()
        else:
            retrieve = Reterivedata(self.url, self.data_source, "/v2/locations")
            data = retrieve.retreive()

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
            retrieve = Reterivedata(self.url, self.data_source, "/v2/locations",
                                    {"country_code": country_code, "timelines": str(timelines).lower()})
            data = retrieve.retreive()
        else:
            retrieve = Reterivedata(self.url, self.data_source, "/v2/locations",
                                    {"country_code": country_code})
            data = retrieve.retreive()

        return data["locations"]

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        data = None
        if timelines:
            retrieve = Reterivedata(self.url, self.data_source, "/v2/locations",
                                    {"country": country, "timelines": str(timelines).lower()})
            data = retrieve.retreive()
        else:
            retrieve = Reterivedata(self.url, self.data_source, "/v2/locations",
                                    {"country": country})
            data = retrieve.retreive()
        return data["locations"]

    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        retrieve = Reterivedata(self.url, self.data_source, "/v2/locations/" + str(country_id))
        data = retrieve.retreive()
        return data["location"]
