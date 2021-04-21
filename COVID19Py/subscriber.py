class PreviousDataSubscriber:
    """
    This class represents the `previousData` observer
    """

    def __init__(self):
        self.previousData = None

    def notifyObservers(self, publisher):
        """
        This method is called from the publisher when a possible update to the subject happens.
        It updates the `previousData` after the publisher (latestData) is updated.

        :param publisher: publisher object for which this observer object monitors
        :return: None
        """
        self.previousData = publisher.latestDataCopy