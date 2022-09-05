import logging
from abc import ABC, abstractclassmethod
import ssl,smtplib

logger = logging.getLogger(__name__)

class Connection(ABC):
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    @abstractclassmethod
    def setConnection(self):
        pass

class SMTPConnection(Connection):
    def __init__(self, smtpserver, port, sender, password, receiver):
        self.smtpserver = smtpserver
        self.port = port
        self.sender = sender
        self.password = password
        self.receiver = receiver

    def send_email(self, server):
        try:
            server.sendmail(self.sender, self.receiver, "Day tap the duc")
            server.quit()
            print("Email sent!")
        except Exception as e:
            print("Error: ", e)

    def setConnection(self):
        context = ssl.create_default_context()
        print("Connecting to SMTP server ", self.smtpserver)
        try:
            server = smtplib.SMTP_SSL(self.smtpserver, self.port, context=context)
            server.ehlo()
            server.login(self.sender, self.password)
            self.send_email(server)
        except Exception as e:
            print("Error while connecting to SMTP", e)
        finally:
            server.close()
            print("SMTP connection is closed")

def my_scheduled_job():
    print("day tap the duc")
    logger.info("cron job is called")

def sent_mail():
    print("\nSMTP Connection")
    testsmtp = SMTPConnection(
        "smtp.gmail.com",
        465,
        "quangdinh.clone@gmail.com",
        "xmfjhirhpyxzpdra",
        "quangdinhvh2@gmail.com",
    )
    testsmtp.setConnection()

    logger.info("sent mail")