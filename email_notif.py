from dbfunctions import get_event_details, get_full_name
import ssl, smtplib
from random import choice
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 587
smtp_server = "smtp.office365.com"
sender_email = "buddyconnect1@outlook.com"
password = "HelloBuddy"

msg = MIMEMultipart()
msg["From"] = sender_email

def send_email(event_id, requesting_email):
    event_details = get_event_details(event_id)
    event_name = event_details[1]
    full_name = get_full_name(requesting_email)

    msg["To"] = event_details[9]
    msg["Subject"]="Potential Buddy Found!"

    email_body = f"""Hi,

    We found you a potential buddy for {event_name}.

    Name: {full_name}
    Email: {requesting_email}

    Reach out if you're interested!

    Regards,
    BuddyConnect
    """

    msg.attach(MIMEText(email_body))
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  
        server.starttls(context=context)
        server.ehlo()  
        server.login(sender_email, password)
        server.sendmail(sender_email, event_details[1], msg.as_string())

if __name__ == "__main__":
    send_email(1, "user2@email.com")

