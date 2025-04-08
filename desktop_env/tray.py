from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer, QTime

class SystemTray(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.clock = QLabel()
        self.volume = QLabel("🔊")  # Placeholder

        layout.addWidget(self.volume)
        layout.addWidget(self.clock)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm")
        self.clock.setText(current_time)
