import os,smtplib
from email.message import EmailMessage
msg=EmailMessage()
msg["From"]=os.environ["FROM_EMAIL"]
msg["To"]=os.environ["ADMIN_EMAIL"]
msg["Subject"]="AI Revenue Engine Deployed"
msg.set_content("Site updated with new niches & pages.")
with smtplib.SMTP(os.environ["SMTP_HOST"],int(os.environ["SMTP_PORT"])) as s:
    s.starttls()
    s.login(os.environ["SMTP_USER"],os.environ["SMTP_PASS"])
    s.send_message(msg)
