import psutil
from plyer import notification
import time

def monitor_cpu(threshold=80):
    """
    Monitor CPU usage and send an alert if it exceeds the threshold.

    Args:
        threshold (int): The CPU usage percentage threshold for alerts.
    """
    try:
        while True:
            # Get current CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)

            # Check if CPU usage exceeds threshold
            if cpu_usage > threshold:
                notification.notify(
                    title="High CPU Usage Alert",
                    message=f"CPU Usage is at {cpu_usage}%. Consider closing some applications.",
                    timeout=10  # Notification disappears after 10 seconds
                )

            time.sleep(5)  # Check CPU usage every 5 seconds
    except KeyboardInterrupt:
        print("CPU Monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the monitoring function
if __name__ == "__main__":
    monitor_cpu(threshold=10)