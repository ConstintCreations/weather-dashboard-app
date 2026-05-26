import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QDate
from PySide6.QtGui import QIcon, Qt

class WeatherDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 350)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()

        layout.addLayout(header_layout)

        self.currentDate = QDate.currentDate()

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_date_button = QPushButton()
        right_date_button = QPushButton()

        left_date_button.setIcon(QIcon("icons/leftArrow.svg"))
        right_date_button.setIcon(QIcon("icons/rightArrow.svg"))

        left_date_button.clicked.connect(self.previous_date)
        right_date_button.clicked.connect(self.next_date)

        self.update_date()

        header_layout.addWidget(left_date_button)
        header_layout.addWidget(self.date_label)
        header_layout.addWidget(right_date_button)

        centralWidget.setLayout(layout)

    def update_date(self):
        date_string = self.currentDate.toString("dddd, MMMM, d")

        self.date_label.setText(date_string)

        self.setWindowTitle(f"Weather Dashboard - {date_string}")

    def previous_date(self):
        self.currentDate = self.currentDate.addDays(-1)
        self.update_date()

    def next_date(self):
        self.currentDate = self.currentDate.addDays(1)
        self.update_date()




app = QApplication(sys.argv)

window = WeatherDashboard()

window.show()
app.exec()