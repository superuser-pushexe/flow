import json
import subprocess
import platform
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

def get_wallpaper_path():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data.get("wallpaper")

def set_wallpaper(path):
    system = platform.system()
    if system == "Linux":
        subprocess.call(["feh", "--bg-scale", path])
    elif system == "Windows":
        import ctypes
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    elif system == "Darwin":  # macOS
        subprocess.call(["osascript", "-e", f'tell app "Finder" to set desktop picture to POSIX file "{path}"'])

def set_wallpaper_from_config():
    path = get_wallpaper_path()
    if path:
        set_wallpaper(path)
