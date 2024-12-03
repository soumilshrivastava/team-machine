import psutil
from plyer import notification
import time
from threading import Thread

def monitor_cpu_memory(threshold=80):
    """
    Monitor CPU and memory usage, alerting if thresholds are exceeded.
    """
    try:
        while True:
            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            # Get memory usage
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent

            # Check if CPU usage exceeds threshold
            if cpu_usage > threshold:
                notification.notify(
                    title="High CPU Usage Alert",
                    message=f"CPU Usage is at {cpu_usage}%. Consider closing some applications.",
                    timeout=10
                )

            # Check if Memory usage exceeds threshold
            if memory_usage > threshold:
                notification.notify(
                    title="High Memory Usage Alert",
                    message=f"Memory Usage is at {memory_usage}%. Consider freeing up some memory.",
                    timeout=10
                )

            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("CPU and Memory monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

def monitor_disk_usage(threshold=8):
    """
    Monitor disk partitions and usage, alerting if any partition exceeds the threshold.
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
                            timeout=10
                        )
                except PermissionError:
                    # Some partitions may not be accessible; skip them
                    continue
            
            # Wait for 5 seconds before the next check
            time.sleep(15)
    except KeyboardInterrupt:
        print("Disk usage monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Create threads for both monitors
    cpu_memory_thread = Thread(target=monitor_cpu_memory, args=(80,))
    disk_usage_thread = Thread(target=monitor_disk_usage, args=(40,))

    # Start both threads
    cpu_memory_thread.start()
    disk_usage_thread.start()

    # Keep the main thread alive while the monitoring threads run
    cpu_memory_thread.join()
    disk_usage_thread.join()
