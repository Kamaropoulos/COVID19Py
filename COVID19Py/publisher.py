class GenericPublisher:
    """
    This class represents a generic publisher with add, remove and notify functions
    """

    def __init__(self):
        self.observerList = []

    def addNewObserver(self, observer):
        """
        This methods adds a new observer `observer` to the list of observers

        :param observer: observer to add to the list
        :return:None
        """
        if observer not in self.observerList:
            self.observerList.append(observer)
        else:
            # Already in this list, pass
            pass

    def removeObserver(self, observer):
        """
        This method removes an observer from the list of observers

        :param observer: Observer to remove
        :return: None
        """
        try:
            self.observerList.remove(observer)
        except Exception:
            raise Exception("observer not in the list")

    def notifyObservers(self):
        """
        This method notifies all the observers in the list of observers about a change to the publisher.
        :return: None
        """
        [currObserver.notifyObservers(self) for currObserver in self.observerList]


class LatestDataPublisher(GenericPublisher):
    """
    This class represents `latestData` publisher
    """

    def __init__(self):
        GenericPublisher.__init__(self)
        self.latestData = None
        self.latestDataCopy = None

    def set_latestData(self, newData):
        """
        This setter function sets the value of `latestData` to `newData`
        :param newData: new value to set `latestData` to.
        :return: None
        """
        try:
            self.latestDataCopy = self.latestData
            self.latestData = newData
        except Exception:
            raise Exception("Error setting latestData's value")
        else:
            self.notifyObservers()
