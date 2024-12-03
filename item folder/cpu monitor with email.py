import psutil
import smtplib
from email.message import EmailMessage
from plyer import notification
import time

def send_email(cpu_usage, sender_email, receiver_email, email_password):
    """
    Send an email alert about high CPU usage.

    Args:
        cpu_usage (float): The current CPU usage percentage.
        sender_email (str): The sender's email address.
        receiver_email (str): The receiver's email address.
        email_password (str): The sender's email password or app password.
    """
    subject = "High CPU Usage Alert!"
    body = f"Warning: CPU usage has reached {cpu_usage}%. Immediate action is required to reduce the load."

    # Create the email message
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(em)
        print(f"Email alert sent to {receiver_email}.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

def monitor_cpu(threshold=99, email_alert=True):
    """
    Monitor CPU usage and send alerts when it exceeds the threshold.

    Args:
        threshold (int): The CPU usage percentage threshold for alerts.
        email_alert (bool): Whether to send email alerts for high CPU usage.
    """
    # Email configuration
    sender_email = 'pd3366990@gmail.com'
    receiver_email = 'pokemon190108@gmail.com'
    email_password = 'tkjjwtpoivilehdv'  # Replace with your app password

    print(f"Monitoring CPU usage. Alert threshold set to {threshold}%.")
    try:
        while True:
            # Get current CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)

            if cpu_usage > threshold:
                # Send desktop notification
                notification.notify(
                    title="High CPU Usage Alert",
                    message=f"CPU Usage is at {cpu_usage}%. Immediate action is recommended.",
                    timeout=10
                )
                print(f"High CPU usage detected: {cpu_usage}%")

                # Send email alert if enabled
                if email_alert:
                    send_email(cpu_usage, sender_email, receiver_email, email_password)

            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("CPU monitoring stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    monitor_cpu()
