import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from utils.database import get_smtp_config
from config import SMTP_HOST, SMTP_PORT

def send_alert(score, ip_address, tx_hash, user_id=None):
    config = get_smtp_config(user_id)
    if not config:
        return False, "SMTP not configured"

    sender = config["sender_email"]
    password = config["sender_password"]
    recipient = config["recipient_email"]

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Intrusion Detected - QuantumShield Alert"
        msg["From"] = sender
        msg["To"] = recipient

        body = f"""
        <html>
        <body>
        <h2>Intrusion Detected</h2>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>IP Address:</strong> {ip_address}</p>
        <p><strong>Confidence Score:</strong> {score:.4f} ({score * 100:.2f}%)</p>
        <p><strong>Blockchain TX Hash:</strong> {tx_hash}</p>
        <p>This event has been logged to the blockchain ledger.</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())

        return True, "Alert sent"
    except Exception as e:
        return False, str(e)