import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QListWidget, QHBoxLayout, QLineEdit, QListWidgetItem, QMessageBox, QComboBox, QColorDialog
)
from desktop_env.wallpaper import set_wallpaper
import sys

CONFIG_PATH = Path(__file__).parent / "config.json"

class SettingsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.config = self.load_config()

        self.init_wallpaper_section()
        self.init_apps_section()
        self.init_appearance_section()

    def load_config(self):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)

    def save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)

    def init_wallpaper_section(self):
        self.layout.addWidget(QLabel("Wallpaper:"))
        self.wallpaper_btn = QPushButton("Change Wallpaper")
        self.wallpaper_btn.clicked.connect(self.choose_wallpaper)
        self.layout.addWidget(self.wallpaper_btn)

    def choose_wallpaper(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Wallpaper")
        if file:
            self.config["wallpaper"] = file
            self.save_config()
            set_wallpaper(file)

    def init_apps_section(self):
        self.layout.addWidget(QLabel("Apps in Taskbar:"))

        self.app_list = QListWidget()
        for app in self.config["apps"]:
            item = QListWidgetItem(f'{app["name"]} - {app["command"]}')
            self.app_list.addItem(item)
        self.layout.addWidget(self.app_list)

        app_input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("App Name")
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Command (e.g. xdg-open .)")
        app_input_layout.addWidget(self.name_input)
        app_input_layout.addWidget(self.command_input)

        self.layout.addLayout(app_input_layout)

        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Add App")
        add_btn.clicked.connect(self.add_app)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("Remove Selected App")
        remove_btn.clicked.connect(self.remove_app)
        btn_layout.addWidget(remove_btn)

        self.layout.addLayout(btn_layout)

    def add_app(self):
        name = self.name_input.text().strip()
        command = self.command_input.text().strip().split()

        if not name or not command:
            QMessageBox.warning(self, "Input Error", "Please enter both a name and a command.")
            return

        app_entry = {"name": name, "command": command}
        self.config["apps"].append(app_entry)
        self.app_list.addItem(f'{name} - {command}')
        self.save_config()

        self.name_input.clear()
        self.command_input.clear()

    def remove_app(self):
        selected_items = self.app_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            index = self.app_list.row(item)
            self.app_list.takeItem(index)
            del self.config["apps"][index]
        self.save_config()

    def init_appearance_section(self):
        self.layout.addWidget(QLabel("Appearance:"))

        # Taskbar position
        taskbar_layout = QHBoxLayout()
        taskbar_layout.addWidget(QLabel("Taskbar Position:"))
        self.taskbar_pos = QComboBox()
        self.taskbar_pos.addItems(["top", "bottom"])
        self.taskbar_pos.setCurrentText(self.config.get("taskbar_position", "top"))
        self.taskbar_pos.currentTextChanged.connect(self.update_taskbar_position)
        taskbar_layout.addWidget(self.taskbar_pos)
        self.layout.addLayout(taskbar_layout)

        # Theme color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Theme Color:"))
        self.color_btn = QPushButton("Choose Color")
        self.color_btn.clicked.connect(self.choose_color)
        color_layout.addWidget(self.color_btn)
        self.layout.addLayout(color_layout)

    def update_taskbar_position(self, position):
        self.config["taskbar_position"] = position
        self.save_config()
        QMessageBox.information(self, "Restart Required", "Please restart Flow Desktop to apply taskbar position.")

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.config["theme_color"] = color.name()
            self.save_config()
            self.setStyleSheet(f"background-color: {color.name()};")

def start_settings_app():
    app = QApplication(sys.argv)

    with open("config.json", "r") as f:
        config = json.load(f)
    theme = config.get("theme", "light")
    if theme == "dark":
        app.setStyleSheet(open("dark.qss").read())
    else:
        app.setStyleSheet(open("light.qss").read())

    win = SettingsApp()
    win.show()
    app.exec_()
