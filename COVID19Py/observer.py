from abc import ABC, abstractmethod
from typing import List
from covid19 import COVID19


class IObserver(ABC):
    """
    Observer interface
    """
    @abstractmethod
    def update(self,subject) -> None:
        pass


class Subject(ABC):
    """
    Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: IObserver) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: IObserver) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass

class ConcreteCovidGetLocation(Subject):
    _getLocation = None

    _observers = []


    def attach(self,observer: IObserver) -> None:
        self._observers.append(observer)

    def detach(observer: IObserver) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for i in self._observers:
            i.update(self)
    def getLocationByCountry(self,country: str,timeline=False):
        self._getLocation = COVID19().getLocationByCountry(country,timeline)
        self.notify()



class ConcreteObserver(IObserver):
    data = None
    def update(self,subject:Subject) -> None:
        self.data = subject._getLocation 