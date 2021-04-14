class Singleton(type):

    #can have multiple instances would have the same result
    _singletonInstances = {}

    def __call__(cls, *args, **kwargs):
        #changes to arguement values of __inut__ will not impact returned instance

        if cls not in cls._singletonInstances:
            instance = super().__call__(*args, **kwargs)
            cls._singletonInstances[cls] = instance
        return cls._singletonInstances[cls]
