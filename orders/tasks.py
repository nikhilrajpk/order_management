import imaplib
import email
import google.generativeai as genai
from celery import shared_task
from django.conf import settings
from orders.models import Order
import logging
import json

logger = logging.getLogger(__name__)

@shared_task
def monitor_warehouse_emails():
    logger.info("Starting monitor_warehouse_emails task")
    try:
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Connect to email inbox
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        mail.select('INBOX')

        # Search for unread emails from warehouse
        _, data = mail.search(None, '(FROM "warehouseemail2025@gmail.com" UNSEEN)')
        logger.info(f"Found {len(data[0].split())} unread emails from warehouse")

        for num in data[0].split():
            _, msg_data = mail.fetch(num, '(RFC822)')
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)

            # Extract email content
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        content = part.get_payload(decode=True).decode()
                        break
            else:
                content = msg.get_payload(decode=True).decode()

            logger.info(f"Processing email content: {content}")

            # Use Gemini to extract order ID
            prompt = f"""
            Extract the order ID from the following email content as a JSON object:
            {content}
            Return only the JSON object, e.g., {{"order_id": "123"}}.
            If no order ID is found, return {{"order_id": null}}.
            """
            response = model.generate_content(prompt)
            try:
                result = json.loads(response.text.strip('```json\n').strip('\n```'))
                order_id = result.get('order_id')
                if order_id:
                    logger.info(f"Found order ID: {order_id}")
                    try:
                        order = Order.objects.get(id=order_id)
                        order.status = 'Confirmed'
                        order.save()
                        logger.info(f"Updated order {order_id} to Confirmed")
                    except Order.DoesNotExist:
                        logger.warning(f"Order {order_id} not found")
                else:
                    logger.info("No order ID found in email content")
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON response from Gemini: {response.text}")
                continue

            mail.store(num, '+FLAGS', '\\Seen')
        mail.logout()
    except Exception as e:
        logger.error(f"Error in monitor_warehouse_emails: {str(e)}")
        raise