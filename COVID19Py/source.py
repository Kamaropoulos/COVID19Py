import requests
import json


class Source(object):

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    
    data_source = None
    def __init__ (self,url,data_source):
        self.url = url
        self.data_source = data_source
        
        response = requests.get(self.mirrors_source)
        response.raise_for_status()
        self.mirrors = response.json()
    

        for mirror in self.mirrors:
            # Set URL of mirror
            self.url = mirror["url"]
            result = None
            try:
                result = self._getSources()
                print(result)
                if "jhu" in result:
                    # We found a mirror that worked just fine, let's stick with it
                    break
            except Exception as e:
                # URL did not work, reset it and move on
                self.url = ""
                continue
                # None of the mirrors worked. Raise an error to inform the user.
                raise RuntimeError("No available API mirror was found.")
          



    def _getSources(self):
        response = requests.get(self.url + "/v2/sources")
        response.raise_for_status()
        return response.json()['sources']

    def getUrl(self):
        return self.url
    