import smtplib, os
from email.message import EmailMessage

def send(to,sub,body):
    msg=EmailMessage()
    msg["From"]=os.getenv("FROM_EMAIL")
    msg["To"]=to
    msg["Subject"]=sub
    msg.set_content(body)
    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")) ) as s:
        s.starttls()
        s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        s.send_message(msg)

# Example (commented until creds set)
# send("user@example.com","Welcome","Your AI site is live")
