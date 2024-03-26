from celery import shared_task
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@shared_task
def send_email():
    try:
        # Email configuration
        sender_email = "devanshu@lltes.com" #details["sender"]
        receiver_email = "devanshukumar45@gmail.com" #details["receiver"]
        password = "devmailer26"

        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "I AM A FUCKING BILLIONAIRE"

        # Add body to email
        body = "BELIEVE IN YOURSELF KID"
        message.attach(MIMEText(body, "plain"))

        # Connect to SMTP server
        smtp_server = "mail.lltes.com"
        smtp_port = 465  # Use 465 for SSL
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # server.starttls()  # Enable TLS encryption
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("done")

        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")