from .models import *
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.contrib import messages
import datetime

def paytm(request):
    customer = request.user.customer
    order = Order.objects.get(customer=customer, order_status='Pending', complete=False)
    print(order)
    print("hello")
    # user = request.user
    transaction = Transaction.objects.create(made_by=customer, order_id=order, amount=order.get_cart_total, result='Failed')
    transaction.save()
    print("First Time Save", transaction.transaction_id)
    merchant_key = settings.PAYTM_SECRET_KEY
    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.transaction_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://localhost:8000/customer/callback/'),
        # ('CALLBACK_URL', 'https://fe1f-203-109-79-189.ngrok.io/customer/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )
    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)
    print(checksum)

    transaction.checksum = checksum
    transaction.save()
    print("Second time Time Save", transaction.transaction_id)
    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)

    # Removing Duplicate Entries of Transaction table
    Transaction.objects.filter(transaction_id=None).delete()

    data = {
        'order': order,
    }

    context = paytm_params
    print("context = ", context)

    return context