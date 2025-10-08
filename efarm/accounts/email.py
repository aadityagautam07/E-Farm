# For Sending Email
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage
from django.conf import settings

# Importing below because we have modified the User model
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import *

def verification_email(request, otp):

    pk = request.session.get('pk')
    print(f"{'-'*20} {pk} Inside email File {'-'*20}")

    if pk:
        main_user = User.objects.filter(pk=pk).get()
        subject = "OTP Verification ..."
        print("hello")
        email_from = settings.EMAIL_HOST_USER
        print("------")
        recipient_list = [main_user.email]
        print("Yas")
        # import html message.html file
        print(f"{main_user.username} = Mail ")

        html_template = 'emails/otp.html'
        print('html_template = ',html_template)
        html_message = render_to_string(html_template, {'otp': otp})
        print('Below Html_message = ', html_message)
        message = EmailMessage(subject, html_message, email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()


def invoice_mail(request, user, order, transaction_id, shipping_address):

    print(f"{'-'*20} Inside Invoice email File {'-'*20}")

    # Fetching Data
    items = order.orderitem_set.all()

    context = {
        'order': order,
        'items': items,
        'shipping_address': shipping_address,
        'transaction_id': transaction_id,
    }

    subject = "Thanks For Purchase"
    print("hello")
    email_from = settings.EMAIL_HOST_USER
    print("------")
    recipient_list = [user.email]
    print("Yas")

    # import html message.html file
    # print(f"{main_user.username} = Mail ")
    html_template = 'emails/invoice.html'
    print('html_template = ',html_template)
    html_message = render_to_string(html_template, context)
    print('Below Html_message = ', html_message)
    message = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send()

def discount_mail(request, user, order, transaction_id, shipping_address):

    print(f"{'-'*20} Inside Invoice email File {'-'*20}")

    # Fetching Data
    items = order.orderitem_set.all()

    context = {
        'order': order,
        'items': items,
        'shipping_address': shipping_address,
        'transaction_id': transaction_id,
    }

    subject = "Thanks For Purchase"
    print("hello")
    email_from = settings.EMAIL_HOST_USER
    print("------")
    recipient_list = [user.email]
    print("Yas")

    # import html message.html file
    # print(f"{main_user.username} = Mail ")
    html_template = 'emails/invoice.html'
    print('html_template = ',html_template)
    html_message = render_to_string(html_template, context)
    print('Below Html_message = ', html_message)
    message = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send()