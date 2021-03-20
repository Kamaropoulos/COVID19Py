import COVID19Py

covid19 = COVID19Py.COVID19(data_source="csbs")

location = covid19.getLocationByCountryCode("US")
print(covid19.getLatest())
print(location)
