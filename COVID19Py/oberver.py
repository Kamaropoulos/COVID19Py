from abc import ABC, abstractmethod
from typing import List
from .covid19 import COVID19
class Subject(ABC):
    """
    Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
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

class ConcreteCovidGetLatest(Subject):
    _getLatest = None

    _observers = []


    def attach(self,observer: Observer) -> None:
        self._observers.append(observer)

    def detach(observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for i in _observers:
            i.update(self)
    def getLatest(self):
        self._getLatest = COVID19().getLatest()
        self.notify()

class Observer(ABC):
    """
    Observer interface
    """
    @abstractmethod
    def update(self,subject:Subject) -> None:
        pass


class ConcreteObserver(Observer):
    data = None
    def update(self,subject:Subject) -> None:
        self.data = subject._getLatest 