import ssl
import socket
import smtplib
import os
import requests
import time
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv
import logging

# Load .env file from custom path
load_dotenv(dotenv_path="/path/to/your/.env")

# Logging setup
log_file = "/path/to/your/ssl_monitor.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Configuration
websites = ['your.domain1.com', 'your.domain2.com']
threshold_days = 30

email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")

# Pull cached SSL grade if <3h old, else trigger new scan
def get_ssl_grade(domain, max_retries=5, retry_delay=180):
    url = "https://api.ssllabs.com/api/v3/analyze"
    params_cache = {"host": domain, "fromCache": "on", "maxAge": 10800}  # 3 hours cache
    params_fresh = {"host": domain, "startNew": "on"}

    try:
        response = requests.get(url, params=params_cache, timeout=10)
        data = response.json()
        if data.get("status") == "READY":
            endpoints = data.get("endpoints", [])
            if endpoints:
                return endpoints[0].get("grade", "No grade (cached)")
        else:
            logging.info(f"{domain}: Cache miss or status {data.get('status')} — starting fresh scan")
    except Exception as e:
        logging.warning(f"{domain}: Failed cache check — {e}")

    # Start new scan
    try:
        requests.get(url, params=params_fresh, timeout=10)
        for _ in range(max_retries):
            time.sleep(retry_delay)
            response = requests.get(url, params=params_cache, timeout=10)
            data = response.json()
            if data.get("status") == "READY":
                endpoints = data.get("endpoints", [])
                if endpoints:
                    return endpoints[0].get("grade", "No grade (new)")
    except Exception as e:
        return f"Error: {e}"
    return "Timed out"

# SSL expiration check
def get_ssl_expiry(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            return expiry

# Build HTML alert + collect data
def check_certificates():
    alerts = []
    html_rows = ""

    for site in websites:
        try:
            expiry = get_ssl_expiry(site)
            days_left = (expiry - datetime.utcnow()).days
            grade = get_ssl_grade(site)

            row_color = "#ffcccc" if days_left < threshold_days else "#ccffcc"
            html_rows += f"""
            <tr style="background-color:{row_color}">
                <td>{site}</td>
                <td>{expiry.strftime('%Y-%m-%d')}</td>
                <td>{days_left}</td>
                <td>{grade}</td>
            </tr>"""

            log_msg = f"{site} | Expires: {expiry.strftime('%Y-%m-%d')} | Days left: {days_left} | Grade: {grade}"
            logging.info(log_msg)
            alerts.append(log_msg)

        except Exception as e:
            err_msg = f"{site} ERROR: {e}"
            html_rows += f"""
            <tr style="background-color:#ffdddd">
                <td>{site}</td>
                <td colspan="3">{e}</td>
            </tr>"""
            logging.error(err_msg)
            alerts.append(err_msg)

    return alerts, html_rows

# Send HTML-formatted email
def send_email(alerts, html_table_rows):
    if not alerts:
        logging.info("No alerts to send.")
        return

    html_body = f"""
    <html>
        <body>
            <h2>SSL Certificate Report</h2>
            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
                <tr style="background-color:#f2f2f2">
                    <th>Domain</th>
                    <th>Expiry Date</th>
                    <th>Days Remaining</th>
                    <th>Grade</th>
                </tr>
                {html_table_rows}
            </table>
        </body>
    </html>
    """

    msg = EmailMessage()
    msg['Subject'] = "🔐 SSL Certificate Report"
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg.set_content("This email contains HTML content. Please view in an HTML-compatible email client.")
    msg.add_alternative(html_body, subtype='html')

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        logging.info("Alert email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send alert email: {e}")

# Entrypoint
if __name__ == "__main__":
    logging.info("Running SSL check...")
    alerts, html_rows = check_certificates()
    send_email(alerts, html_rows)
