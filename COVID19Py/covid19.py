from typing import Dict, List
from .getData import GetData

class COVID19(object):

    default_url = "https://covid-tracker-us.herokuapp.com"

    def __init__(self, url=default_url, data_source='jhu'):
      self.url = url
      self.data_source = data_source
      self.obj = GetData(self.url, self.data_source)

    def getAll(self, timelines=False):
        """
        :param timelines: Whether timeline information should be returned as well
        :return: all Covid data numbers from around the world.
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
       
