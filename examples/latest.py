from COVID19Py import COVID19

covid19 = COVID19()


print(covid19.getLatest())
print(covid19.getAll(timelines=True))
print(covid19.getLatestChanges())
print(covid19.getLocationById(1))
print(covid19.getLocationByCountry("Canada"))
print(covid19.getLocationByCountryCode("CA"))
print(covid19.getLatest())
print(covid19.getLocations())