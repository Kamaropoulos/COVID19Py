import COVID19Py

covid19 = COVID19Py.SingletonOfCOVID19()
co = COVID19Py.SingletonOfCOVID19()
print(covid19.getLocationByCountry("China"))
print(co.getAll())
