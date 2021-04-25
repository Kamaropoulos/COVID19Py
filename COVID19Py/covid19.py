from typing import Dict, List
import requests
import json

class COVID19(object):

COVID19InfoTool retrievalTool
COVID19Data data
previousData = None
latestData = None
url = ""
data_source = ""

    def __init__(self, url, data_source):
        retrievalTool = COVID19InfoTool()
        data = COVID19Data(url, data_source)
        self.url = data.url
        self.data_source = data.data_source

    def _update(self, timelines):
        data._update(timelines)
        self.previousData = data.previousData
        self.latestData = data.latestData

    def _getSources(self):
        return retrievalTool._getSources()

    def _request(self, endpoint, params=None):
        return data._request(endpoint, params)

    def getAll(self, timelines = False):
        return data.getAll(timelines)

    def getLatestChanges(self):
        return retrievalTool.getLatestChanges(self.previousData, self.latestData)

    def getLatest(self) -> List[Dict[str, int]]:
        return retrievalTool.getLatest(self.url, self.data_source)

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        return retrievalTool.getLocations(timelines, self.url, self.data_source)

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        return retrievalTool.getLocationByCountryCode(country_code, timelines, self.url, self.data_source)

    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        return retrievalTool.getLocationByCountry(country, timelines, self.url, self.data_source)

    def getLocationById(self, country_id: int):
        return retrievalTool.getLocationById(country_id, self.url, self.data_source)



class COVID19Data(object):

    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    _valid_data_sources = []
    previousData = None
    latestData = None

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

    def getAll(self, timelines=False):
        self._update(timelines)
        return self.latestData


class COVID19InfoTool(object):

    def __init__(self):
        pass

    def _getSources(self, url):
        response = requests.get(url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]

    def _request(self, endpoint, params=None, url, data_source):
        if params is None:
            params = {}
        response = requests.get(url + endpoint, {**params, "source":data_source})
        response.raise_for_status()
        return response.json()


    def getLatestChanges(self, previousData, latestData):
        changes = None
        if previousData:
            changes = {
                "confirmed": latestData["latest"]["confirmed"] - latestData["latest"]["confirmed"],
                "deaths": latestData["latest"]["deaths"] - latestData["latest"]["deaths"],
                "recovered": latestData["latest"]["recovered"] -latestData["latest"]["recovered"],
            }
        else:
            changes = {
                "confirmed": 0,
                "deaths": 0,
                "recovered": 0,
            }
        return changes

    def getLatest(self, url, data_source) -> List[Dict[str, int]]:
        data = self._request("/v2/latest", None, url, data_source)
        return data["latest"]

    def getLocations(self, timelines=False, rank_by: str = None, url, data_source) -> List[Dict]:
        data = None
        if timelines:
            data = self._request("/v2/locations", {"timelines": str(timelines).lower()}, url, data_source)
        else:
            data = self._request("/v2/locations", None, url, data_source)

        data = data["locations"]

        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError("Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(data, key=lambda i: i['latest'][rank_by], reverse=True)
            data = ranked

        return data

    def getLocationByCountryCode(self, country_code, timelines=False, url, data_source) -> List[Dict]:
        data = None
        if timelines:
            data = self._request("/v2/locations", {"country_code": country_code, "timelines": str(timelines).lower()}, url, data_source)
        else:
            data = self._request("/v2/locations", {"country_code": country_code}, url, data_source)
        return data["locations"]

    def getLocationByCountry(self, country, timelines=False, url, data_source) -> List[Dict]:
        data = None
        if timelines:
            data = self._request("/v2/locations", {"country": country, "timelines": str(timelines).lower()}, url, data_source)
        else:
            data = self._request("/v2/locations", {"country": country}, url, data_source)
        return data["locations"]

    def getLocationById(self, country_id: int, url, data_source):
        data = self._request("/v2/locations/" + str(country_id), None, url, data_source)
        return data["location"]
