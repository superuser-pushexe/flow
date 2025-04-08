import threading
from desktop_env.wm import start_window_manager
from desktop_env.taskbar import start_taskbar
from desktop_env.wallpaper import set_wallpaper_from_config
from desktop_env.settings import start_settings_app
def start_settings_app():
    app = QApplication(sys.argv)

    with open("config.json", "r") as f:
        config = json.load(f)
    theme = config.get("theme", "light")
    if theme == "dark":
        app.setStyleSheet(open("dark.qss").read())
    else:
        app.setStyleSheet(open("light.qss").read())

    win = SettingsWindow()
    win.show()
    app.exec_()

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
