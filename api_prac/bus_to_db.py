import requests
import json

with open('LowBus_not.txt', 'rt', encoding='UTF8') as f:
    line = f.readline()
    while line:
        line = line[:-1]
        headers = {'Authorization': "Token a3bac872c62a14150fa00c3d0a353faa8d162c23",
                   'Content-Type': "application/json",
                  }
        body = {'area': "서울",
                'line': line,
                'height': 0,
                }
        r = requests.post('http://127.0.0.1:8000/information/bussave/', headers=headers, data=json.dumps(body))
        while str(r) != "<Response [201]>":
            print(r)
            r = requests.post('http://127.0.0.1:8000/information/bussave/', headers=headers, data=json.dumps(body))
        line = f.readline()
    f.close

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