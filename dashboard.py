from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QDate, QSize, QMargins, QDateTime, QEvent;
from PySide6.QtGui import QIcon, Qt, QFontDatabase, QFont, QPen, QColor;
from PySide6.QtCharts import QChart, QSplineSeries, QChartView, QValueAxis, QDateTimeAxis, QScatterSeries, QLineSeries, QAreaSeries;
from PySide6.QtSvgWidgets import QSvgWidget;

class WeatherDashboard(QMainWindow):

    def eventFilter(self, watched, event):

        if watched == self.main_chart_view.viewport():

            if event.type() == QEvent.Type.MouseMove:
                self.chart_hover(event.pos())

            if event.type() == QEvent.Type.Leave:
                self.tooltip.hide()
                self.hover_dot.clear()

        return super().eventFilter(watched, event)
    
    def chart_hover(self, position):
        chart_position = self.feels_like_chart.mapToValue(position)
        closest_point = min(self.feels_like_points, key= lambda point: abs(point[0].toMSecsSinceEpoch() - chart_position.x()))
        date_time, temperature = closest_point

        self.hover_dot.clear()
        self.hover_dot.append(date_time.toMSecsSinceEpoch(), temperature)

        time_string = date_time.toString("h:mm AP")
        self.tooltip.setText(f"{time_string} | {temperature}{self.units}")
        self.tooltip.adjustSize()
        self.tooltip.show()

    def get_hourly_data(self, date: QDate, data: str = "apparent_temperature"):
        times = self.weather["hourly"]["time"]
        temperatures = self.weather["hourly"][data]

        points = []

        next_date_time = date.addDays(1)

        for time, temperature in zip(times, temperatures):
            date_time = QDateTime.fromString(time, "yyyy-MM-ddTHH:mm")

            if date_time.date() == date:
                points.append((date_time, temperature))

            if date_time.date() == next_date_time:
                points.append((date_time, temperature))
                break

        return points

    def update_date_display(self):
        date_string = self.currentDate.toString("dddd, MMMM d")

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
        if (self.currentDateIndex + 1) <= 20:
            self.currentDateIndex += 1
            self.currentDate = self.currentDate.addDays(1)
            self.update_date_display()
            self.update_weather_data_display()
            self.left_date_button.setEnabled(True)
            self.left_date_button.setIcon(QIcon("icons/leftArrow.svg"))
            if self.currentDateIndex == 20:
                self.right_date_button.setEnabled(False)
                self.right_date_button.setIcon(QIcon())

    def update_weather_data_display(self):
        if not(self.weather is None):

            self.units = self.weather['current_units']['temperature_2m']
            precipitation_units = self.weather['daily_units']['precipitation_sum']
            if precipitation_units == "inch":
                precipitation_units = "inches"

            if str(self.weather['daily']['time'][self.currentDateIndex]) == str(QDate.currentDate().toPython()):
                self.temperature_label.setText(f"{self.weather['current']['temperature_2m']}{self.units}")
                self.feels_like_label.setText(f"Feels Like {self.weather['current']['apparent_temperature']}{self.units}")
                self.weather_icon.load(self.weather_icon_mappings[f"{self.weather["current"]["weather_code"]}"]["day" if self.weather["current"]["is_day"] == 1 else "night"]["icon"])
                self.weather_label.setText(self.weather_icon_mappings[f"{self.weather["current"]["weather_code"]}"]["day" if self.weather["current"]["is_day"] == 1 else "night"]["description"])
            
            self.precipitation_chance_sum_label.setText(f"{self.weather['daily']['precipitation_probability_max'][self.currentDateIndex]}% | {round(self.weather['daily']['precipitation_sum'][self.currentDateIndex], 2)} {precipitation_units}")
            self.sun_label.setText(f"{QDateTime.fromString(self.weather['daily']['sunrise'][self.currentDateIndex], "yyyy-MM-ddTHH:mm").toString("h:mm AP")} - {QDateTime.fromString(self.weather['daily']['sunset'][self.currentDateIndex], "yyyy-MM-ddTHH:mm").toString("h:mm AP")}")

            self.info_widget.setVisible(True)

            self.feels_like_series.clear()

            self.feels_like_points = self.get_hourly_data(self.currentDate, "apparent_temperature")
            
            if not(self.feels_like_points):
                self.chart.setVisible(False)
                return
            
            for date_time, temperature in self.feels_like_points:
                self.feels_like_series.append(date_time.toMSecsSinceEpoch(), temperature)

            self.feels_like_x.setRange(self.feels_like_points[0][0], self.feels_like_points[-1][0])
            min_feels_like = min(self.feels_like_points, key= lambda point: point[1])[1]
            max_feels_like = max(self.feels_like_points, key= lambda point: point[1])[1]
            gap = (max_feels_like - min_feels_like) * 0.1
            self.feels_like_y.setRange(min_feels_like - gap, max_feels_like + gap)

            self.line_series.clear()
            self.line_series.append(self.feels_like_points[0][0].toMSecsSinceEpoch(), 0)
            self.line_series.append(self.feels_like_points[-1][0].toMSecsSinceEpoch(), 0)
            self.chart.setVisible(True)
            self.tooltip.hide()

            self.chart_max.setText(f"High: {max_feels_like}{self.units}")
            self.chart_avg.setText(f"Avg: {round((max_feels_like+min_feels_like)/2, 1)}{self.units}")
            self.chart_min.setText(f"Low: {min_feels_like}{self.units}")
            self.chart_min_avg_max.setVisible(True)

            self.temperature_points = self.get_hourly_data(self.currentDate, "temperature_2m")
            if not(self.temperature_points):
                return
            
            min_temperature = min(self.temperature_points, key= lambda point: point[1])[1]
            max_temperature = max(self.temperature_points, key= lambda point: point[1])[1]

            if not(str(self.weather['daily']['time'][self.currentDateIndex]) == str(QDate.currentDate().toPython())):
                self.feels_like_label.setText(f"(Avg) Feels Like {round((max_feels_like+min_feels_like)/2, 1)}{self.units}")
                self.temperature_label.setText(f"(Avg) {round((max_temperature+min_temperature)/2, 1)}{self.units}") 
                self.weather_icon.load(self.weather_icon_mappings[f"{self.weather["daily"]["weather_code"][self.currentDateIndex]}"]["day"]["icon"])
                self.weather_label.setText(self.weather_icon_mappings[f"{self.weather["daily"]["weather_code"][self.currentDateIndex]}"]["day"]["description"])           


    def __init__(self, settings, weather, weather_icon_mappings):
        self.settings = settings
        self.weather = weather
        self.weather_icon_mappings = weather_icon_mappings

        super().__init__()
        self.resize(800, 450)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

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
        layout.addSpacing(20)

        self.info_widget = QWidget()
        self.info_widget.setObjectName("infoWidget")

        info_layout = QHBoxLayout(self.info_widget)
        info_layout.addStretch()

        self.weather_widget = QWidget()
        self.weather_layout = QVBoxLayout(self.weather_widget)
        self.weather_icon = WeatherIcon("icons/weather/day/sun.svg", 128)
        self.weather_label = QLabel()
        self.weather_label.setFont(QFont("Stack", 16))
        self.weather_layout.addWidget(self.weather_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        self.weather_layout.addSpacing(5)
        self.weather_layout.addWidget(self.weather_label, alignment=Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(self.weather_widget)

        self.left_info_list_widget = QWidget()
        self.left_info_list_layout = QVBoxLayout(self.left_info_list_widget)

        self.temperature_main_widget = QWidget()
        self.temperature_main_layout = QHBoxLayout(self.temperature_main_widget)

        self.temperature_icon = WeatherIcon("icons/thermometer.svg", 48)
        self.temperature_main_layout.addWidget(self.temperature_icon)

        self.temperature_info_widget = QWidget()
        self.temperature_info_layout = QVBoxLayout(self.temperature_info_widget)
        self.temperature_label = QLabel()
        self.temperature_label.setFont(QFont("Stack", 12))
        self.feels_like_label = QLabel()
        self.feels_like_label.setObjectName("feelsLikeLabel")
        self.feels_like_label.setFont(QFont("Stack", 10))
        self.temperature_info_layout.addWidget(self.temperature_label)
        self.temperature_info_layout.addWidget(self.feels_like_label)
        self.temperature_main_layout.addWidget(self.temperature_info_widget)

        self.left_info_list_layout.addWidget(self.temperature_main_widget)
        self.left_info_list_layout.addStretch()

        self.precipitation_main_widget = QWidget()
        self.precipitation_main_layout = QHBoxLayout(self.precipitation_main_widget)

        self.precipitation_icon = WeatherIcon("icons/rainDroplet.svg", 48)
        self.precipitation_main_layout.addWidget(self.precipitation_icon)

        self.precipitation_info_widget = QWidget()
        self.precipitation_info_layout = QVBoxLayout(self.precipitation_info_widget)
        self.precipitation_chance_sum_label = QLabel()
        self.precipitation_chance_sum_label.setFont(QFont("Stack", 12))
        self.precipitation_info_layout.addWidget(self.precipitation_chance_sum_label)
        self.precipitation_main_layout.addWidget(self.precipitation_info_widget)

        self.left_info_list_layout.addWidget(self.precipitation_main_widget)

        info_layout.addSpacing(20)
        info_layout.addWidget(self.left_info_list_widget)
        info_layout.addSpacing(20)

        self.right_info_list_widget = QWidget()
        self.right_info_list_layout = QVBoxLayout(self.right_info_list_widget)

        self.sun_main_widget = QWidget()
        self.sun_main_layout = QHBoxLayout(self.sun_main_widget)

        self.sun_icon = WeatherIcon("icons/sunriseSquare.svg", 48)
        self.sun_main_layout.addWidget(self.sun_icon)

        self.sun_info_widget = QWidget()
        self.sun_info_layout = QVBoxLayout(self.sun_info_widget)
        self.sun_label = QLabel()
        self.sun_label.setFont(QFont("Stack", 12))
        self.sun_info_layout.addWidget(self.sun_label)
        self.sun_main_layout.addWidget(self.sun_info_widget)

        self.right_info_list_layout.addWidget(self.sun_main_widget)
        self.right_info_list_layout.addStretch()

        self.apparel_main_widget = QWidget()
        self.apparel_main_layout = QHBoxLayout(self.apparel_main_widget)

        self.apparel_icon = WeatherIcon("icons/hangerSquare.svg", 48)
        self.apparel_main_layout.addWidget(self.apparel_icon)

        self.apparel_info_widget = QWidget()
        self.apparel_info_layout = QVBoxLayout(self.apparel_info_widget)
        self.apparel_label = QLabel()
        self.apparel_label.setFont(QFont("Stack", 12))
        self.apparel_info_layout.addWidget(self.apparel_label)
        self.apparel_main_layout.addWidget(self.apparel_info_widget)

        self.right_info_list_layout.addWidget(self.apparel_main_widget)
        info_layout.addWidget(self.right_info_list_widget)

        info_layout.addStretch()

        self.info_widget.setVisible(False)

        self.chart = QWidget()
        self.chart.setObjectName("chart")

        self.chart_layout = QVBoxLayout(self.chart)

        self.chart_min_avg_max = QWidget()
        self.chart_min_avg_max.setObjectName("chartMinAvgMax")
        self.chart_min_avg_max_layout = QHBoxLayout(self.chart_min_avg_max)

        self.chart_max = QLabel()
        self.chart_avg = QLabel()
        self.chart_min = QLabel()

        self.chart_max.setFont(QFont("Stack", 12))
        self.chart_avg.setFont(QFont("Stack", 12))
        self.chart_min.setFont(QFont("Stack", 12))

        self.chart_min_avg_max_layout.addStretch()
        self.chart_min_avg_max_layout.addWidget(self.chart_min)
        self.chart_min_avg_max_layout.addStretch()
        self.chart_min_avg_max_layout.addWidget(self.chart_avg)
        self.chart_min_avg_max_layout.addStretch()
        self.chart_min_avg_max_layout.addWidget(self.chart_max)
        self.chart_min_avg_max_layout.addStretch()

        self.chart_min_avg_max.setVisible(False)

        self.main_chart_title = QLabel("Feels Like Temperature (\u00b0F)")
        self.main_chart_title.setFont(QFont("Stack", 16))

        self.feels_like_pen = QPen(QColor("#ff8800"))
        self.feels_like_pen.setWidth(5)
        self.feels_like_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        self.feels_like_grid_pen = QPen(QColor("#555555"))
        self.feels_like_grid_pen.setWidth(3)

        self.feels_like_series = QSplineSeries()
        self.feels_like_series.setPen(self.feels_like_pen)

        self.feels_like_chart = QChart()
        self.feels_like_chart.legend().hide()
        self.feels_like_chart.setBackgroundVisible(False)
        self.feels_like_chart.setMargins(QMargins(0,0,0,0))
        self.feels_like_chart.setPlotAreaBackgroundVisible(False)
        self.feels_like_chart.addSeries(self.feels_like_series)

        self.feels_like_x = QDateTimeAxis()
        self.feels_like_x.setFormat("h AP")
        self.feels_like_x.setTickCount(5)
        self.feels_like_x.setLabelsColor(QColor("#888888"))
        self.feels_like_x.setGridLinePen(self.feels_like_grid_pen)
        self.feels_like_x.setLinePen(self.feels_like_grid_pen)
        self.feels_like_x.setLabelsFont(QFont("Stack", 10))
        
        self.feels_like_chart.addAxis(self.feels_like_x, Qt.AlignmentFlag.AlignBottom)
        self.feels_like_series.attachAxis(self.feels_like_x)

        self.feels_like_y = QValueAxis()
        self.feels_like_y.setGridLineVisible(False)
        self.feels_like_y.setLineVisible(False)
        self.feels_like_y.setLabelsFont(QFont("Stack", 10))
        self.feels_like_y.setLabelsColor(QColor("#888888"))

        self.feels_like_chart.addAxis(self.feels_like_y, Qt.AlignmentFlag.AlignLeft)
        self.feels_like_series.attachAxis(self.feels_like_y)

        self.hover_dot = QScatterSeries()
        self.hover_dot.setMarkerSize(12)
        self.hover_dot.setColor(QColor("#a85a00"))
        self.hover_dot.setPen(QColor("#a85a00"))
        self.feels_like_chart.addSeries(self.hover_dot)
        self.hover_dot.attachAxis(self.feels_like_x)
        self.hover_dot.attachAxis(self.feels_like_y)

        self.line_series = QLineSeries()

        area_fill_color = QColor("#ff8800")
        area_fill_color.setAlpha(50)

        self.area_series = QAreaSeries(self.feels_like_series, self.line_series)
        self.area_series.setBrush(area_fill_color)
        self.area_series.setPen(Qt.PenStyle.NoPen)
        self.feels_like_chart.addSeries(self.area_series)
        self.area_series.attachAxis(self.feels_like_x)
        self.area_series.attachAxis(self.feels_like_y)
        
        self.main_chart_view = QChartView(self.feels_like_chart)
        self.main_chart_view.viewport().setCursor(Qt.CursorShape.BlankCursor)
        self.main_chart_view.setFixedHeight(200)
        self.main_chart_view.setMouseTracking(True)
        self.main_chart_view.viewport().setMouseTracking(True)
        self.main_chart_view.viewport().installEventFilter(self)

        self.chart.setVisible(False)

        self.tooltip = QLabel(self.main_chart_view)
        self.tooltip.setFont(QFont("Stack", 10))
        self.tooltip.setObjectName("tooltip")
        self.tooltip.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.tooltip.move(40, 0)
        self.tooltip.hide()

        self.update_weather_data_display()

        self.chart_layout.addWidget(self.main_chart_title)
        self.chart_layout.addWidget(self.main_chart_view)

        layout.addStretch()
        layout.addWidget(self.info_widget)
        layout.addSpacing(20)
        layout.addStretch()
        layout.addWidget(self.chart)
        layout.addWidget(self.chart_min_avg_max)
        layout.addStretch()

        central_widget.setLayout(layout)

        with open("style.qss") as file:
            self.setStyleSheet(file.read())

class WeatherIcon(QSvgWidget):
    def __init__(self, path, size = 64):
        super().__init__(path)
        self.setFixedSize(size, size)