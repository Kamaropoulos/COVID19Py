from typing import Dict, List
import requests
import json # -------------------------- THIS IS THE PART OF STRUCTURAL(ADAPTER PATTERN) CODE --------------------------
            # WE HAVE IMPORTED THIS JSON BECAUSE WE NEED TO DISPLAY THE OUTPUT IN FORM OF JSON, BECAUSE THE DATA IN THE
            # DATASOURCE IS IN XML FILE AND WE CANNOT DIRECTLY SHOW THE OUTPUT IN XML FORMAT, SO IT WILL BE EASY TO DISPLAY
            # THE OUTPUT IN JSON (LIST OF DICTIONARY FORMAT) THERE FORE WE HAVE THIS


# class COVID19 is defined , to store definition of each methods used
class COVID19(object):
    # print("inside class")
    # we have taken this link as default url
    default_url = "https://covid-tracker-us.herokuapp.com"

    # an empty string url is taken
    url = ""

    # an empty string datasource is taken
    data_source = ""

    # previous data is initialized as None
    previousData = None

    # latest data is initialized as None
    latestData = None

    # list _valid_data_sources is defined and kept empty initially
    _valid_data_sources = []

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    # ------------ A FACTORY METHOD IS DEFINED (THAT COMES UNDER CREATIONAL (FACTORY ) DESIGN PATTERN) ----------------------------
    # THIS METHOD IS USED WHEN WE WANT TO ADD NEW FUNCTION FOR EXTRACTIING DATA IN NEW FORMAT, THEN WE CAN JUST ADD THAT FUNCTION
    # TO THIS FACTORY METHOD AND SIMPLY DEFINE THE FUNCTION WITHOUT ALTERING THE OTHER FUNCTION OF THE CODE --------------------
    def factory(self):
        localizer = {
            "stateCode" : fromStateCode,
            "countryCode": fromCountryCode,
            "districtCode": fromDistrictCode,
            "districtID" : fromDistrictID,
            "stateID": fromStateID,
            "countryID": fromCountryID,
        }
    # ------------------------------------------------------------------------------------------------------------------

    # ======================================================================================================================
    # __init__ method is defined which is considered to be the constructor of the class COVID19
    def __init__(self, url="https://covid-tracker-us.herokuapp.com", data_source='csbs'):

        # print("inside __init__")
        # if url we passed through is same as the default url, we will not check mirror
        if url == self.default_url:
            # print("if")
            # we directly load the mirrors
            response = requests.get(self.mirrors_source)
            response.raise_for_status()
            self.mirrors = response.json()

            # Try to get sources as a test
            for mirror in self.mirrors:
                # print("mirror for loop")
                # Set URL of mirror
                self.url = mirror["url"]
                result = None
                try:
                    result = self.fromSources()
                except Exception as e:
                    # URL did not work, reset it and move on
                    self.url = ""
                    continue

                if "csbs" in result:
                    # print("jhu in result")
                    break

                # Raise the RuntimeError when no mirror worked
                raise RuntimeError("No available API mirror was found.")

        else:
            # print("print else")
            self.url = url

        self._valid_data_sources = self.fromSources()
        if data_source not in self._valid_data_sources:
            # print("if not in")
            raise ValueError("Invalid data source. Expected one of: %s" % self._valid_data_sources)
        self.data_source = data_source

    # ======================================================================================================================
    # function new1 defined in such a way so that we can check if there is anything new happened
    def new1(self, timelines):
        # print("update")
        latest = self.fromlat()
        locations = self.fromloc(timelines)
        if self.latestData:
            self.previousData = self.latestData
        self.latestData = { # -------------- THIS IS HOW THE LATEST DATA IS VISIBLE USING JSON CODE FORMAT
                            # THIS IS ALSO THE PART OF STRUCTURAL(ADAPTER METHOD) ---------------------
            "latest": latest,
            "locations": locations
        }

    # ======================================================================================================================
    # function fromSources defined to get the sources
    def fromSources(self):
        # print("fromSources")
        response = requests.get(self.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]

    # ======================================================================================================================
    # function permission defined to take the permission
    def permission(self, endpoint, params=None):
        # print("permission")
        if params is None:
            params = {}
        response = requests.get(self.url + endpoint, {**params, "source": self.data_source})
        response.raise_for_status()
        return response.json()

    # ======================================================================================================================
    # function get1 defined to get all the data
    def get1(self, timelines=False):
        # print("get1")
        self.new1(timelines)
        return self.latestData # THIS LATESTDATA IS RETURN IN FORM OF JSON FORMAT -------------------------

    # ======================================================================================================================
    # function defined to check for changes
    def fromChanges(self):
        # print("fromChanges")
        changes = None
        if self.previousData:
            # print("latest changes if")
            changes = { "confirmed": self.latestData["latest"]["confirmed"] - self.latestData["latest"]["confirmed"], "deaths": self.latestData["latest"]["deaths"] - self.latestData["latest"]["deaths"], "recovered": self.latestData["latest"]["recovered"] - self.latestData["latest"]["recovered"], }
        else:
            # print("latest changes else")
            changes = { "confirmed": 0, "deaths": 0, "recovered": 0, }
        return changes

    # ======================================================================================================================
    def fromlat(self) -> List[Dict[str, int]]:
        # print("fromlat")
        data = self.permission("/v2/latest")
        return data["latest"]

    # ======================================================================================================================
    # function fromloc defined to get from the location
    def fromloc(self, timelines=False, rank_by: str = None) -> List[Dict]:
        # print("fromloc")

        data = None
        if timelines:
            data = self.permission("/v2/locations", {"timelines": str(timelines).lower()})
        else:
            data = self.permission("/v2/locations")

        data = data["locations"]

        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError("Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(data, key=lambda i: i['latest'][rank_by], reverse=True)
            data = ranked

        return data

    # ======================================================================================================================
    # implemented to get data with the help of districtcode
    def fromDistrictCode(self, district_code, timelines=False) -> List[Dict]:
        # print("fromDistrictCode")

        data = None
        if timelines:
            data = self.permission("/v2/locations", {"district_code": district_code, "timelines": str(timelines).lower()})
        else:
            data = self.permission("/v2/locations", {"district_code": district_code})
        return data["locations"]

    # ======================================================================================================================
    # implemented to get data with the help of statecode
    def fromStateCode(self, state_code, timelines=False) -> List[Dict]:
        # print("fromStateCode")

        data = None
        if timelines:
            data = self.permission("/v2/locations", {"state_code": state_code, "timelines": str(timelines).lower()})
        else:
            data = self.permission("/v2/locations", {"state_code": state_code})
        return data["locations"]

    # factory("stateCode")
    # ======================================================================================================================
    # implemented to get data with the help of countrycode
    def fromCountryCode(self, country_code, timelines=False) -> List[Dict]:
        # print("fromCountryCode")

        data = None
        if timelines:
            data = self.permission("/v2/locations", {"country_code": country_code, "timelines": str(timelines).lower()})
        else:
            data = self.permission("/v2/locations", {"country_code": country_code})
        return data["locations"]

    # ======================================================================================================================
    # implemented to get data with the help of country
    def fromCountry(self, country, timelines=False) -> List[Dict]:
        # print("fromCountry")

        data = None
        if timelines:
            data = self.permission("/v2/locations", {"country": country, "timelines": str(timelines).lower()})
        else:
            data = self.permission("/v2/locations", {"country": country})
        return data["locations"]

    # ======================================================================================================================
    # implemented to get data with the help of country
    def fromState(self, state, timelines=False) -> List[Dict]:
        # print("fromCountry")

        data = None
        if timelines:
            data = self.permission("/v2/locations", {"state": state, "timelines": str(timelines).lower()})
        else:
            data = self.permission("/v2/locations", {"state": state})
        return data["locations"]

    # ======================================================================================================================
    # implemented to get data with the help of country
    def fromDistrict(self, district, timelines=False) -> List[Dict]:
        # print("fromCountry")

        data = None
        if timelines:
            data = self.permission("/v2/locations", {"district": district, "timelines": str(timelines).lower()})
        else:
            data = self.permission("/v2/locations", {"district": district})
        return data["locations"]

    # ======================================================================================================================
    # implemented to get data with the help of Country id
    def fromCountryId(self, country_id: int):
        # print("fromCountryId")

        data = self.permission("/v2/locations/" + str(country_id))
        return data["location"]

    # ======================================================================================================================
    # implemented to get data with the help of State id
    def fromStateId(self, state_id: int):
        # print("fromStateId")

        data = self.permission("/v2/locations/" + str(state_id))
        return data["location"]

    # ======================================================================================================================
    # implemented to get data with the help of District id
    def fromDistrictId(self, district_id: int):
        # print("fromDistrictId")

        data = self.permission("/v2/locations/" + str(state_id))
        return data["location"]
