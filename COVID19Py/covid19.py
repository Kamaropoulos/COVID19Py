from abc import ABCMeta, abstractmethod
from Concrete import ConcreteAPIDefault,ConcreteAPIMirror
from enum import Enum

class Source(Enum):
    Default = 1
    Mirror = 2

class COVID19:

    @staticmethod
    def create_object(mirror:int,data_source:str="jhu"):
        if mirror == Source.Default:
            return ConcreteAPIDefault(data_source)        
        if mirror == Source.Mirror:
            return ConcreteAPIMirror(data_source)