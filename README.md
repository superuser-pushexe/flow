# Flow Desktop
# This respository is archived. Visit the new one at: https://github.com/superuser-pushexe/Flow-Desktop
(refractored to C)

A lightweight, customizable desktop environment built with Python, PyQt5, and Xlib. Flow Desktop aims to provide a lightweight, modern desktop experience similar to other major desktops, with features like desktop icons, a taskbar with app launcher, system tray, and window management.

## Website 
https://superuser-pushexe.github.io/
## Features
- **Desktop Icons**: View and interact with files/folders on the desktop with drag-and-drop and context menus.
- **Taskbar**: Includes an app launcher with search, window previews, and a system tray showing clock, battery, and network status.
- **Window Management**: Supports window dragging, snapping (left/right), minimize (Alt+M), and maximize/restore (Alt+F).
- **Settings App**: Customize wallpaper, taskbar position, theme colors, and manage taskbar apps.
- **Cross-Platform Wallpaper**: Wallpaper support for Linux, Windows, and macOS.

## Requirements
- Python 3.x
- PyQt5 (`pip install PyQt5`)
- Xlib (Linux only, `pip install python-xlib`)
- psutil (`pip install psutil`)

## Installation
### 1. Clone the repository:
git clone https://github.com/superuser-pushexe/flow.git
cd flow

### 2. Install dependencies:
pip install -r requirements.txt

Or manually: `pip install PyQt5 python-xlib psutil`
### 3. Run the desktop:
python main.py

## Usage
- **Taskbar**: Click the logo button to open the app launcher. Search and launch apps from the grid.
- **Desktop**: Right-click files/folders to open or delete them. Drag to reposition.
- **Window Management**:
- Drag windows to snap them to the left/right half of the screen.
- Press `Alt+M` to minimize a window.
- Press `Alt+F` to maximize/restore a window.
- **Settings**: Use the settings app to change wallpaper, taskbar position, theme colors, and manage apps.

## Configuration
Edit `config.json` to customize:
- `wallpaper`: Path to your wallpaper image.
- `taskbar_position`: `"top"` or `"bottom"`.
- `apps`: List of apps in the taskbar (e.g., `[{"name": "Terminal", "command": ["x-terminal-emulator"]}]`).

## Contributing
Feel free to submit issues or pull requests to improve Flow Desktop!
