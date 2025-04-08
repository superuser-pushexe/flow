import threading
from desktop_env.wm import start_window_manager
from desktop_env.taskbar import start_taskbar
from desktop_env.wallpaper import set_wallpaper_from_config
from desktop_env.settings import start_settings_app
import os
import json
import subprocess
import sys

required_modules = ['PyQt5', 'Xlib']
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Module '{module}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

default_config = {
    "theme": "light",
    "wallpaper": "/usr/share/backgrounds/default.jpg"
}

if not os.path.exists("config.json"):
    with open("config.json", "w") as f:
        json.dump(default_config, f, indent=4)


def main():
    set_wallpaper_from_config()
    wm_thread = threading.Thread(target=start_window_manager)
    taskbar_thread = threading.Thread(target=start_taskbar)
    wm_thread.start()
    taskbar_thread.start()
    start_settings_app()
    wm_thread.join()
    taskbar_thread.join()

if __name__ == "__main__":
    main()
