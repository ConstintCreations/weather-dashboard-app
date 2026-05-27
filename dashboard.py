from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QDate, QSize;
from PySide6.QtGui import QIcon, Qt, QFontDatabase, QFont, QPen, QColor;
from PySide6.QtCharts import QChart, QSplineSeries, QChartView, QValueAxis;

class WeatherDashboard(QMainWindow):

    def update_date_display(self):
        date_string = self.currentDate.toString("dddd, MMMM, d")

        self.date_label.setText(date_string)

        self.setWindowTitle(f"Weather Dashboard - {date_string}")

    def previous_date(self):
        if (self.currentDateIndex - 1) >= 0: 
            self.currentDateIndex -= 1
            self.currentDate = self.currentDate.addDays(-1)
            self.update_date_display()
            self.update_weather_data_display()
            self.right_date_button.setEnabled(True)
            self.right_date_button.setIcon(QIcon("icons/rightArrow.svg"))
            if self.currentDateIndex == 0:
                self.left_date_button.setEnabled(False)
                self.left_date_button.setIcon(QIcon())

    def next_date(self):
        if (self.currentDateIndex + 1) <= 22:
            self.currentDateIndex += 1
            self.currentDate = self.currentDate.addDays(1)
            self.update_date_display()
            self.update_weather_data_display()
            self.left_date_button.setEnabled(True)
            self.left_date_button.setIcon(QIcon("icons/leftArrow.svg"))
            if self.currentDateIndex == 22:
                self.right_date_button.setEnabled(False)
                self.right_date_button.setIcon(QIcon())

    def update_weather_data_display(self):
        if not(self.weather is None):

            units = self.weather['current_units']['temperature_2m']
            precipitation_units = self.weather['daily_units']['precipitation_sum']

            if str(self.weather['daily']['time'][self.currentDateIndex]) == str(QDate.currentDate().toPython()):
                self.current_temperature_label.setVisible(True)
                self.current_temperature_label.setText(f"Temperature ({units}): {self.weather['current']['temperature_2m']}")
                self.feels_like_label.setVisible(True)
                self.feels_like_label.setText(f"Feels Like ({units}): {self.weather['current']['apparent_temperature']}")
            else:
                self.current_temperature_label.setVisible(False)
                self.feels_like_label.setVisible(False)

            self.daily_high_label.setText(f"High ({units}): {self.weather['daily']['temperature_2m_max'][self.currentDateIndex]}")
            self.daily_low_label.setText(f"Low ({units}): {self.weather['daily']['temperature_2m_min'][self.currentDateIndex]}")
            self.feels_like_high_label.setText(f"Feels Like High ({units}): {self.weather['daily']['apparent_temperature_max'][self.currentDateIndex]}")
            self.feels_like_low_label.setText(f"Feels Like Low ({units}): {self.weather['daily']['apparent_temperature_min'][self.currentDateIndex]}")
            self.precipitation_sum_label.setText(f"Estimated Precipitation ({precipitation_units}): {self.weather['daily']['precipitation_sum'][self.currentDateIndex]}")
            self.precipitation_chance_label.setText(f"Precipitation Chance (%): {self.weather['daily']['precipitation_probability_max'][self.currentDateIndex]}")

    def __init__(self, settings, weather):
        self.settings = settings
        self.weather = weather

        super().__init__()
        self.resize(600, 350)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        QFontDatabase.addApplicationFont(
            "fonts/Stack.ttf"
        )

        self.setFont(QFont("Stack"))

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        self.currentDate = QDate.currentDate()
        self.currentDateIndex = 7

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.date_label.setObjectName("dateLabel")

        self.left_date_button = QPushButton()
        self.right_date_button = QPushButton()

        self.left_date_button.setIcon(QIcon("icons/leftArrow.svg"))
        self.right_date_button.setIcon(QIcon("icons/rightArrow.svg"))

        self.left_date_button.setIconSize(QSize(20, 12.5))
        self.right_date_button.setIconSize(QSize(20, 12.5))

        self.left_date_button.setFixedSize(80, 30)
        self.right_date_button.setFixedSize(80, 30)

        self.left_date_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.right_date_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.left_date_button.clicked.connect(self.previous_date)
        self.right_date_button.clicked.connect(self.next_date)

        self.update_date_display()

        header_layout.addStretch()
        header_layout.addWidget(self.left_date_button)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.date_label)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.right_date_button)
        header_layout.addStretch()

        layout.addLayout(header_layout)
        layout.addStretch()

        central_layout = QVBoxLayout()

        self.current_temperature_label = QLabel()
        self.daily_high_label = QLabel()
        self.daily_low_label = QLabel()

        self.feels_like_label = QLabel()
        self.feels_like_low_label = QLabel()
        self.feels_like_high_label = QLabel()

        self.precipitation_sum_label = QLabel()
        self.precipitation_chance_label = QLabel()

        self.feels_like_pen = QPen(QColor("#ff8800"))
        self.feels_like_pen.setWidth(5)

        self.feels_like_series = QSplineSeries()
        self.feels_like_series.setPen(self.feels_like_pen)
        self.feels_like_series.append(0, 6)
        self.feels_like_series.append(1, 62)
        self.feels_like_series.append(2, 44)

        self.feels_like_chart = QChart()
        self.feels_like_chart.legend().hide()
        self.feels_like_chart.setBackgroundVisible(True)
        self.feels_like_chart.setPlotAreaBackgroundVisible(False)
        self.feels_like_chart.addSeries(self.feels_like_series)

        self.feels_like_x = QValueAxis()
        self.feels_like_x.setRange(0, 2)
        self.feels_like_x.setTickCount(4)
        
        self.feels_like_chart.addAxis(self.feels_like_x, Qt.AlignmentFlag.AlignBottom)
        self.feels_like_series.attachAxis(self.feels_like_x)

        self.feels_like_y = QValueAxis()
        self.feels_like_y.setRange(0, 80)
        self.feels_like_y.setTickCount(2)
        self.feels_like_y.setGridLineVisible(False)

        self.feels_like_chart.addAxis(self.feels_like_y, Qt.AlignmentFlag.AlignLeft)
        self.feels_like_series.attachAxis(self.feels_like_y)
        
        self.main_chart_view = QChartView(self.feels_like_chart)

        self.main_chart_view.setMinimumHeight(200)

        self.update_weather_data_display()

        central_layout.addWidget(self.current_temperature_label)
        central_layout.addWidget(self.daily_high_label)
        central_layout.addWidget(self.daily_low_label)

        central_layout.addWidget(self.feels_like_label)
        central_layout.addWidget(self.feels_like_high_label)
        central_layout.addWidget(self.feels_like_low_label)

        central_layout.addWidget(self.precipitation_sum_label)
        central_layout.addWidget(self.precipitation_chance_label)

        central_layout.addWidget(self.main_chart_view)

        layout.addLayout(central_layout)
        layout.addStretch()

        centralWidget.setLayout(layout)

        with open("style.qss") as file:
            self.setStyleSheet(file.read())