from abstract import COVIDAPI
from implementation import ImplementationDefault,ImplementationMirror,ImplementationMirror1


#print(COVIDAPI(ImplementationDefault()).getAll())
#print(COVIDAPI(ImplementationMirror()).getAll())
print(COVIDAPI(ImplementationMirror1()).getLocations())