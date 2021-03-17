class Data(object):

    """
        Data model for COVID19 class.
        :param previousData: previous requested data.
        :param latestData: current lastest data.
    """
    def __init__(self,previousData=None,latestData=None):
        self.previousData = previousData
        self.latestData = latestData
