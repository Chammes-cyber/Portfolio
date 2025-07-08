import os
import platform
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Ping configuration
primary_service = "8.8.8.8" # Primary IP to ping
backup_service = "8.8.8.8" # Second IP to ping if primary is unreachable
ping_interval = 1
alert_sent = False
service_down = False

# Read and add emails to notification
def load_recipients_from_file(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"ERROR: Could not find {filename}. No emails loaded.")
        return []

# Email configuration

smtp_server = "smtp.office365.com"
smtp_port = 587
sender_email = "" # Enter senders email address
sender_password = "" # Enter senders eamil password
recipients = load_recipients_from_file("EXAMPLE.txt")

# Service down email structure

def send_email(subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())
            print(f"Email sent: {subject}")
    except Exception as e:
        print("Email failed: {e}")

def send_outage_alert():
    subject = "⚠️ Service Alert: Service Outage"
    body = """
    <html>
        <body>
            <h3>🚨 Service Outage Detected</h3>
            <p>YOUR_COMPANY is currently experienceing a service outage.</p>
            <p>We're currently investigating the issue and will provide an update shortly.</p>
        </body>
    </html>
    """
    send_email(subject, body)

# Service recovery email structure

def send_recovery_alert():
    subject = "✅ Service Restored: Services Are Back Online"
    body = """
    <html>
        <body>
            <h3>✅ Service Restored</h3>
            <p>The service issue has been corrected.</p>
            <p>We apologize about the inconvenience and will continue monitoring for stability at this time.</p>
        </body>
    </html>
    """
    send_email(subject, body)

# Ping command parameters depending on os

param = "-n" if platform.system().lower() == "windows" else "-c"

# Determine if alert needs to be sent out

print(f"Pinging {primary_service} every {ping_interval} seconds.")

try:
    while True:
        response = os.system(f"ping {param} 1 {primary_service}")
        if response == 0:
            print(f"{primary_service} is reachable!")
        if service_down:
            send_recovery_alert()
            service_down = False
            alert_sent = False
        else:
            print(f"{primary_service} is unreachable! Pinging backup serive {backup_service} to verify outage.")
            backup_response = os.system(f"ping {param} 1 {backup_service}")
            if backup_response == 0:
                print(f"{backup_service} is reachable. Possible issue with panel.")
            else:
                print(f"{backup_service} is also unreachable. Possible site power outage.")
            if not alert_sent:
                send_outage_alert()
                alert_sent = True
                service_down = True

        time.sleep(ping_interval)

except KeyboardInterrupt:
    print("\nStopped by admin.")
