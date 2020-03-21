import requests

class COVID19():
    url = ""
    previousData = None
    latestData = None

    def __init__(self, url="https://coronavirus-tracker-api.herokuapp.com"):
        self.url = url

    def _update(self, timelines):
        latest = self.getLatest()
        locations = self.getLocations(timelines)
        if self.latestData:
            self.previousData = self.latestData
        self.latestData = {
            "latest":latest,
            "locations":locations
        }

    def _request(self, endpoint, params=None):
        response = requests.get(self.url + endpoint, params)
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

    def getLatest(self):
        data = self._request("/v2/latest")
        return data["latest"]
    
    def getLocations(self, timelines=False, rank_by=None):
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

            ranked = sorted(data, key = lambda i: i['latest'][rank_by],reverse=True)
            data = ranked

        return data

    def getLocationByCountryCode(self, country_code, timelines=False):
        data = None
        if timelines:
            data = self._request("/v2/locations", {"country_code": country_code, "timelines": str(timelines).lower()})
        else:
            data = self._request("/v2/locations", {"country_code": country_code})
        return data["locations"]

    def getLocationById(self, id):
        data = self._request("/v2/locations/" + str(id))
        return data["location"]
