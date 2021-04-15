from covid19 import COVID19

# creating first instance
covid = COVID19()
print(covid)

covid_2 = COVID19.getInstance()
print(covid_2)

covid_3 = COVID19.getInstance()
print(covid_3)

# creating second instance --> raises exception
# working as intended, more than one instance can not be instantiated
new_covid_instance = COVID19()
print(new_covid_instance)