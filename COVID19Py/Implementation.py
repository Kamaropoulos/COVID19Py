from typing import Dict, List
from abc import ABC, abstractmethod

#This is the implementation interface and does all the work is done
class Get_covid_data_implementation(ABC):
    
    @abstractmethod
    def getAll(self, timelines=False):
        pass
    
    @abstractmethod
    def getLatestChanges(self) -> Dict:
        pass

    @abstractmethod
    def getLatest(self) -> List[Dict[str, int]]:
        pass

    @abstractmethod
    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        pass

    @abstractmethod
    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
        pass

    @abstractmethod
    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
        pass

    @abstractmethod
    def getLocationById(self, country_id: int):
        pass
