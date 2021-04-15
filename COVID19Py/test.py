from abstract import COVIDAPI
from implementation import ImplementationDefault


print(COVIDAPI(ImplementationDefault()).getLatest())