from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
import sys

class WeatherDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Dashboard")
        self.resize(400, 300)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout(self)
        centralWidget.setLayout(layout)

        title = QLabel("Test")
        layout.addWidget(title)

app = QApplication(sys.argv)

window = WeatherDashboard()

window.show()
app.exec()