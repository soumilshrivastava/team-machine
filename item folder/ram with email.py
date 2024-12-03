import psutil
import time
import smtplib

def send_email_alert(sender_email, receiver_email, sender_password, subject, message):
    """
    Send an email alert.
    
    Args:
        sender_email (str): Sender's email address.
        receiver_email (str): Receiver's email address.
        sender_password (str): Sender's email password (or app password).
        subject (str): Email subject.
        message (str): Email body.
    """
    try:
        # Format email
        email_text = f"Subject: {subject}\n\n{message}"
        
        # Set up SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, email_text)
        
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_ram_usage_with_email(threshold=80, check_interval=5, email_config=None):
    """
    Monitor RAM usage and send an email alert if usage exceeds a specified threshold.
    
    Args:
        threshold (int): Percentage usage threshold for alerts. Default is 80%.
        check_interval (int): Time interval (in seconds) between checks. Default is 5 seconds.
        email_config (dict): Email configuration with sender_email, receiver_email, and sender_password.
    """
    try:
        if not email_config:
            raise ValueError("Email configuration is missing.")
        
        print(f"Monitoring RAM usage. Alert threshold set to {threshold}%. Press Ctrl+C to stop.")
        
        while True:
            # Get memory usage
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent

            # Check if memory usage exceeds threshold
            if memory_usage > threshold:
                subject = "High RAM Usage Alert"
                message = (
                    f"RAM Usage is at {memory_usage}%.\n"
                    f"Used: {memory_info.used / (1024**3):.2f} GB, "
                    f"Total: {memory_info.total / (1024**3):.2f} GB.\n"
                    "Consider closing unused applications."
                )
                # Send email alert
                send_email_alert(
                    sender_email=email_config["sender_email"],
                    receiver_email=email_config["receiver_email"],
                    sender_password=email_config["sender_password"],
                    subject=subject,
                    message=message
                )

            # Wait for the next check
            time.sleep(check_interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Configuration for email
email_config = {
    "sender_email": "pd3366990@gmail.com",
    "receiver_email": "pokemon190108@gmail.com",
    "sender_password": "tkjjwtpoivilehdv"  # Use an app password for Gmail
}

# Call the function
if __name__ == "__main__":
    monitor_ram_usage_with_email(threshold=10, check_interval=5, email_config=email_config)
