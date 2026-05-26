from PySide6.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Weather Dashboard")
window.resize(400, 300)

window.show()
app.exec()