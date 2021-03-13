import COVID19Py
import CaseByCountry
case = COVID19Py.COVID19()

print(case.getLatest())
print(case.getLatestChanges())
#print(case.getLocationByCountryCode("US"))


country = CaseByCountry(case)
print(country.getLocationByCountryCode("US"))
