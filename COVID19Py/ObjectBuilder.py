from abc import ABCMeta,abstractmethod
from typing import Dict, List
import covid19
import requests
import json

"The Builder Interface"
class InterfaceBuilder(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def setURL():
        "build url"

    @staticmethod
    @abstractmethod
    def setDataSource():
        "build data source"

    @staticmethod
    @abstractmethod
    def getProduct():
        "return the final product"

"The concrete Builder"
class ObjectBuilder(InterfaceBuilder):
    
    def __init__(self):
        self.product = covid19.COVID19()
        
    def setURL(self,url):
        if url == self.product.default_url:
           
            # Load mirrors
            response = requests.get(self.product.mirrors_source)
            response.raise_for_status()
            self.product.mirrors = response.json()
            # Try to get sources as a test
            for mirror in self.product.mirrors:
                # Set URL of mirror
                self.product.url = mirror["url"]
                result = None
               
                try:
                    result = self.product._getSources()
                    
                except Exception as e:
                   
                    # URL did not work, reset it and move on
                    self.product.url = ""
                    continue

                # TODO: Should have a better health-check, this is way too hacky...
                if "jhu" in result:
                    # We found a mirror that worked just fine, let's stick with it
                    break

                # None of the mirrors worked. Raise an error to inform the user.
                raise RuntimeError("No available API mirror was found.")

        else:
            self.product.url = url
      
        return self
    
    def setDataSource(self,data_source):
       
        self.product._valid_data_sources = self.product._getSources()
        
        if data_source not in self.product._valid_data_sources:
            raise ValueError("Invalid data source. Expected one of: %s" % self._valid_data_sources)
        self.product.data_source = data_source
        
        return self
    
    def getProduct(self):
        return self.product

        
class Director:

    @staticmethod
    def constructURL(obj=ObjectBuilder(),url="https://covid-tracker-us.herokuapp.com"):
        return obj.setURL(url)
    @staticmethod
    def constructDataSource(obj=ObjectBuilder(),dataSource='jhu'):
        return obj.setDataSource(dataSource)
    @staticmethod
    def contructWholeProduct(obj=ObjectBuilder(),url="https://covid-tracker-us.herokuapp.com", dataSource='jhu'):
        return obj.setURL(url).setDataSource(dataSource).getProduct()
    
        
