import threading
from desktop_env.wm import start_window_manager
from desktop_env.taskbar import start_taskbar
from desktop_env.wallpaper import set_wallpaper_from_config
from desktop_env.settings import start_settings_app

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
