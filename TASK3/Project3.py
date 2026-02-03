
#File: email_sender.py
import smtplib
import csv
import time
import logging
from email.message import EmailMessage
import os

# ---------- CONFIG ----------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"   # Gmail App Password
ATTACHMENT_PATH = "report.pdf"

LOG_FILE = "email_log.txt"

# ---------- Logging ----------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_email(to_email, name, retries=3):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Monthly Report"

    msg.set_content(
        f"""Hello {name},

Please find the attached report.

Regards,
Automation Bot
"""
    )

    # Attach file
    if os.path.exists(ATTACHMENT_PATH):
        with open(ATTACHMENT_PATH, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(ATTACHMENT_PATH)
            )

    for attempt in range(1, retries + 1):
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)

            logging.info(f"Email sent to {to_email}")
            print(f"✅ Email sent to {to_email}")
            return

        except Exception as e:
            logging.error(f"Attempt {attempt} failed for {to_email}: {e}")
            print(f"❌ Attempt {attempt} failed for {to_email}")
            time.sleep(2)

    logging.error(f"Email failed after retries: {to_email}")

# ---------- Main Function ----------
def main():
    print("📧 Email Sender Bot Started")

    try:
        with open("TASK3\\recipients.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                send_email(row["email"], row["name"])
                time.sleep(1)   # polite delay

    except FileNotFoundError:
        print("❌ recipients.csv file not found.")
        logging.error("Recipient file missing.")


main()
