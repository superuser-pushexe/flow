import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from desktop_env.wallpaper import set_wallpaper

CONFIG_PATH = Path(__file__).parent / "config.json"

def start_settings_app():
    app = QApplication([])
    win = QWidget()
    win.setWindowTitle("Desktop Settings")
    layout = QVBoxLayout()
    label = QLabel("Choose Wallpaper")

    def choose_wallpaper():
        file, _ = QFileDialog.getOpenFileName(win, "Select Wallpaper")
        if file:
            with open(CONFIG_PATH, "r+") as f:
                data = json.load(f)
                data["wallpaper"] = file
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            set_wallpaper(file)

    btn = QPushButton("Change Wallpaper")
    btn.clicked.connect(choose_wallpaper)

    layout.addWidget(label)
    layout.addWidget(btn)
    win.setLayout(layout)
    win.show()
    app.exec_()
