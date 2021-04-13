from abc import ABCMeta, abstractmethod, classmethod


class ICOVID19(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def create_object():
        "Abstract Interface method"

    @classmethod
    @abstractmethod
    def _update(self,timelines):
        "Update"

    @classmethod
    @abstractmethod
    def _getSources(self):
        "_getSources"

    @classmethod
    @abstractmethod
    def _request(self,endpoint,params=None):
        "_getRequest"

    @classmethod
    @abstractmethod
    def getAll(self,timelines=False):
        "getAll"
    
    @classmethod
    @abstractmethod
    def getLatestChanges(self):
        "getLatestChanges"

    @classmethod
    @abstractmethod
    def getLatest(self):
        "getLatestChanges"
    
    @classmethod
    @abstractmethod
    def getLocations(self, timelines=False, rank_by: str = None):
        "getLocations"
    
       
    @classmethod
    @abstractmethod
    def getLocations(self, timelines=False, rank_by: str = None):
        "getLocations"
    
    @classmethod
    @abstractmethod
    def getLocationByCountry(self, country, timelines=False):
        "getLocationByCountry"
    
    @classmethod
    @abstractmethod
    def getLocationById(self,country_id):
        "getLocationById"

class ConcreteAPIDefault(ICOVID19):
    