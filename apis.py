import requests
from PySide6.QtCore import QObject, Signal

def get_location():
    try:
        data = requests.get("https://ipapi.co/json", timeout=5).json()
        return {
            "longitude": data["longitude"],
            "latitude": data["latitude"]
        }
    
    except Exception:
        return None
    
def get_weather(settings, timeout=30):
    return requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={settings['latitude']}&longitude={settings['longitude']}&daily=temperature_2m_max,temperature_2m_min,sunset,sunrise,precipitation_sum,precipitation_probability_max,weather_code&current=apparent_temperature,temperature_2m,is_day,weather_code&hourly=temperature_2m,apparent_temperature&timezone={settings['timezone']}&past_days=7&forecast_days=16&temperature_unit={settings['temperature_units']}&precipitation_unit={settings['precipitation_units']}", timeout=timeout).json()

class WeatherWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def run(self):
        try:
            new_weather_data = get_weather(self.settings)
            self.finished.emit(new_weather_data)
        except Exception as exception:
            self.error.emit(str(exception))