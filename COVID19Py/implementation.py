from abc import ABC,abstractmethod
from typing import Dict, List


class Implementation(ABC):

    @abstractmethod
    def getEndLatest(self):
        pass
    
    @abstractmethod
    def getEndLocations(self):
        pass
    
class ImplementationDefault(Implementation):
    url = "https://covid-tracker-us.herokuapp.com"
    def __init__(self,data_source="jhu"):
        self.data_source = data_source

    def getEndLatest(self):
        return "/v2/latest"

    def getEndLocations(self):
        return "/v2/locations"


class ImplementationMirror(Implementation):
    url = "https://cvtapi.nl"
    def __init__(self,data_source="jhu"):
        self.data_source = data_source

    def getEndLatest(self):
        return "/v2/latest"

    def getEndLocations(self):
        return "/v2/locations"


class ImplementationMirror1(Implementation):
    url = "http://covid19-api.kamaropoulos.com"
    def __init__(self,data_source="jhu"):
        self.data_source = data_source

    def getEndLatest(self):
        return "/v2/latest"

    def getEndLocations(self):
        return "/v2/locations"
