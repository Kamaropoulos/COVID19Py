import requests

class RequestData:
    def __init__(self, requestURL, data_source, params = None):
        self._url = requestURL
        self._data_source = data_source
        self._params = None
        if params is None:
            self._params = params

    def requestData(self):
        """
        This method requests the based on the class's URL, data_source, and params
        :return: dictionary containing the requested data
        """
        if self._params is None:
            self._params = {}
        response = requests.get(self._url, {**self._params, "source": self._data_source})
        response.raise_for_status()
        return response.json()

    def getSources(self):
        """
        :return: 
        """
        response = requests.get(self._url)
        response.raise_for_status()
        return response.json()["sources"]
