import requests

class RequestData:
    def __init__(self, entityURL_uid, data_source, params = None):
        self.url = entityURL_uid
        self.data_source = data_source
        self.params = None
        if params is None:
            self.params = params

    def requestData(self):
        """
        This method requests the based on the class's URL, data_source, and params
        :return: dictionary containing the requested data
        """
        if self.params is None:
            self.params = {}
        response = requests.get(self.url, {**self.params, "source": self.data_source})
        response.raise_for_status()
        return response.json()
