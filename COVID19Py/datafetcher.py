from typing import List, Dict

class DataFetcher:
    """
    This class represents the abstraction interface for the Bridge Pattern.
    The class holds the reference to the `Implementor` and performs necessary operations via that reference.

    """


    def __init__(self, reference):
        self._implementorRef = reference

    def getAll(self, timelines=False) -> Dict:
        """
        This method calls upon the implementor's reference to returns all the data associated with COVID19, as per the Package's specifications.

        :param timelines: bool: value that represents the choice of user to receiver or not to receive data with corresponding timelime.
        :return: dictionary containing the data
        """
        return self._implementorRef.getAll(timelines=timelines)

    def getLatestChanges(self) -> Dict:
        """
        This method calls upon the implementor's reference to return a dictionary containing the changes that have happened since the last call of `getAll()`

        :return: dict[str, int]: containing the numbers pertaining to the changes.
        """
        return self._implementorRef.getLatestChanges()

    def getLatest(self) -> List[Dict[str, int]]:
        """
        This method calls upon the implementor's reference to return the latest amount of total confirmed cases, deaths, and recoveries.

        :return: List[Dict[str, int]]
        """
        return self._implementorRef.getLatest()

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        This method calls upon the implementor's reference and gets all locations affected by COVID-19, as well as latest case data.

        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        return self._implementorRef.getLocations(timelines=timelines, rank_by=rank_by)

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        """
        This method calls upon the implementor's reference and returns the data associated with `country_code` country.

        :param country_code: String denoting the ISO 3166-1 alpha-2 code (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country_code. If the country_code is invalid, it returns an empty list.
        """
        return self._implementorRef.getLocationByCountryCode(country_code=country_code, timelines=timelines)

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        This method calls upon the implementor's reference and returns the data associated with `country` country.

        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        return self._implementorRef.getLocationByCountry(country=country, timelines=timelines)

    def getLocationById(self, country_id: int) -> Dict:
        """
        This method calls upon the implementor's reference and returns the data associated with `country_id` country

        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        return self._implementorRef.getLocationById(country_id=country_id)