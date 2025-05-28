import shutil
import smtplib
from email.mime.text import MIMEText
import socket
from datetime import datetime
import subprocess

# Configuration
THRESHOLD = 80
EMAIL = "your_email@example.com"
SUBJECT = f"Disk Usage Alert on {socket.gethostname()}"

# Function to get disk usage info
def get_disk_usage():
    partitions = []
    df_output = subprocess.check_output(["df", "-h"]).decode("utf-8").splitlines()
    for line in df_output:
        if line.startswith("/dev/"):
            parts = line.split()
            usage_percent = int(parts[4].strip('%'))
            mount_point = parts[5]
            partitions.append((mount_point, usage_percent))
    return partitions

# Function to send email
def send_email(subject, message, to_email):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = "alert@yourdomain.com"
    msg["To"] = to_email

    try:
        # Adjust SMTP settings as per your environment
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main logic
for mount_point, usage in get_disk_usage():
    if usage >= THRESHOLD:
        message = f"Warning: Disk usage on {mount_point} has reached {usage}% on {socket.gethostname()} at {datetime.now()}"
        print(message)
        send_email(SUBJECT, message, EMAIL)
