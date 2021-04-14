from covid19 import COVID19,Source


client = COVID19().create_object(Source.Default,"jhu")

print(client.getAll())