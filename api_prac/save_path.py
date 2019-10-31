import googlemaps
from datetime import datetime

# google map key read
with open('apikey.txt') as f:
    api_key = f.readline()
    f.close
print("Google Map API key :", api_key)
gmaps = googlemaps.Client(key=api_key)

now = datetime.now()
di = gmaps.directions(("37.50539", "126.954445"), ("37.390793", "126.95407"), mode="transit", departure_time=now, alternatives=True)

print(di)