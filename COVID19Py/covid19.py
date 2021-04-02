from .requestdata import RequestData
from .datafetcher_implement import DataFetcherImplementation
from typing import Dict, List
from contracts import contract
import requests


class COVID19(DataFetcherImplementation):
    """
    This class represents the concrete implementing class, that implements `DataFetcherImplementation` interface.
    """
    _requestURL = ""
    _default_url = "https://covid-tracker-us.herokuapp.com"
    _url = ""
    _data_source = ""
    _previousData = None
    _latestData = None
    _valid_data_sources = []
    _default_source_name = "jhu"
    _mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    _mirrors = None

    def __init__(self, url=_default_url, data_source=_default_source_name):
        # Skip mirror checking if custom url was passed
        if url == self._default_url:
            # Load mirrors
            response = requests.get(self._mirrors_source)
            response.raise_for_status()
            self._mirrors = response.json()

            # Try to get sources as a test
            for mirror in self._mirrors:
                # Set URL of mirror
                self._url = mirror["url"]
                result = None
                try:
                    requestData = RequestData(requestURL=self._url + "/v2/sources", data_source=self._data_source)
                    result = requestData.getSources()
                except Exception as e:
                    # URL did not work, reset it and move on
                    self._url = ""
                    continue

                # TODO: Should have a better health-check, this is way too hacky...
                if self._default_source_name in result:
                    # We found a mirror that worked just fine, let's stick with it
                    break

                # None of the mirrors worked. Raise an error to inform the user.
                raise RuntimeError("No available API mirror was found.")

        else:
            self._url = url

        requestData = RequestData(requestURL=self._url + "/v2/sources", data_source=self._data_source)
        self._valid_data_sources = requestData.getSources()
        if data_source not in self._valid_data_sources:
            raise ValueError("Invalid data source. Expected one of: %s" % self._valid_data_sources)
        self._data_source = data_source

    @contract(timelines='bool')
    def update(self, timelines):
        """
        This function updates the `latestData` variable by setting it to the up-to-data data fetched from the source.
        It also updates the `previousData`, if there was a `latestData` that previously existed.

        :param timelines: bool: value that represents the choice of user to receiver or not to receive data with corresponding timelime.

        """
        latest = self.getLatest()
        locations = self.getLocations(timelines)
        if self._latestData:
            self._previousData = self._latestData
        self._latestData = {
            "latest": latest,
            "locations": locations
        }

    @contract(timelines='bool', returns='dict(str:*)')
    def getAll(self, timelines=False):
        """
        This method returns all the data associated with COVID19, as per the Package's specifications.

        :param timelines: bool: value that represents the choice of user to receiver or not to receive data with corresponding timelime.
        :return: dictionary containing the data
        """
        self.update(timelines)
        return self._latestData

    @contract(returns='dict(str:int)')
    def getLatestChanges(self):
        """
        This function returns a dictionary containing the changes that have happened since the last call of `getAll()`
        :return: dict[str, int]: containing the numbers pertaining to the changes.
        """
        changes = None
        if self._previousData:
            changes = {
                "confirmed": self._latestData["latest"]["confirmed"] - self._latestData["latest"]["confirmed"],
                "deaths": self._latestData["latest"]["deaths"] - self._latestData["latest"]["deaths"],
                "recovered": self._latestData["latest"]["recovered"] - self._latestData["latest"]["recovered"],
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
        self._requestURL = self._url + "/v2/latest"
        requestData = RequestData(requestURL=self._requestURL,
                                  data_source=self._data_source,
                                  params=None
                                  )
        data = requestData.requestData()
        return data["latest"]

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        data = None
        self._requestURL = self._url + "/v2/locations"
        if timelines:
            endpoint_params = {"timelines": str(timelines).lower()}

            # Make request calling on the RequestData Value-object: separation of objects for consistency.
            requestData = RequestData(requestURL=self._requestURL,
                                      data_source=self._data_source,
                                      params=endpoint_params
                                      )
            data = requestData.requestData()
        else:
            requestData = RequestData(requestURL=self._requestURL,
                                      data_source=self._data_source,
                                      params=None
                                      )
            data = requestData.requestData()

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
        self._requestURL = self._url + "/v2/locations"
        if timelines:
            endpoint_params = {"country_code": country_code, "timelines": str(timelines).lower()}
            requestData = RequestData(requestURL=self._requestURL,
                                      data_source=self._data_source,
                                      params=endpoint_params
                                      )
            data = requestData.requestData()
        else:
            endpoint_params = {"country_code": country_code}
            requestData = RequestData(requestURL=self._requestURL,
                                      data_source=self._data_source,
                                      params=endpoint_params
                                      )
            data = requestData.requestData()
        return data["locations"]

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        """
        :param country: String denoting name of the country
        :param timelines: Whether timeline information should be returned as well.
        :return: A list of areas that correspond to the country name. If the country is invalid, it returns an empty list.
        """
        data = None
        self._requestURL = self._url + "/v2/locations"
        if timelines:
            endpoint_params = {"country": country, "timelines": str(timelines).lower()}
            requestData = RequestData(requestURL=self._requestURL,
                                      data_source=self._data_source,
                                      params=endpoint_params
                                      )
            data = requestData.requestData()
        else:
            endpoint_params = {"country": country}
            requestData = RequestData(requestURL=self._requestURL,
                                      data_source=self._data_source,
                                      params=endpoint_params
                                      )
            data = requestData.requestData()
        return data["locations"]

    @contract(country_id=int, returns='dict(str:*)')
    def getLocationById(self, country_id: int):
        """
        :param country_id: Country Id, an int
        :return: A dictionary with case information for the specified location.
        """
        self._requestURL = self._url + "/v2/locations/" + str(country_id)
        requestData = RequestData(requestURL=self._requestURL,
                                  data_source=self._data_source,
                                  params=None
                                  )
        data = requestData.requestData()
        return data["location"]
