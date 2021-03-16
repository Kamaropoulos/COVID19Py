import COVID19Py

covid19 = COVID19Py.COVID19()
locations = covid19.getLocationByCountryCode("CA")
print(covid19.getLatest())
print(locations)