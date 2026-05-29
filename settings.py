import sys
from PySide6.QtWidgets import QApplication
from storage import load_data
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider;
from PySide6.QtCore import QDate, QSize, QMargins, QDateTime, QEvent, QThread, QTimer;
from PySide6.QtGui import QIcon, Qt, QFontDatabase, QFont, QPen, QColor;
from PySide6.QtCharts import QChart, QSplineSeries, QChartView, QValueAxis, QDateTimeAxis, QScatterSeries, QLineSeries, QAreaSeries;
from PySide6.QtSvgWidgets import QSvgWidget;

class Settings(QMainWindow):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.setWindowTitle("Settings")
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
        self.temperature_units_slider.setTickInterval(1)
        self.temperature_units_slider.setRange(0, 1)
        if self.settings["temperature_units"] == "fahrenheit":
            self.temperature_units_slider.setValue(1)
        else:    
            self.temperature_units_slider.setValue(0)
        self.temperature_units_edit_layout.addStretch()
        self.temperature_units_edit_layout.addWidget(self.temperature_units_celsius_label)
        self.temperature_units_edit_layout.addWidget(self.temperature_units_slider)
        self.temperature_units_edit_layout.addWidget(self.temperature_units_fahrenheit_label)
        self.temperature_units_edit_layout.addStretch()
        self.temperature_units_layout.addWidget(self.temperature_units_edit_widget)

        layout.addWidget(self.temperature_units_widget)
        
        layout.addStretch()

        central_widget.setLayout(layout)

        with open("style.qss") as file:
            self.setStyleSheet(file.read())

#Easier for testing
SETTINGS_FILE = Path("settings.json")
app = QApplication(sys.argv)
window = Settings(load_data(SETTINGS_FILE))

window.show()
app.exec()
