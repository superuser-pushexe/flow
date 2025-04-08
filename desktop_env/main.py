import threading
from desktop_env.wm import start_window_manager
from desktop_env.taskbar import start_taskbar
from desktop_env.wallpaper import set_wallpaper_from_config
from desktop_env.settings import start_settings_app
from desktop_env.desktop import start_desktop
import os
import json
import subprocess
import sys

required_modules = ['PyQt5', 'Xlib', 'psutil']
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Module '{module}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

default_config = {
    "theme": "light",
    "wallpaper": "/usr/share/backgrounds/default.jpg",
    "taskbar_position": "top",
    "apps": []
}

if not os.path.exists("config.json"):
    with open("config.json", "w") as f:
        json.dump(default_config, f, indent=4)

def main():
    set_wallpaper_from_config()
    desktop_thread = threading.Thread(target=start_desktop)
    wm_thread = threading.Thread(target=start_window_manager)
    taskbar_thread = threading.Thread(target=start_taskbar)
    desktop_thread.start()
    wm_thread.start()
    taskbar_thread.start()
    start_settings_app()
    desktop_thread.join()
    wm_thread.join()
    taskbar_thread.join()

if __name__ == "__main__":
    main()
