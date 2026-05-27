import sys, requests
from PySide6.QtWidgets import QApplication
from pathlib import Path
from storage import load_data, save_data
from apis import get_location, get_weather
from dashboard import WeatherDashboard

SETTINGS_FILE = Path("settings.json")
WEATHER_DATA_FILE = Path("weather.json")

settings = load_data(SETTINGS_FILE)

if settings is None:
    settings = get_location()
    if not(settings is None):
        save_data(settings, SETTINGS_FILE)
    else:
        settings = {
            "longitude": 0,
            "latitude": 0,
            "timezone": ""
        }

weather = get_weather(settings)
save_data(weather, WEATHER_DATA_FILE)


app = QApplication(sys.argv)

window = WeatherDashboard()

window.show()
app.exec()