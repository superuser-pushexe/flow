import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QMenu, QAction
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

def start_taskbar():
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

    # Example apps
    apps = [
        ("Terminal", lambda: print("Launching Terminal...")),
        ("File Manager", lambda: print("Launching File Manager...")),
        ("Browser", lambda: print("Launching Browser...")),
    ]

    for name, action_func in apps:
        action = QAction(name, taskbar)
        action.triggered.connect(action_func)
        app_menu.addAction(action)

    # Show the menu when logo button is clicked
    logo_button.clicked.connect(lambda: app_menu.exec_(logo_button.mapToGlobal(logo_button.rect().bottomLeft())))

    taskbar.show()
    sys.exit(app.exec_())

start_taskbar()
