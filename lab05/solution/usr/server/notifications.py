import ssl
import smtplib
from email.message import EmailMessage

class EmailNotifier:
    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 465,
        username: str = "linsw.mini",
        password: str = "<your-app-password-here>",
        sender: str = "linsw.mini@gmail.com"
    ):
        self.smtp_server = smtp_server
        self.smtp_port   = smtp_port
        self.username    = username
        self.password    = password
        self.sender      = sender

        if not self.username or not self.password:
            raise ValueError("SMTP username and password must be provided")

        self.context = ssl.create_default_context()

    def send(
        self,
        to_email: str,
        subject: str,
        body: str,
        html: str = None
    ):
        msg = EmailMessage()
        msg["From"]    = self.sender
        msg["To"]      = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        if html:
            msg.add_alternative(html, subtype="html")

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=self.context) as smtp:
            smtp.login(self.username, self.password)
            smtp.send_message(msg)