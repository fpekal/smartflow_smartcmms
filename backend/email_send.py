import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(login: str, token: str, to: str, subject: str, content: str, filename: str):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = login
    msg["To"] = to

    msg.attach(MIMEText(content))
    with open(filename, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(filename)
        )

    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
    msg.attach(part)

    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login(login, token)

    s.send_message(msg)
    s.quit()
