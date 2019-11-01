import googlemaps
import unicodedata
import requests
import datetime
import json

# google map key read
with open('apikey.txt') as f:
    api_key = f.readline()
    f.close
print("Google Map API key :", api_key)
gmaps = googlemaps.Client(key=api_key)
bus_api_key = "o%2F8lx%2BaSSJ5JX9amhzpTK14wysQgTKaS2WkFl1j5I6lQ9hZiUQbGOAzpXsGTZGSgxpFhKsKnNCG0j1hN8jONZw%3D%3D"

# BUS info READ
un_bus =[]
with open('LowBus.txt', 'rt', encoding='UTF8') as f:
    line = f.readline()
    while line:
        un_bus.append(line[:-1])
        line = f.readline()
    f.close

print(un_bus)

d = datetime.date(2019, 11, 1)
t = datetime.time(12, 23, 38)
dt = datetime.datetime.combine(d, t)

# now = datetime.now()
# print(now)
di = gmaps.directions(("37.510014", "126.96339"), ("37.505108", "126.95354"), mode="transit", departure_time=dt, alternatives=True)
# print(di)37.505108	126.95354
path_index = 0
for path in di:
    path_index += 1
    print("PATH NUMBER :", path_index)
    # print(path['legs'])
    for sub_path in path['legs'][0]['steps']:
        print("Start Cord :", sub_path['start_location'])
        print("End Cord :", sub_path['end_location'])
        print("Path Type :", sub_path['travel_mode'])
        # for i in sub_path:
        #     print(i)
        if str(sub_path['travel_mode']) == "TRANSIT":
            if "지하철" in sub_path['transit_details']['line']['name']:
                print("지하철")
            else:
                print("버스", sub_path['transit_details']['line']['name'][:2], sub_path['transit_details']['line']['short_name'], end=" ")
                if sub_path['transit_details']['line']['short_name'] in un_bus:
                    print("비저상버스")
                else:
                    print("저상버스")
        # else:
        #     headers = {'Accept': "application/json",
        #                'Content-Type': "application/json; charset=UTF-8",
        #                'appKey': "54d398b9-d82b-4361-93ad-fb8366c44e77",
        #                'Accept-Language': "ko",
        #                }
        #     body = {'startX': str(sub_path['start_location']['lng']),
        #             'startY': str(sub_path['start_location']['lat']),
        #             'endX': str(sub_path['end_location']['lng']),
        #             'endY': str(sub_path['end_location']['lat']),
        #             # 'reqCoordType': "WGS84GEO",
        #             'startName': "안뇽",
        #             'endName': "잘가",
        #             }
        #
        #     r = requests.post('https://apis.openapi.sk.com/tmap/routes/pedestrian', headers=headers, data=json.dumps(body))
        #     while str(r) != "<Response [200]>":
        #         print(r)
        #
        #     for element in r.json()['features']:
        #         if element['geometry']['type'] == "Point":
        #             print("경로 :", element['geometry']['coordinates'][1], element['geometry']['coordinates'][0])


        print()
    print(end="\n\n\n\n")
