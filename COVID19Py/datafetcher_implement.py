from typing import  Dict, List
import abc

class DataFetcherImplementation(metaclass=abc.ABCMeta):
    """
    This class represents the Implementor; it is also the interface for concrete implementing classes

    """

    @abc.abstractmethod
    def getAll(self, timelines=False) -> Dict:
        pass

    @abc.abstractmethod
    def getLatestChanges(self) -> Dict:
        pass

    @abc.abstractmethod
    def getLatest(self) -> List[Dict[str, int]]:
        pass

    @abc.abstractmethod
    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        pass

    @abc.abstractmethod
    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        pass

    @abc.abstractmethod
    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        pass

    @abc.abstractmethod
    def getLocationById(self, country_id: int) -> Dict:
        pass

    @abc.abstractmethod
    def update(self, timelines):
        pass