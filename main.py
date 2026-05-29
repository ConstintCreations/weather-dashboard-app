import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDate
from pathlib import Path
from storage import load_data, save_data
from apis import get_location, get_weather
from dashboard import WeatherDashboard

SETTINGS_FILE = Path("settings.json")
WEATHER_DATA_FILE = Path("weather.json")
WEATHER_ICON_MAPPINGS_FILE = Path("weatherIconMappings.json")

settings = load_data(SETTINGS_FILE)

if settings is None:
    settings = get_location()
    if not(settings is None):
        settings["timezone"] = "auto"
        settings["apparel"] = [
            {
                "min": -1000,
                "max": 20,
                "recommendation": "Coat"
            },
            {
                "min": 20,
                "max": 45,
                "recommendation": "Jacket"
            },
            {
                "min": 45,
                "max": 65,
                "recommendation": "Long-Sleeve Shirt"
            },
            {
                "min": 65,
                "max": 1000,
                "recommendation": "T-Shirt"
            }
        ]
        settings["temperature_units"] = "fahrenheit"
        settings["precipitation_units"] = "inch"
        save_data(settings, SETTINGS_FILE)
    else:
        settings = {
            "longitude": -87.65,
            "latitude": 41.85,
            "timezone": "auto",
            "temperature_units": "fahrenheit",
            "precipitation_units": "inch",
            "apparel": [
                {
                    "min": -1000,
                    "max": 20,
                    "recommendation": "Coat"
                },
                {
                    "min": 20,
                    "max": 45,
                    "recommendation": "Jacket"
                },
                {
                    "min": 45,
                    "max": 65,
                    "recommendation": "Long-Sleeve Shirt"
                },
                {
                    "min": 65,
                    "max": 1000,
                    "recommendation": "T-Shirt"
                }
            ]
        }

# weather = get_weather(settings)
# save_data(weather, WEATHER_DATA_FILE)

weather = load_data(WEATHER_DATA_FILE)
if weather is None:
    weather = get_weather(settings)
    save_data(weather, WEATHER_DATA_FILE)

foundCurrentDate = False
for index, date in enumerate(weather['daily']['time']):
    if str(date) == str(QDate.currentDate().toPython()):
        foundCurrentDate = True
        break

if foundCurrentDate == False:
    weather = get_weather(settings)
    save_data(weather, WEATHER_DATA_FILE)

app = QApplication(sys.argv)

window = WeatherDashboard(settings = settings, weather = weather, weather_icon_mappings = load_data(WEATHER_ICON_MAPPINGS_FILE))

window.show()
app.exec()