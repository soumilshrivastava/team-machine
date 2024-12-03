import psutil
import smtplib
from email.message import EmailMessage
import time

def send_email_alert(subject, message, sender_email, receiver_email, sender_password):
    """
    Sends an email alert.

    Args:
        subject (str): Subject of the email.
        message (str): Body of the email.
        sender_email (str): Sender's email address.
        receiver_email (str): Receiver's email address.
        sender_password (str): Sender's email password or app password.
    """
    try:
        # Configure the email
        email = EmailMessage()
        email['From'] = sender_email
        email['To'] = receiver_email
        email['Subject'] = subject
        email.set_content(message)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email)
        print(f"Email sent to {receiver_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_disk_usage(threshold=20):
    """
    Monitors disk usage and sends an email alert if usage exceeds the threshold.

    Args:
        threshold (int): Usage percentage threshold for alerts. Default is 80%.
    """
    sender_email = "pd3366990@gmail.com"  # Sender's email
    sender_password = "tkjjwtpoivilehdv"  # App password for the sender's email
    receiver_email = "pokemon190108@gmail.com"  # Receiver's email

    try:
        while True:
            # Get all disk partitions
            partitions = psutil.disk_partitions()

            for partition in partitions:
                try:
                    # Get disk usage statistics for the partition
                    usage = psutil.disk_usage(partition.mountpoint)

                    # Check if usage exceeds the threshold
                    if usage.percent > threshold:
                        subject = "High Disk Usage Alert"
                        message = (
                            f"Partition: {partition.device}\n"
                            f"Mountpoint: {partition.mountpoint}\n"
                            f"Usage: {usage.percent}%\n"
                            f"Used: {usage.used / (1024**3):.2f} GB\n"
                            f"Total: {usage.total / (1024**3):.2f} GB\n"
                        )
                        send_email_alert(subject, message, sender_email, receiver_email, sender_password)

                except PermissionError:
                    # Skip partitions that are inaccessible
                    continue
            
            # Wait before checking again
            time.sleep(60)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Start monitoring
if __name__ == "__main__":
    monitor_disk_usage(threshold=20)
