import smtplib
from email.message import EmailMessage

# Fixed HR email
HR_EMAIL = "digitalpathfinder9@gmail.com"  

def send_email(subject, body, attachments=[]):
    EMAIL_SENDER = "defencejournal2@gmail.com"
    EMAIL_PASSWORD = "rpga errd gbvo ttgm"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = HR_EMAIL
    msg.set_content(body)

    for file_path in attachments:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = f.name.split("/")[-1]
        msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
