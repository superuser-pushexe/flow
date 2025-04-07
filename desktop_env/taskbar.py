import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

def start_taskbar():
    app = QApplication(sys.argv)
    taskbar = QMainWindow()
    taskbar.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    taskbar.setGeometry(0, 0, 800, 30)
    taskbar.setStyleSheet("background-color: black; color: white;")
    label = QLabel("Python Desktop Taskbar", taskbar)
    label.move(10, 5)
    taskbar.show()
    sys.exit(app.exec_())
