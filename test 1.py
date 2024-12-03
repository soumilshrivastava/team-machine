from plyer import notification
import psutil
import time

def check_battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged

    if plugged:  # If the charger is connected
        if percent >= 80:
            notification.notify(
                title="Battery Status",
                message="Battery is fully charged. Please unplug to extend battery life.",
                timeout=5
            )
        elif percent == 100:
            notification.notify(
                title="Battery Status",
                message="Battery is at 100%. Unplug the charger!",
                timeout=5
            )
    else:  # If the charger is not connected
        if percent <= 20:
            notification.notify(
                title="Battery Low",
                message="Battery is low! Please plug in your charger.",
                timeout=5
            )
        elif percent <= 75:
            notification.notify(
                title="Battery Status",
                message=f"Battery is at {percent}%. Consider charging soon.",
                timeout=5
            )

if __name__ == "_main_":
    while True:
        check_battery_status()
        time.sleep(60)  # Check every minute