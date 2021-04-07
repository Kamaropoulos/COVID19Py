from abc import ABCMeta, abstractmethod

class AbstractCoronavirus(metaclass=ABCMeta):

        @abstractmethod
        def _update():
            pass
        @abstractmethod
        def _getSources():
            pass
        @abstractmethod
        def _request():
            pass
        @abstractmethod
        def getAll():
            pass
        @abstractmethod
        def getLatestChanges():
            pass
        @abstractmethod
        def getLatest():
            pass
        @abstractmethod
        def getLocations():
            pass
        @abstractmethod
        def getLocationByCountryCode():
            pass
        @abstractmethod
        def getLocationByCountry():
            pass
        @abstractmethod
        def getLocationById():
            pass
