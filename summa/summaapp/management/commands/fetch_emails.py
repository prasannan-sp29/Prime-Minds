import imaplib
import email
import re
from django.core.management.base import BaseCommand
from summaapp.models import ContactInfo

class Command(BaseCommand):
    help = 'Fetch emails and extract contact information'

    def handle(self, *args, **kwargs):
        self.fetch_emails()

    def fetch_emails(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('activecustomer.email@gmail.com', 'mdti hyxy cpzp iozr')
        mail.select('inbox')

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        for email_id in email_ids:
            email_message = self.get_email_content(mail, email_id)
            email_body = self.extract_body(email_message)
            info = self.extract_information(email_body)
            if info:
                ContactInfo.objects.create(name=info['name'], phone=info['phone'], address=info['address'])
                self.stdout.write(self.style.SUCCESS(f'Successfully saved info: {info}'))

    def get_email_content(self, mail, email_id):
        status, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        return email.message_from_bytes(raw_email)

    def extract_body(self, email_message):
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))

                if 'attachment' not in content_disposition:
                    if content_type == 'text/plain':
                        return part.get_payload(decode=True).decode()
        else:
            return email_message.get_payload(decode=True).decode()

    def extract_information(self, email_body):
        name_pattern = r"Name:\s*(.*)"
        phone_pattern = r"Phone:\s*(.*)"
        address_pattern = r"Address:\s*(.*)"

        name = re.search(name_pattern, email_body)
        phone = re.search(phone_pattern, email_body)
        address = re.search(address_pattern, email_body)

        if name and phone and address:
            return {
                'name': name.group(1).strip(),
                'phone': phone.group(1).strip(),
                'address': address.group(1).strip()
            }
        return None