import requests


class DataClass:
    url = ""
    data_s = ""

    # These are the 2 main component of a data class, the back-end API url and data_s is the type of source being used
    def __init__(self, url, data_s):
        self.url = url
        self.data_s = data_s

    def _request(self, endpoint, params=None):
        if params is None:
            params = {}

        response = requests.get(self.url + endpoint, {**params, "source": self.data_source})
        response.raise_for_status()

        return response.json()

    def getSources(self):
        response = requests.get(self.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]
