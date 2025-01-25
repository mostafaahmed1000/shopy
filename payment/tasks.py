import os 
from celery import shared_task
import pdfkit
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

wkhtml_to_pdf = os.path.join(
    settings.BASE_DIR, "wkhtmltopdf.exe")
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    print(f'Processing order with ID {order_id}')
    try:
        order = Order.objects.get(id=order_id)
        print(f'Order with ID {order_id} found')
    except Order.DoesNotExist:
        print(f'Order with ID {order_id} not found')
        return

    options = {
        'page-size': 'A4',
        'page-height': "13in",
        'page-width': "10in",
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'encoding': "UTF-8",
        'no-outline': None,
        "enable-local-file-access": ""
    }

    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'

    try:
        email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
        print('Email created')
    except Exception as e:
        print(f'Error creating email: {e}')
        return

    try:
        html = render_to_string('orders/order/pdf.html', {'order': order})
        config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)
        pdf = pdfkit.from_string(html, False, configuration=config, options=options)
        email.attach(f'order_{order.id}.pdf', pdf, 'application/pdf')
        email.send()
        print('Email sent')
    except Exception as e:
        print(f'Error sending email: {e}')
        return
