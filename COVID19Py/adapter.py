
from abc import ABCMeta, abstractmethod


class covidInterface(metaclass=ABCMeta):
    @abstractmethod
    def getLocation(self, arg1):
        pass

    @abstractmethod
    def getDeath(self):
        pass


class Adapter(covidInterface):
    covid19 = None
    def __init__(self, covidapp):
        self.covid19 = covidapp

    def getLocation(self,input):
        if isinstance(input, int):
           return self.covid19.getLocationById(input)
        elif isinstance(input, str) and len(input) == 2:
          return  self.covid19.getLocationByCountryCode(input)
        else:
           return self.covid19.getLocationByCountry(input)
    
    
    def getDeath(self):
        return self.covid19.getLatest()["deaths"]
    