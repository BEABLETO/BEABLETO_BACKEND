import requests

params = {"version": "1", "city":"서울", "county":"강남구","village":"도곡동"}
headers = {"appKey": "54d398b9-d82b-4361-93ad-fb8366c44e77"}
r = requests.get("http://apis.skplanetx.com/weather/current/hourly", params=params, headers=headers)
print(r.json) #json형태로 출력


