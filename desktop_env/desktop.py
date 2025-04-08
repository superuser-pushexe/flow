import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QIcon

class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.setGeometry(QDesktopWidget().screenGeometry())
        self.setStyleSheet("background: transparent;")

        self.icons = []
        self.load_desktop_items()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_desktop_context_menu)

    def load_desktop_items(self):
        for icon in self.icons:
            icon.deleteLater()
        self.icons.clear()
        desktop_path = os.path.expanduser("~/Desktop")
        for item in os.listdir(desktop_path):
            item_path = os.path.join(desktop_path, item)
            icon = QLabel(self)
            icon.setPixmap(QIcon.fromTheme("folder" if os.path.isdir(item_path) else "text-x-generic").pixmap(48, 48))
            icon.setText(item)
            icon.setAlignment(Qt.AlignCenter)
            icon.setStyleSheet("color: white; font-size: 12px;")
            icon.setGeometry(50 + len(self.icons) * 100, 50, 80, 80)
            icon.setContextMenuPolicy(Qt.CustomContextMenu)
            icon.customContextMenuRequested.connect(lambda pos, i=icon: self.show_context_menu(pos, i, item_path))
            icon.mousePressEvent = lambda e, i=icon: self.start_drag(e, i)
            self.icons.append(icon)

    def show_context_menu(self, pos, icon, path):
        menu = QMenu(self)
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: os.system(f"xdg-open '{path}'"))
        menu.addAction(open_action)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: (shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)) or self.load_desktop_items())
        menu.addAction(delete_action)
        menu.exec_(icon.mapToGlobal(pos))

    def show_desktop_context_menu(self, pos):
        menu = QMenu(self)
        new_folder_action = QAction("New Folder", self)
        new_folder_action.triggered.connect(self.create_new_folder)
        menu.addAction(new_folder_action)
        menu.exec_(self.mapToGlobal(pos))

    def create_new_folder(self):
        desktop_path = os.path.expanduser("~/Desktop")
        base_name = "New Folder"
        new_folder = os.path.join(desktop_path, base_name)
        counter = 1
        while os.path.exists(new_folder):
            new_folder = os.path.join(desktop_path, f"{base_name} {counter}")
            counter += 1
        os.makedirs(new_folder)
        self.load_desktop_items()

    def start_drag(self, event, icon):
        if event.buttons() == Qt.LeftButton:
            self.drag_start_pos = event.pos()
            self.dragged_icon = icon

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, "dragged_icon"):
            delta = event.pos() - self.drag_start_pos
            self.dragged_icon.move(self.dragged_icon.pos() + delta)

    def mouseReleaseEvent(self, event):
        self.dragged_icon = None

def start_desktop():
    app = QApplication([])
    desktop = Desktop()
    desktop.show()
    app.exec_()
