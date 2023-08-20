from __future__ import annotations

import email.mime.application
import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config as environment


class EmailClient:

    port: int
    smtp_server: str
    sender_account_email: str
    sender_account_password: str
    recipients: list
    message_subject: str

    def __init__(self):
        receipt_accounts_email = []

        self.port = int(environment('EMAIL_SERVER_PORT'))
        self.smtp_server = environment('EMAIL_SMTP_SERVER')
        self.sender_account_email = environment('SENDER_ACCOUNT_EMAIL')
        self.sender_account_password = environment('SENDER_ACCOUNT_PASSWORD')

        email_receipts = environment('RECEIPT_ACCOUNT_EMAIL')

        for email_receipt in email_receipts.split(','):
            receipt_accounts_email.append(email_receipt)

        self.message_subject = environment('EMAIL_SUBJECT_TXT')

        self.message = MIMEMultipart('alternative')
        self.message['Subject'] = self.message_subject
        self.message['From'] = self.sender_account_email
        self.message['To'] = ', '.join(receipt_accounts_email)

        self.context = ssl.create_default_context()

        self.recipients = receipt_accounts_email

    @staticmethod
    def attach_file_to_email(file_to_attach):
        with open(file_to_attach, 'rb') as attach_file:  # open the file

            file_name = os.path.basename(attach_file.name)

            attach_f = email.mime.application.MIMEApplication(attach_file.read(), subtype='pdf')

            attach_file.flush()

            attach_file.close()

            attach_f.add_header('Content-Disposition', 'attachment', filename=file_name)

            return attach_f

    def send_email(self, file_path_attached, content_message):
        email_send_success = ''

        # Turn the text_message into plain/html MIMEText objects
        msg_part = MIMEText(content_message, 'plain')
        # part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        self.message.attach(msg_part)

        attach_file = self.attach_file_to_email(file_path_attached)

        self.message.attach(attach_file)

        # Create secure connection with server and send email
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:

            server.ehlo()

            server.login(self.sender_account_email, self.sender_account_password)

            server.sendmail(
                self.sender_account_email, self.recipients, self.message.as_string(),
            )

        email_send_success = f'Server Email User: {server.user}, Email Receipt: {self.message.get("To")}, ' \
                             f'Email Subject: {self.message_subject}, File: {attach_file.get_filename()}'

        server.close()

        return email_send_success
