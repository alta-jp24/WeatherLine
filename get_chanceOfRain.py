import requests

url = requests.get("https://weather.tsukumijima.net/api/forecast/city/180010")
data = url.json()

chanceOfRain = data["forecasts"][0]["chanceOfRain"]["T12_18"]

print(f"T12_18の降水確率: {chanceOfRain}")