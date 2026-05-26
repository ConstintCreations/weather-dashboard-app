import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QDate, QSize;
from PySide6.QtGui import QIcon, Qt, QFontDatabase, QFont;

class WeatherDashboard(QMainWindow):

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

    def __init__(self):
        super().__init__()
        self.resize(600, 350)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        QFontDatabase.addApplicationFont(
            "fonts/Stack.ttf"
        )

        self.setFont(QFont("Stack"))

        layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()

        self.currentDate = QDate.currentDate()

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.date_label.setObjectName("dateLabel")

        left_date_button = QPushButton()
        right_date_button = QPushButton()

        left_date_button.setIcon(QIcon("icons/leftArrow.svg"))
        right_date_button.setIcon(QIcon("icons/rightArrow.svg"))

        left_date_button.setIconSize(QSize(20, 12.5))
        right_date_button.setIconSize(QSize(20, 12.5))

        left_date_button.setFixedSize(80, 30)
        right_date_button.setFixedSize(80, 30)

        left_date_button.setCursor(Qt.CursorShape.PointingHandCursor)
        right_date_button.setCursor(Qt.CursorShape.PointingHandCursor)

        left_date_button.clicked.connect(self.previous_date)
        right_date_button.clicked.connect(self.next_date)

        self.update_date()

        header_layout.addStretch()
        header_layout.addWidget(left_date_button)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.date_label)
        header_layout.addSpacing(15)
        header_layout.addWidget(right_date_button)
        header_layout.addStretch()

        layout.addLayout(header_layout)
        layout.addStretch()

        centralWidget.setLayout(layout)

        with open("style.qss") as file:
            self.setStyleSheet(file.read())




app = QApplication(sys.argv)

window = WeatherDashboard()

window.show()
app.exec()