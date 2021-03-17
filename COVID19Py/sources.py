import requests


class Reterivedata:
    def __init__(self, url, data_source, endpoint, params=None):
        self.url = url
        self.data_source = data_source
        self.endpoint = endpoint
        self.params = params if params else None

    def retreive(self):
        if self.params is None:
            self.params = {}
        response = requests.get(self.url + self.endpoint, {**self.params, "source": self.data_source})
        response.raise_for_status()
        return response.json()

    def getSources(self):
        response = requests.get(self.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]
