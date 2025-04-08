import psutil
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer, QTime

class SystemTray(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.clock = QLabel()
        self.volume = QLabel("🔊")
        self.battery = QLabel()
        self.network = QLabel()

        layout.addWidget(self.network)
        layout.addWidget(self.battery)
        layout.addWidget(self.volume)
        layout.addWidget(self.clock)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)
        self.update_status()

    def update_status(self):
        # Clock
        current_time = QTime.currentTime().toString("HH:mm")
        self.clock.setText(current_time)

        # Battery
        battery = psutil.sensors_battery()
        if battery:
            self.battery.setText(f"🔋 {int(battery.percent)}%")
        else:
            self.battery.setText("🔋 N/A")

        # Network (simplified)
        self.network.setText("📶")
