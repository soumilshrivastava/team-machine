import psutil
from plyer import notification
import time

def monitor_disk_usage(threshold=80):
    """
    Monitor disk partitions and usage, alerting if any partition exceeds the threshold.

    Args:
        threshold (int): The usage percentage threshold for alerts. Default is 80%.
    """
    try:
        while True:
            # Get all disk partitions
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    # Get disk usage statistics for the partition
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Check if usage exceeds threshold
                    if usage.percent > threshold:
                        notification.notify(
                            title="High Disk Usage Alert",
                            message=(
                                f"Partition: {partition.device}\n"
                                f"Mountpoint: {partition.mountpoint}\n"
                                f"Usage: {usage.percent}% (Used: {usage.used / (1024**3):.2f} GB, "
                                f"Total: {usage.total / (1024**3):.2f} GB)"
                            ),
                            timeout=10  # Notification disappears after 10 seconds
                        )
                except PermissionError:
                    # Skip partitions that are inaccessible
                    continue
            
            # Wait for 5 seconds before checking again
            time.sleep(5)
    except KeyboardInterrupt:
        print("Disk monitoring stopped by the user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Call the function with the default threshold
if __name__ == "__main__":
    monitor_disk_usage(threshold=80)
