import json
import subprocess
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

def get_wallpaper_path():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    return data.get("wallpaper")

def set_wallpaper(path):
    subprocess.call(["feh", "--bg-scale", path])

def set_wallpaper_from_config():
    path = get_wallpaper_path()
    if path:
        set_wallpaper(path)
