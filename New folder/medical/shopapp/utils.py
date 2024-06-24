import imaplib
import email
from email.header import decode_header
from email import message_from_string
from .models import Lead

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

                # Fetch the email body
                body = get_email_body(msg)

                # Extract the desired information from the body
                # Assuming the body format is "Name: John Doe, Phone: 1234567890, Address: 123 Main St"
                name, phone, tablet, price, quantity = parse_body(body)

                # Save the information in the Contact model
                Lead.objects.create(customer_name=name, phone_number=phone, tablet_name=tablet,price=price,quantity=quantity)

    # Close the connection and logout
    imap.close()
    imap.logout()

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload is not None:
                    body += payload.decode()
    else:
        payload = msg.get_payload(decode=True)
        if payload is not None:
            body = payload.decode()
    return body

def parse_body(body):
    parts = body.split(", ")
    name = parts[0].split(": ")[1]
    phone = parts[1].split(": ")[1]
    tablet = parts[2].split(": ")[1]
    price = parts[3].split(": ")[1]
    quantity = parts[4].split(": ")[1]

    return name, phone, tablet,price,quantity
