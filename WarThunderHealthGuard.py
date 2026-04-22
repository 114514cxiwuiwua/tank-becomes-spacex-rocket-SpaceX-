import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon, QMenu
import psutil
import time
import threading

class WarThunderHealthGuard:
    def __init__(self):
        self.playtime_limit = 2 * 60 * 60  # 2 hours in seconds
        self.playtime_recorded = 0
        self.network_throttling = True
        self.autostart = False
        self.initial_consent = False
        self.initUI()

    def initUI(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon('icon.png'))  # Replace with a valid icon path
        self.tray_icon.setVisible(True)

        # Create context menu for the systray icon
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit)
        self.tray_icon.setContextMenu(menu)

        self.tray_icon.activated.connect(self.on_icon_click)

        self.request_user_consent()

    def request_user_consent(self):
        reply = QMessageBox.question(None, 'Consent Required', 'Do you consent to the application running?','Yes', 'No')
        if reply == QMessageBox.Yes:
            self.initial_consent = True
            self.start_monitoring()
        else:
            sys.exit(0)

    def start_monitoring(self):
        self.playtime_thread = threading.Thread(target=self.monitor_playtime)
        self.playtime_thread.start()

    def monitor_playtime(self):
        while True:
            if self.initial_consent:
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] == 'WarThunder.exe':  # Adjust if necessary
                        self.playtime_recorded += 1
                        time.sleep(1)
                        if self.playtime_recorded > self.playtime_limit:
                            self.handle_limit_exceeded()
                            break
            time.sleep(1)

    def handle_limit_exceeded(self):
        if self.network_throttling:
            self.simulate_network_throttling()
        self.notify_user("Playtime limit exceeded!")

    def simulate_network_throttling(self):
        # Simulate network throttling (1KB upload)
        pass  # Implementation details required

    def notify_user(self, message):
        self.tray_icon.showMessage('Notification', message, QSystemTrayIcon.Information, 2000)

    def on_icon_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.notify_user("Application is running")  # Provide current status

    def exit(self):
        self.tray_icon.hide()
        sys.exit(0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = WarThunderHealthGuard()
    sys.exit(app.exec_())
