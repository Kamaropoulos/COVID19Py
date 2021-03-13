from typing import Dict, List
class Country:
    def __init__(self,Covid19Object,countryName='',countryCode='',countryId=0):
        self.obj = Covid19Object
        self.name = countryName
        self.code = countryCode
        self.id = countryId
    
    def populationByName(self) -> List[Dict]:
        data = None
        data = self.obj._request("/v2/locations", {"country": self.name})
        return data["country_population"]
    def coordinatesByName(self) -> List[Dict]:
        data = None
        data = self.obj._request("/v2/locations", {"country": self.name})
        return data["country_population"]


