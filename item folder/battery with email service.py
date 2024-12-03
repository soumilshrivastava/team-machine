import smtplib
import psutil
import time
from email.message import EmailMessage

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
    # Create the email message
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(msg)
        print(f"Email sent to {receiver_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_battery_and_send_email(threshold=20):
    """
    Monitor battery level and send an email if it drops below the threshold.

    Args:
        threshold (int): The battery level percentage threshold for sending an alert.
    """
    # Email configuration
    sender_email = 'pd3366990@gmail.com'
    receiver_email = 'pokemon190108@gmail.com'
    email_password = 'tkjjwtpoivilehdv'  # Replace with your app password

    print(f"Monitoring battery level. Alert if it drops below {threshold}%.")
    try:
        while True:
            # Get battery status
            battery = psutil.sensors_battery()
            if battery is None:
                print("Battery information is not available on this system.")
                return

            percent = battery.percent
            plugged = battery.power_plugged

            # Check if battery level drops below the threshold and charger is not plugged in
            if percent < threshold and not plugged:
                subject = "Low Battery Alert!"
                body = f"Battery level is critically low at {percent}%. Please plug in the charger immediately."
                send_email(subject, body, sender_email, receiver_email, email_password)

                # Prevent spamming by waiting longer after sending an email
                time.sleep(300)  # Wait for 5 minutes before recheckingś
            else:
                print(f"Battery level: {percent}%. Plugged in: {'Yes' if plugged else 'No'}.")

            time.sleep(60)  # Regular check every 1 minute
    except KeyboardInterrupt:
        print("Battery monitoring stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    monitor_battery_and_send_email(threshold=99)
