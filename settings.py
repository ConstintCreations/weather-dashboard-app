import sys
from PySide6.QtWidgets import QApplication
from storage import load_data
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
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

        central_widget.setLayout(layout)

        with open("style.qss") as file:
            self.setStyleSheet(file.read())

#Easier for testing
SETTINGS_FILE = Path("settings.json")
app = QApplication(sys.argv)
window = Settings(load_data(SETTINGS_FILE))

window.show()
app.exec()
