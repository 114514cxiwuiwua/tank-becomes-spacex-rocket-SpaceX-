import json
import time
import threading
from datetime import datetime
from plyer import notification
import os

# Function to write daily playtime data to a JSON file
def write_playtime_data(playtime_data):
    with open('playtime_data.json', 'w') as f:
        json.dump(playtime_data, f)

# Function to show notifications based on game playtime
def show_notification(level):
    messages = {
        'light': "You've been playing for 1 hour. Remember to take a break!",
        'moderate': "You've been playing for 2 hours. It's time to stretch!",
        'severe': "You've been playing for 4 hours. Consider taking a longer break!",
        'hospital': "You've been playing for 6 hours. Please visit a hospital!"
    }
    notification.notify(
        title='War Thunder Health Alert',
        message=messages[level],
        timeout=10
    )

# Function to monitor playtime
def monitor_playtime():
    playtime_data = {'date': datetime.now().strftime('%Y-%m-%d'), 'playtime_hours': 0}
    start_time = datetime.now()

    while True:
        time.sleep(3600)  # Wait for 1 hour
        playtime_data['playtime_hours'] += 1

        if playtime_data['playtime_hours'] == 1:
            show_notification('light')
        elif playtime_data['playtime_hours'] == 2:
            show_notification('moderate')
        elif playtime_data['playtime_hours'] == 4:
            show_notification('severe')
        elif playtime_data['playtime_hours'] == 6:
            show_notification('hospital')
            break  # Stop monitoring after 6 hours

        write_playtime_data(playtime_data)

# Function to request user consent
def request_user_consent():
    consent = input("Do you consent to monitor your game playtime for health alerts? (yes/no): ")
    return consent.lower() == 'yes'

if __name__ == '__main__':
    if request_user_consent():
        print("Starting War Thunder Health Monitor...")
        monitor_thread = threading.Thread(target=monitor_playtime)
        monitor_thread.start()
    else:
        print("User did not consent. Exiting...")

# Disclaimer: This program tracks virtual health data for entertainment purposes only. Play responsibly!