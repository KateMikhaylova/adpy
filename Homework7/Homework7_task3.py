import configparser
import email
import smtplib
import imaplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email.message import Message
from typing import List


class MyMail:
    """
    Class to work with e-mail

    Attributes:
        login: email login
        password: email password
        smtp: domain name of mail using SMTP protocol (to send messages)
        imap: domain name of mail using IMAP protocol (to receive messages)

    Methods:
        send_message: sends message to indicated recipients
        receive_last_message: returns last message with indicated header
    """

    def __init__(self, login: str, password: str, smtp: str, imap: str):
        """
        Sets up login, password, smtp, imap attributes
        :param login: email login
        :param password: email password
        :param smtp: domain name of mail using SMTP protocol
        :param imap: domain name of mail using IMAP protocol
        """
        self.login = login
        self.password = password
        self.smtp = smtp
        self.imap = imap

    def send_message(self, recipients: List[str], subject: str, message: str) -> None:
        """
        Sends message to indicted recipients
        :param recipients: list of recipients emails (str)
        :param subject: subject of message
        :param message: message text
        :return:
        """
        msg = MIMEMultipart()

        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.smtp, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()

        ms.login(self.login, self.password)
        ms.sendmail(self.login, msg['To'], msg.as_string())

        ms.quit()

    def receive_last_message(self, header: str = None) -> Message:
        """
        Returns last message with indicated header
        :param header: header to look for, None as default in such case 'ALL' messages are searched for
        :return: email.message.Message object
        """
        mail = imaplib.IMAP4_SSL(self.imap)

        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")

        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'

        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        mail.logout()

        return email_message


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('email.ini')
    my_login = config['email']['login']
    my_password = config['email']['password']
    gmail_smtp = config['email']['GMAIL_SMTP']
    gmail_imap = config['email']['GMAIL_IMAP']

    my_mail = MyMail(my_login, my_password, gmail_smtp, gmail_imap)

    my_mail.send_message(['vasya@email.com', 'petya@email.com'], 'Subject', 'Message')

    last_email = my_mail.receive_last_message()
