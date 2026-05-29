import requests

def get_location():
    try:
        data = requests.get("https://ipapi.co/json", timeout=5).json()
        return {
            "longitude": data["longitude"],
            "latitude": data["latitude"],
            "timezone": data["timezone"]
        }
    
    except Exception:
        return None
    
def get_weather(settings):
    return requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={settings['latitude']}&longitude={settings['longitude']}&daily=temperature_2m_max,temperature_2m_min,sunset,sunrise,precipitation_sum,precipitation_probability_max,weather_code&current=apparent_temperature,temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature&timezone={settings['timezone']}&past_days=7&forecast_days=16&temperature_unit=fahrenheit&precipitation_unit=inch", timeout=15).json()