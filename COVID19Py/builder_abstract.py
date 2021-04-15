from typing import Dict, List
from .Implementation import Get_covid_data_implementation

#This is the absraction interface part and maintains refrence to the implementation part where all the work is done
class Get_covid_data:

    def __init__(self, implementation: Get_covid_data_implementation) -> None:
        #reference to implementation
        self.implementation = implementation

    def getAll(self, timelines=False):
        
        return self.implementation.getAll(timelines=timelines)

    def getLatestChanges(self) -> Dict:
    
        return self.implementation.getLatestChanges()

    def getLatest(self) -> List[Dict[str, int]]:
        
        return self.implementation.getLatest()

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
       
        return self.implementation.getLocations(timelines=timelines, rank_by=rank_by)

    def getLocationByCountryCode(self, country_code, timelines=False) -> List[Dict]:
       
        return self.implementation.getLocationByCountryCode(country_code=country_code, timelines=timelines)
    
    def getLocationByCountry(self, country, timelines=False) -> List[Dict]:
       
        return self.implementation.getLocationByCountry(country=country, timelines=timelines)

    def getLocationById(self, country_id: int):

        return self.implementation.getLocationById(country_id=country_id)
        
