import imaplib
import email
from email.header import decode_header
from .models import Contact

def fetch_unseen_emails():
    # Connect to the email server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login("activecustomer.email@gmail.com", "mdti hyxy cpzp iozr")

    # Select the mailbox you want to check
    imap.select("inbox")

    # Search for unseen emails
    status, messages = imap.search(None, '(UNSEEN)')

    # Convert messages to a list of email IDs
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = imap.fetch(email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the email content
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                # Extract the desired information from the subject
                # Assume the subject format is "Name: John Doe, Phone: 1234567890, Address: 123 Main St"
                name, phone, address = parse_subject(subject)

                # Save the information in the Contact model
                Contact.objects.create(name=name, phone=phone, address=address)

    # Close the connection and logout
    imap.close()
    imap.logout()

def parse_subject(subject):
    # Assuming the subject format is "Name: John Doe, Phone: 1234567890, Address: 123 Main St"
    parts = subject.split(", ")
    name = parts[0].split(": ")[1]
    phone = parts[1].split(": ")[1]
    address = parts[2].split(": ")[1]
    return name, phone, address
