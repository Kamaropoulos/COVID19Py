from observer import *
import requests
subject = ConcreteCovidGetLocation()

observer_1 = ConcreteObserver()
observer_2 = ConcreteObserver()

subject.attach(observer_1)
subject.attach(observer_2)

subject.getLocationByCountry("canada")


print(observer_1.data)