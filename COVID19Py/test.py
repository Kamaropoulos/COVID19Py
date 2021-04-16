from covid19 import COVID19
from covid19 import GetTotalData
from covid19 import GetLocationData

access = COVID19()
print(GetTotalData.getAll(access))
print("--------------------------")
print("--------------------------")
print("--------------------------")
print("--------------------------")
print("--------------------------")
print("--------------------------")
print(GetLocationData.getLocations(access))
print("--------------------------")
print("--------------------------")
print("--------------------------")
print(GetLocationData.getLocationByCountryCode(access, 'CA'))
print("--------------------------")
print("--------------------------")
print("--------------------------")
#print(GetLocationData.getLocationById(access, 25))


