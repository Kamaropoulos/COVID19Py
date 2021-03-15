from typing import Dict, List
import COVID19Py
#aggregate OverViewOfCovid19
class OverViewOfCovid19:
    def __init__(self,Covid19Object):
        self.obj = Covid19Object

    def getAll(self, timelines=False):
        self.obj._update(timelines)
        return self.obj.latestData

    def getLatestChanges(self):
        changes = None
        if self.obj.previousData:
            changes = {
                "confirmed": self.obj.latestData["latest"]["confirmed"] - self.obj.latestData["latest"]["confirmed"],
                "deaths": self.obj.latestData["latest"]["deaths"] - self.obj.latestData["latest"]["deaths"],
                "recovered": self.obj.latestData["latest"]["recovered"] - self.obj.latestData["latest"]["recovered"],
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
        data = self.obj._request("/v2/latest")
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
            data = self.obj._request("/v2/locations", {"timelines": str(timelines).lower()})
        else:
            data = self.obj._request("/v2/locations")

        data = data["locations"]
        
        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError("Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(data, key=lambda i: i['latest'][rank_by], reverse=True)
            data = ranked

        return data


