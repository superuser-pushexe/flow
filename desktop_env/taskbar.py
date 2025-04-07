import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QMenu, QAction, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QTimer, QTime

CONFIG_PATH = "config.json"

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

def start_taskbar():
    config = load_config()
    apps = config.get("apps", [])

    app = QApplication(sys.argv)
    taskbar = QMainWindow()
    taskbar.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    taskbar.setGeometry(0, 0, 800, 30)
    taskbar.setStyleSheet("background-color: black;")

    # Logo button
    logo_button = QPushButton(taskbar)
    logo_button.setIcon(QIcon("logo.png"))
    logo_button.setIconSize(QSize(24, 24))
    logo_button.setGeometry(5, 3, 24, 24)
    logo_button.setStyleSheet("background: transparent; border: none;")

    # App menu
    app_menu = QMenu(taskbar)
    app_menu.setStyleSheet("QMenu { background-color: #222; color: white; }")

    for app_entry in apps:
        name = app_entry.get("name")
        command = app_entry.get("command")
        if name and command:
            action = QAction(name, taskbar)
            action.triggered.connect(lambda _, cmd=command: subprocess.Popen(cmd))
            app_menu.addAction(action)

    logo_button.clicked.connect(lambda: app_menu.exec_(logo_button.mapToGlobal(logo_button.rect().bottomLeft())))

    # Clock label
    clock_label = QLabel(taskbar)
    clock_label.setStyleSheet("color: white; font-family: monospace;")
    clock_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    clock_label.setGeometry(700, 0, 95, 30)

    def update_clock():
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        clock_label.setText(current_time)

    timer = QTimer()
    timer.timeout.connect(update_clock)
    timer.start(1000)
    update_clock()

    taskbar.show()
    sys.exit(app.exec_())

start_taskbar()
