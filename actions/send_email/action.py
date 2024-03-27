import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

def send_email(details):
    try:
        # Email configuration
        sender_email = details["sender"]
        receiver_email = details["receiver"]

        # create the mail
        message = MIMEMultipart() 
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "I AM A FUCKING BILLIONAIRE" #details["subject"]
        body = "BELIEVE IN YOURSELF KID" #details["body"]
        message.attach(MIMEText(body, "plain"))

        # fetch the smtp credentials
        smtp_host = os.environ.get("SMTP_HOST")
        smtp_user = os.environ.get("SMTP_USER")
        smtp_password = os.environ.get("SMTP_PASS")
        smtp_port = os.environ.get("SMTP_PORT")

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            text = message.as_string()
            err = server.sendmail(sender_email, receiver_email, text)
        
        if not err:
            print("INFO: Email sent successfully!")
        else:
            print("ERROR: Could not send email ", err)

    except Exception as e:
        print(f"ERROR: {e}")