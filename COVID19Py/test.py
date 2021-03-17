from covid19 import COVID19

if __name__ == "__main__":
    covid19 = COVID19(data_source='nyt')

    print(covid19.getLatest())