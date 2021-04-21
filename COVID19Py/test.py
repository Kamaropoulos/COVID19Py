from .observer import *

subject = ConcreteCovidGetLatest()

observer_1 = ConcreteObserver()
observer_2 = ConcreteObserver()

subject.attach(observer_1)
subject.attach(observer_2)

subject.getLatest()


print(observer_1.data)