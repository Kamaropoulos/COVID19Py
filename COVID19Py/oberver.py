from abc import ABC, abstractmethod
from typing import List

class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
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

