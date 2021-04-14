from abc import ABC, abstractmethod

class I_SOURCE(object):
    """
    An interface to implement new instances of COVID19 to use within a single instance of COVID19.
    These instances can pull data from alternate sources or different back ends.
    """
    
    def __init__(self, url, data_source):
        """Create a new covid19 instance with the desired data source"""
        pass
    
    def accessAlt(self):
        """Return alternate source"""
        pass


class ABSTRACT_COUNTRIES(ABC):
    """
    An abstract class that holds a list of multiple countries. COVID19 information from each country
    can be accessed at once.
    """
    
    @abstractmethod
    def _getCountriesByCode(self, timelines = False, country_list = []):
        """Return a list of countries when given their codes"""
        pass
    
    @abstractmethod
    def _getCountriesByName(self, timelines = False, country_list = []):
        """Return a list of countries when given their names"""
        pass
    
    @abstractmethod
    def _getCountriesById(self, country_list = []):
        """Return a list of countries when given their ids"""
        pass