import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QListWidget, QListWidgetItem, QLineEdit, QWidget, QLabel, QGridLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QTimer, QTime, QRect
from tray import SystemTray

CONFIG_PATH = "config.json"

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

class AppsMenu(QWidget):
    def __init__(self, apps, parent=None):
        super().__init__(parent)
        self.apps = apps
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("""
            background-color: #222;
            color: white;
            border: 1px solid #444;
        """)
        layout = QVBoxLayout()

        # Search bar
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search apps...")
        self.search_input.textChanged.connect(self.filter_apps)
        self.search_input.setStyleSheet("padding: 5px; background: #333; border: none;")
        layout.addWidget(self.search_input)

        # Apps grid
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        self.grid_widget.setStyleSheet("background: transparent;")
        layout.addWidget(self.grid_widget)

        # Populate apps
        self.all_buttons = []
        self.update_grid(self.apps)

        self.setLayout(layout)
        self.adjustSize()

    def update_grid(self, apps):
        # Clear existing buttons
        for button in self.all_buttons:
            self.grid_layout.removeWidget(button)
            button.deleteLater()
        self.all_buttons.clear()

        # Add apps in a 3-column grid
        for i, app_entry in enumerate(apps):
            name = app_entry.get("name")
            command = app_entry.get("command")
            if name and command:
                btn = QPushButton(name)
                btn.setStyleSheet("""
                    QPushButton {
                        background: #333;
                        padding: 10px;
                        border: none;
                        color: white;
                    }
                    QPushButton:hover {
                        background: #555;
                    }
                """)
                btn.clicked.connect(lambda _, cmd=command: subprocess.Popen(cmd))
                row = i // 3
                col = i % 3
                self.grid_layout.addWidget(btn, row, col)
                self.all_buttons.append(btn)

    def filter_apps(self, text):
        filtered = [app for app in self.apps if text.lower() in app.get("name", "").lower()]
        self.update_grid(filtered)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return仮 and self.all_buttons:
            self.all_buttons[0].click()
        elif event.key() == Qt.Key_Escape:
            self.close()

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

    # Apps menu
    apps_menu = None
    def toggle_apps_menu():
        nonlocal apps_menu
        if apps_menu is None or not apps_menu.isVisible():
            apps_menu = AppsMenu(apps, taskbar)
            pos = logo_button.mapToGlobal(logo_button.rect().bottomLeft())
            apps_menu.setGeometry(QRect(pos.x(), pos.y(), 300, 400))
            apps_menu.show()
            apps_menu.search_input.setFocus()
        else:
            apps_menu.close()
    logo_button.clicked.connect(toggle_apps_menu)

    # System tray
    tray = SystemTray()
    tray.setParent(taskbar)
    tray.setGeometry(700, 0, 100, 30)

    taskbar.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_taskbar()
