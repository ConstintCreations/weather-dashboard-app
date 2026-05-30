import sys
from PySide6.QtWidgets import QApplication
from storage import load_data
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QDoubleSpinBox, QAbstractSpinBox;
from PySide6.QtGui import Qt, QFontDatabase, QFont;

class Settings(QMainWindow):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.setWindowTitle("Weather Dashboard - Settings")
        self.resize(600, 400)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        QFontDatabase.addApplicationFont(
            "fonts/Stack.ttf"
        )

        self.setFont(QFont("Stack"))

        layout = QVBoxLayout()

        layout.addStretch()

        self.location_widget = QWidget()
        self.location_layout = QVBoxLayout(self.location_widget)
        self.location_label = QLabel("Location", alignment = Qt.AlignmentFlag.AlignCenter)
        self.location_label.setFont(QFont("Stack", 16))
        self.location_layout.addWidget(self.location_label)
        self.latitude_edit_widget = QWidget()
        self.latitude_edit_layout = QHBoxLayout(self.latitude_edit_widget)
        self.latitude_label = QLabel("Latitude: ", alignment = Qt.AlignmentFlag.AlignLeft)
        self.latitude_label.setFont(QFont("Stack", 12))
        self.latitude_spinbox = QDoubleSpinBox(alignment = Qt.AlignmentFlag.AlignCenter)
        self.latitude_spinbox.setFont(QFont("Stack", 12))
        self.latitude_spinbox.setRange(-90, 90)
        self.latitude_spinbox.setDecimals(4)
        self.latitude_spinbox.setFixedWidth(140)
        self.latitude_spinbox.setValue(self.settings["latitude"])
        self.latitude_edit_layout.addWidget(self.latitude_label)
        self.latitude_edit_layout.addWidget(self.latitude_spinbox)
        self.longitude_edit_widget = QWidget()
        self.longitude_edit_layout = QHBoxLayout(self.longitude_edit_widget)
        self.longitude_label = QLabel("Longitude: ", alignment = Qt.AlignmentFlag.AlignLeft)
        self.longitude_label.setFont(QFont("Stack", 12))
        self.longitude_spinbox = QDoubleSpinBox(alignment = Qt.AlignmentFlag.AlignCenter)
        self.longitude_spinbox.setFont(QFont("Stack", 12))
        self.longitude_spinbox.setRange(-180, 180)
        self.longitude_spinbox.setDecimals(4)
        self.longitude_spinbox.setFixedWidth(140)
        self.longitude_spinbox.setValue(self.settings["longitude"])
        self.longitude_edit_layout.addWidget(self.longitude_label)
        self.longitude_edit_layout.addWidget(self.longitude_spinbox)
        self.location_layout.addWidget(self.latitude_edit_widget)
        self.location_layout.addWidget(self.longitude_edit_widget)

        self.temperature_units_widget = QWidget()
        self.temperature_units_layout = QVBoxLayout(self.temperature_units_widget)
        self.temperature_units_label = QLabel("Temperature Units", alignment = Qt.AlignmentFlag.AlignCenter)
        self.temperature_units_label.setFont(QFont("Stack", 16))
        self.temperature_units_layout.addWidget(self.temperature_units_label)
        self.temperature_units_edit_widget = QWidget()
        self.temperature_units_edit_layout = QHBoxLayout(self.temperature_units_edit_widget)
        self.temperature_units_celsius_label = QLabel("\u00b0C")
        self.temperature_units_celsius_label.setFont(QFont("Stack", 12))
        self.temperature_units_fahrenheit_label = QLabel("\u00b0F")
        self.temperature_units_fahrenheit_label.setFont(QFont("Stack", 12))
        self.temperature_units_slider = QSlider(Qt.Horizontal)
        self.temperature_units_slider.setFixedHeight(24)
        self.temperature_units_slider.setTickInterval(1)
        self.temperature_units_slider.setRange(0, 1)
        if self.settings["temperature_units"] == "fahrenheit":
            self.temperature_units_slider.setValue(1)
        else:    
            self.temperature_units_slider.setValue(0)
        self.temperature_units_edit_layout.addSpacing(50)
        self.temperature_units_edit_layout.addWidget(self.temperature_units_celsius_label)
        self.temperature_units_edit_layout.addWidget(self.temperature_units_slider)
        self.temperature_units_edit_layout.addWidget(self.temperature_units_fahrenheit_label)
        self.temperature_units_edit_layout.addSpacing(50)
        self.temperature_units_layout.addWidget(self.temperature_units_edit_widget)

        self.precipitation_units_widget = QWidget()
        self.precipitation_units_layout = QVBoxLayout(self.precipitation_units_widget)
        self.precipitation_units_label = QLabel("Precipitation Units", alignment = Qt.AlignmentFlag.AlignCenter)
        self.precipitation_units_label.setFont(QFont("Stack", 16))
        self.precipitation_units_layout.addWidget(self.precipitation_units_label)
        self.precipitation_units_edit_widget = QWidget()
        self.precipitation_units_edit_layout = QHBoxLayout(self.precipitation_units_edit_widget)
        self.precipitation_units_mm_label = QLabel("mm")
        self.precipitation_units_mm_label.setFont(QFont("Stack", 12))
        self.precipitation_units_inch_label = QLabel("in.")
        self.precipitation_units_inch_label.setFont(QFont("Stack", 12))
        self.precipitation_units_slider = QSlider(Qt.Horizontal)
        self.precipitation_units_slider.setFixedHeight(24)
        self.precipitation_units_slider.setTickInterval(1)
        self.precipitation_units_slider.setRange(0, 1)
        if self.settings["precipitation_units"] == "inch":
            self.precipitation_units_slider.setValue(1)
        else:    
            self.precipitation_units_slider.setValue(0)
        self.precipitation_units_edit_layout.addSpacing(50)
        self.precipitation_units_edit_layout.addWidget(self.precipitation_units_mm_label)
        self.precipitation_units_edit_layout.addWidget(self.precipitation_units_slider)
        self.precipitation_units_edit_layout.addWidget(self.precipitation_units_inch_label)
        self.precipitation_units_edit_layout.addSpacing(50)
        self.precipitation_units_layout.addWidget(self.precipitation_units_edit_widget)

        self.apparel_widget = QWidget()
        self.apparel_layout = QVBoxLayout(self.apparel_widget)
        self.apparel_label = QLabel("Apparel", alignment = Qt.AlignmentFlag.AlignCenter)
        self.apparel_label.setFont(QFont("Stack", 16))
        self.apparel_layout.addWidget(self.apparel_label)
        
        layout.addWidget(self.location_widget)
        layout.addWidget(self.temperature_units_widget)
        layout.addWidget(self.precipitation_units_widget)
        layout.addWidget(self.apparel_widget)
        layout.addStretch()

        central_widget.setLayout(layout)

        with open("style.qss") as file:
            self.setStyleSheet(file.read())

#Easier for testing
#"""
SETTINGS_FILE = Path("settings.json")
app = QApplication(sys.argv)
window = Settings(load_data(SETTINGS_FILE))

window.show()
app.exec()
#"""
