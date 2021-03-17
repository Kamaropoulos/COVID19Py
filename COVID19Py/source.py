import requests
import json


class Source(object):

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    
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
                if self.data_source in result:
                    
                    if requests.get(self.url,{"source":self.data_source}).status_code == 200:
                        break
                    
                    #check if last element in mirror then check if the mirror is functiontion 
                    if mirror == self.mirrors[-1] and requests.get(self.url,{"source":self.data_source}).status_code != 200:
                        #None of the mirrors worked. Raise an error to inform the user.
                        raise RuntimeError("No available API mirror was found.")

            except Exception as e:
                raise e
          



    def _getSources(self):
        response = requests.get(self.url + "/v2/sources")
        if response.status_code == 200:
            return response.json()['sources']
        else:
            return []

    def getUrl(self):
        return self.url
    