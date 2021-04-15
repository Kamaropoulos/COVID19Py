from covid19 import COVID19

access = COVID19.getAccessToGlobal()


print(access.getLocations())
print("--------------------")
print(access.getLocationByCountryCode('US'))

access2 = COVID19.getAccessToGlobal()
