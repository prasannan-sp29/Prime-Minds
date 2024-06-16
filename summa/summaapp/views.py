# views.py
import imaplib
import email
from email.policy import default
from django.shortcuts import render
from .models import Lead

def extract_email_details(email_body):
    # Implement your parsing logic here to extract name, phone, email, tablet, quantity, and price
    # This is a basic example and might need adjustments based on your email format
    import re
    
    name = re.search(r"Name:\s*(.*)", email_body).group(1)
    phone = re.search(r"Phone:\s*(.*)", email_body).group(1)
    email_id = re.search(r"Email:\s*(.*)", email_body).group(1)
    tablet = re.search(r"Tablet:\s*(.*)", email_body).group(1)
    quantity = re.search(r"Quantity:\s*(.*)", email_body).group(1)
    price = re.search(r"Price:\s*(.*)", email_body).group(1)
    
    return {
        'name': name.strip(),
        'phone': int(phone.strip()),
        'email': email_id.strip(),
        'tablet': tablet.strip(),
        'quantity': int(quantity.strip()),
        'price': float(price.strip())
    }

def fetch_and_store_email_data(request):
    # Connect to the email server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login("activecustomer.email@gmail.com", "mdti hyxy cpzp iozr")
    mail.select('inbox')

    # Search for unseen emails
    status, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    for email_id in email_ids:
        # Fetch the email
        status, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]

        # Parse the email content
        msg = email.message_from_bytes(raw_email, policy=default)
        email_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_body = part.get_payload(decode=True).decode()
                    break
        else:
            email_body = msg.get_payload(decode=True).decode()

        # Extract details from the email body
        details = extract_email_details(email_body)

        # Store the details in the Lead model
        Lead.objects.create(
            name=details['name'],
            phone=details['phone'],
            email=details['email'],
            tablet=details['tablet'],
            quantity=details['quantity'],
            price=details['price']
        )

    return render(request, 'fetch_email_data.html', {'message': 'Emails processed successfully.'})
