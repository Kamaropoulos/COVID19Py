from abc import ABC,abstractmethod
from typing import Dict, List


class Implementation(ABC):

    @staticmethod
    @abstractmethod
    def getEndLatest(self):
        pass
    
    @staticmethod
    @abstractmethod
    def getEndLocations(self):
        pass
    
class COVID19Implementation(Implementation):

    def __init__(self,url,data_source="jhu"):
        self.url = url
        self.data_source = data_source

    @staticmethod
    def getEndLatest(self):
        return "/v2/latest"

    @staticmethod
    def getEndLocations(self):
        return "/v2/locations"
