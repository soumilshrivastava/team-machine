import psutil
import time
from plyer import notification

def monitor_ram_usage(threshold=80, check_interval=5):
    """
    Monitor RAM usage and alert if usage exceeds a specified threshold.

    Args:
        threshold (int): The percentage usage threshold for alerts. Default is 80%.
        check_interval (int): The interval (in seconds) between checks. Default is 5 seconds.
    """
    try:
        print(f"Monitoring RAM usage. Alert threshold set to {threshold}%. Press Ctrl+C to stop.")
        while True:
            # Get memory usage
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent

            # Check if memory usage exceeds threshold
            if memory_usage > threshold:
                notification.notify(
                    title="High RAM Usage Alert",
                    message=(
                        f"RAM Usage is at {memory_usage}%.\n"
                        f"Used: {memory_info.used / (1024**3):.2f} GB, "
                        f"Total: {memory_info.total / (1024**3):.2f} GB.\n"
                        "Consider closing unused applications."
                    ),
                    timeout=10
                )
                print(
                    f"High RAM usage detected: {memory_usage}% "
                    f"(Used: {memory_info.used / (1024**3):.2f} GB, Total: {memory_info.total / (1024**3):.2f} GB)"
                )

            # Wait for the next check
            time.sleep(check_interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
if __name__ == "__main__":
    monitor_ram_usage(threshold=80, check_interval=5)
