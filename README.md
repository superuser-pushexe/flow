 # Flow: A Python X11 Desktop Environment

A **minimal X11 desktop environment** written (almost) entirely in **Python 3.12**, featuring:

- ✅ Custom wallpaper support  
- ✅ Floating window manager  
- ✅ Taskbar built with PyQt5  
- ✅ GUI settings app to change the wallpaper  
- ✅ Optional `.deb` installer for easy system integration  

> ⚠️ This project is experimental and built as a lightweight alternative DE. Not intended for production desktops yet.

---


## 📦 Features

| Component         | Description                                  |
|------------------|----------------------------------------------|
| **Window Manager**   | Handles basic map requests (floating)        |
| **Taskbar**          | PyQt5 panel that stays on top                |
| **Wallpaper Support**| Set using `feh` based on user config         |
| **Settings App**     | GUI to change wallpaper via file dialog      |
| **Session Support**  | Launchable from display managers (LightDM)   |

---

## 🚀 Getting Started

###  Requirements

- Python 3.12+
- `PyQt5`
- `python-xlib`
- `feh` (for wallpaper management)
- An X11 environment (e.g., Xorg)

---

### 📦 Install Dependencies
`sudo apt update
sudo apt install feh
pip install -r requirements.txt`

---

### 🖥️ Running the Desktop Manually
To run the desktop manually, use the following command:

`python3 desktop_env/main.py`
This will start the desktop environment directly from your terminal.

### 🧱 Building and Installing the .deb Package (Optional)
#### 🛠 Step 1: Build the .deb Package
`chmod +x build_deb.sh
./build_deb.sh`
#### 📥 Step 2: Install the Package
`sudo dpkg -i python-desktop-x11_1.0_all.deb
sudo apt --fix-broken install`
#### 🧪 Step 3: Use the Desktop
Log out and select "Python Desktop" from your session manager (e.g., LightDM or GDM).

### 📁 Project Structure


```text
python-desktop-x11/
├── desktop_env/              # Core desktop components
│   ├── main.py               # Entry point
│   ├── wm.py                 # Window manager
│   ├── taskbar.py            # Taskbar UI
│   ├── wallpaper.py          # Wallpaper setter
│   ├── settings.py           # Settings GUI
│   └── config.json           # User configuration
├── debian/                   # Debian packaging structure
│   ├── DEBIAN/
│   │   ├── control           # Package metadata
│   │   └── postinst          # Post-install script
│   └── usr/share/xsessions/
│       └── python-desktop.desktop
├── requirements.txt          # Python dependencies
├── build_deb.sh              # .deb package builder
├── LICENSE
└── README.md
```

### 🖼 Customizing the Wallpaper
#### Option 1: Manually edit the config file
Edit the config.json file:

`{
  "wallpaper": "/usr/share/backgrounds/default.jpg"
}`
#### Option 2: Use the GUI settings app

`python3 desktop_env/settings.py`
This opens a file dialog where you can pick an image. It will update the config automatically and refresh your wallpaper.

### ❓ FAQ
#### Can I use this as my daily driver?
Not recommended. This is a minimal, experimental desktop for educational or hacking purposes.

#### Does it support Wayland?
No — this project only works with X11.

#### Can I run this inside a VM or Xephyr?
Yes! That’s a great way to test it without logging out of your current session.

### 📃 License
This project is licensed under the GPLv3 License.

### 🙌 Credits
PyQt5

python-xlib

feh

### 🤝 Contributing
Pull requests are welcome!

If you'd like to add features, fix bugs, or request enhancements, feel free to open an issue.
