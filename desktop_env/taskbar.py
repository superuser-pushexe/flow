import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QListWidget, QListWidgetItem, QLineEdit, QWidget, QLabel, QGridLayout, QToolTip
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

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search apps...")
        self.search_input.textChanged.connect(self.filter_apps)
        self.search_input.setStyleSheet("padding: 5px; background: #333; border: none;")
        layout.addWidget(self.search_input)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        self.grid_widget.setStyleSheet("background: transparent;")
        layout.addWidget(self.grid_widget)

        self.all_buttons = []
        self.update_grid(self.apps)

        self.setLayout(layout)
        self.adjustSize()

    def update_grid(self, apps):
        for button in self.all_buttons:
            self.grid_layout.removeWidget(button)
            button.deleteLater()
        self.all_buttons.clear()

        for i, app_entry in enumerate(apps):
            name = app_entry.get("name")
            command = app_entry.get("command")
            icon_path = app_entry.get("icon")  # Optional icon path
            if name and command:
                btn = QPushButton(name)
                if icon_path:
                    btn.setIcon(QIcon(icon_path))
                    btn.setIconSize(QSize(24, 24))
                btn.setStyleSheet("""
                    QPushButton {
                        background: #333;
                        padding: 10px;
                        border: none;
                        color: white;
                        text-align: left;
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
        if event.key() == Qt.Key_Return and self.all_buttons:
            self.all_buttons[0].click()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.config["theme_color"] = color.name()
            self.save_config()
            # Apply to all components (simplified)
            QApplication.instance().setStyleSheet(f"""
                QWidget {{ background-color: {color.name()}; }}
                QPushButton {{ background-color: {color.name()}; }}
            """)

        self.logo_button = QPushButton(self)
        self.logo_button.setIcon(QIcon("logo.png"))
        self.logo_button.setIconSize(QSize(24, 24))
        self.logo_button.setGeometry(5, 3, 24, 24)
        self.logo_button.setStyleSheet("background: transparent; border: none;")

        self.apps_menu = None
        self.logo_button.clicked.connect(self.toggle_apps_menu)

        self.window_buttons = []
        self.window_area = QWidget(self)
        self.window_area.setGeometry(40, 0, screen.width() - 140, 30)
        self.window_layout = QHBoxLayout(self.window_area)
        self.window_layout.setSpacing(5)

        self.tray = SystemTray()
        self.tray.setParent(self)
        self.tray.setGeometry(screen.width() - 100, 0, 100, 30)

        # Timer to update window list
        self.window_timer = QTimer()
        self.window_timer.timeout.connect(self.update_windows)
        self.window_timer.start(1000)
        self.update_windows()

    def update_windows(self):
        global open_windows
        # Clear existing buttons
        for btn in self.window_buttons:
            self.window_layout.removeWidget(btn)
            btn.deleteLater()
        self.window_buttons.clear()

        # Add new buttons for open windows
        for win in open_windows:
            btn = QPushButton(win["name"], self.window_area)
            btn.setStyleSheet("color: white; background: #333; border: none;")
            btn.setFixedWidth(150)
            btn.setToolTip(win["name"])
            self.window_layout.addWidget(btn)
            self.window_buttons.append(btn)

    # Rest of the class remains the same

    def toggle_apps_menu(self):
        if self.apps_menu is None or not self.apps_menu.isVisible():
            self.apps_menu = AppsMenu(self.apps, self)
            pos = self.logo_button.mapToGlobal(self.logo_button.rect().bottomLeft())
            self.apps_menu.setGeometry(QRect(pos.x(), pos.y(), 300, 400))
            self.apps_menu.show()
            self.apps_menu.search_input.setFocus()
        else:
            self.apps_menu.close()

    def add_window(self, window_title):
        btn = QPushButton(window_title, self.window_area)
        btn.setStyleSheet("color: white; background: #333; border: none;")
        btn.setFixedWidth(150)
        btn.setToolTip(window_title)
        self.window_layout.addWidget(btn)
        self.window_buttons.append(btn)

def start_taskbar():
    app = QApplication(sys.argv)
    taskbar = Taskbar()
    taskbar.show()
    app.exec_()

if __name__ == "__main__":
    start_taskbar()
