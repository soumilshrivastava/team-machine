import psutil
from plyer import notification
import smtplib
from email.message import EmailMessage
from threading import Thread
import time


def send_email(subject, body, sender_email, receiver_email, email_password):
    """
    Send an email with the specified subject and body.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        sender_email (str): The sender's email address.
        receiver_email (str): The recipient's email address.
        email_password (str): The sender's email password or app password.
    """
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(msg)
        print(f"Email sent to {receiver_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def monitor_cpu_memory(threshold=80, email_alert=True):
    """
    Monitor CPU and memory usage, alerting and sending emails if thresholds are exceeded.

    Args:
        threshold (int): The usage percentage threshold for alerts. Default is 80%.
        email_alert (bool): Whether to send email alerts. Default is True.
    """
    sender_email = 'pd3366990@gmail.com'
    receiver_email = 'pokemon190108@gmail.com'
    email_password = 'tkjjwtpoivilehdv'  # Replace with your app password

    print(f"Monitoring CPU and memory usage. Alerts triggered at >{threshold}% usage.")
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent

            if cpu_usage > threshold:
                notification.notify(
                    title="High CPU Usage Alert",
                    message=f"CPU Usage is at {cpu_usage}%. Consider closing some applications.",
                    timeout=10
                )
                if email_alert:
                    send_email(
                        "High CPU Usage Alert",
                        f"CPU Usage is at {cpu_usage}%. Please take action.",
                        sender_email,
                        receiver_email,
                        email_password
                    )

            if memory_usage > threshold:
                notification.notify(
                    title="High Memory Usage Alert",
                    message=f"Memory Usage is at {memory_usage}%. Consider freeing up some memory.",
                    timeout=10
                )
                if email_alert:
                    send_email(
                        "High Memory Usage Alert",
                        f"Memory Usage is at {memory_usage}%. Please take action.",
                        sender_email,
                        receiver_email,
                        email_password
                    )

            time.sleep(5)
    except KeyboardInterrupt:
        print("CPU and memory monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")


def monitor_battery_and_send_email(threshold=20, email_alert=True):
    """
    Monitor battery level and send notifications/emails if below the threshold.

    Args:
        threshold (int): The battery level percentage threshold for sending an alert.
        email_alert (bool): Whether to send email alerts. Default is True.
    """
    sender_email = 'pd3366990@gmail.com'
    receiver_email = 'pokemon190108@gmail.com'
    email_password = 'tkjjwtpoivilehdv'  # Replace with your app password

    print(f"Monitoring battery level. Alert if it drops below {threshold}%.")
    try:
        while True:
            battery = psutil.sensors_battery()
            if battery is None:
                print("Battery information is not available on this system.")
                return

            percent = battery.percent
            plugged = battery.power_plugged

            if percent < threshold and not plugged:
                notification.notify(
                    title="Low Battery Alert",
                    message=f"Battery level is critically low at {percent}%. Please plug in the charger.",
                    timeout=10
                )
                if email_alert:
                    send_email(
                        "Low Battery Alert",
                        f"Battery level is critically low at {percent}%. Please plug in the charger.",
                        sender_email,
                        receiver_email,
                        email_password
                    )

                time.sleep(300)  # Wait 5 minutes to prevent spam
            else:
                print(f"Battery level: {percent}%. Plugged in: {'Yes' if plugged else 'No'}.")
            
            time.sleep(60)
    except KeyboardInterrupt:
        print("Battery monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        # Run CPU/memory monitoring and battery monitoring in parallel
        cpu_thread = Thread(target=monitor_cpu_memory, args=(80,))
        battery_thread = Thread(target=monitor_battery_and_send_email, args=(20,))

        cpu_thread.start()
        battery_thread.start()

        cpu_thread.join()
        battery_thread.join()
    except KeyboardInterrupt:
        print("System monitoring stopped.")
