
class covid19singleton:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance


    def __call__(self,cls,*args,**kwargs):
        if cls not in cls._instance:
            cls._instance = super(covid19singleton,cls)

        return cls._instances    

