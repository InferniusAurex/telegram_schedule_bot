import requests

API_KEY = "923f6f2041723d02c411f207eb316089"

LAT = 17.0897
LON = 82.0643

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

    try:
        r = requests.get(url, timeout=10)
        print("STATUS:", r.status_code)
        print("RAW:", r.text)

        data = r.json()

        temp = round(data["main"]["temp"])
        condition = data["weather"][0]["main"]

        return f"{temp}°C", condition

    except Exception as e:
        print("Weather error:", e)
        return None, None
