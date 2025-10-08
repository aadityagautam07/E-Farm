from django.db import models
from django.contrib.auth.models import User
from store.models import all_Product
from efarm import settings
from django.utils.html import format_html
from phonenumber_field.modelfields import PhoneNumberField

from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, default="none")
    last_name = models.CharField(max_length=255, null=True, blank=True, default="none")
    email = models.EmailField(max_length=255, null=True, blank=True, default="none")
    phone = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    landmark = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Order(models.Model):
    order_status = (
        ('Confirm', 'Confirm'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    )

    payment_status = (
        ('Done', 'Done'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Failed', 'Failed'),
    )

    status = (
        ('In Progress', 'In Progress'),
        ('Shipped', 'Shipped'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Received', 'Received'),
    )


    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    order_number = models.CharField(max_length=100, null=True, blank=True, unique=True, default=uuid.uuid4)
    order_status = models.CharField(choices=order_status, max_length=255, default='Pending')
    payment_status = models.CharField(choices=payment_status, max_length=255, default="Pending")
    order_made = models.IntegerField(null=True, blank=True, default=1)
    shipping_method = models.CharField(max_length=200, null=True, blank=True, default="Standard Delivery")
    delivery_status = models.CharField(max_length=255, choices=status, default='In Progress')
    refunded_amount = models.CharField(max_length=200, null=True, blank=True, default='0')

    def __str__(self):
        return str(self.order_number)
        
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])

        if self.shipping_method == 'Express Delivery':
            return total + 150
        elif self.shipping_method == 'Next Business Day':
            return total + 500
        else:
            return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_original_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.original_price * item.quantity for item in orderitems])
        return total
    
    @property
    def get_cart_discount_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.discount_amount * item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(all_Product, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    delivery = models.CharField(max_length=255, null=True, blank=True)

    @property
    def get_total(self):
        total = 0   
        if self.product.discount != '0%':
            total += self.product.after_discount_price * self.quantity
        else:
            total += self.product.original_price * self.quantity
        return total

    def __str__(self):
        return str(self.product.product_name)    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True,  blank=True)
    landmark = models.CharField(max_length=200, null=True,  blank=True)
    address1 = models.CharField(max_length=200, null=True,  blank=True)
    city = models.CharField(max_length=200, null=True,  blank=True)
    state = models.CharField(max_length=200, null=True,  blank=True)
    zipcode = models.CharField(max_length=200, null=True,  blank=True)
    shipping_method = models.CharField(max_length=200, null=True, blank=True) 
    shipping_same_as_billing = models.BooleanField( null=True, blank=True)
    save_info_for_next_time = models.BooleanField( null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.shipping_method)

class Transaction(models.Model):
    made_by = models.ForeignKey(Customer, related_name='transactions',
                                on_delete=models.SET_NULL, null=True, blank=True)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(unique=True, max_length=255, null=True)
    checksum = models.CharField(max_length=255, null=True, blank=True)
    result = models.CharField(max_length=255, null=True, blank=True, default='Failed')
    payer_and_receiver = models.CharField(max_length=255, null=True, blank=True, default='Credit')

    def save(self, *args, **kwargs):
        if self.transaction_id is None and self.made_on and self.id:
            self.transaction_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.transaction_id)

class DeliveryStatus(models.Model):
    status = (
        ('In Progress', 'In Progress'),
        ('Shipped', 'Shipped'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Received', 'Received'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_status = models.CharField(max_length=255, choices=status, default='In Progress')
    transaction_id = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.delivery_status

    def save(self, *args, **kwargs):
        status = self.delivery_status
        order_id = self.order

        # Update the order model 
        order = Order.objects.get(order_number=order_id)
        order.delivery_status = status
        order.save()

        super().save(*args, **kwargs)

class ReturnOrderRequest(models.Model):
    status = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
        ('Payment Done', 'Payment Done'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    response = models.CharField(max_length=255, choices=status, default='Pending')
    product = models.ForeignKey(all_Product, on_delete=models.SET_NULL, blank=True, null=True)
    delivery_status = models.ForeignKey(DeliveryStatus, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.response)   

    def save(self, *args, **kwargs):
        order_id = self.order

        if self.response == "Pending":
            order = Order.objects.get(order_number=order_id)
            orderItems = order.orderitem_set.get(product=self.product)
            print(f"orderItems = {orderItems}")
            orderItems.delivery = 'Return Order Request Got'
            orderItems.save()
        
        if self.response == "Accepted":
            order = Order.objects.get(order_number=order_id)
            orderItems = order.orderitem_set.get(product=self.product)
            print(f"orderItems = {orderItems}")
            orderItems.delivery = 'Return Order Request Accepted'
            orderItems.save()

            # Creating New Transaction If Payment Accepted
            transaction = Transaction.objects.create(made_by=order.customer, order_id=order,
             amount=orderItems.get_total, payer_and_receiver="Debit")
            transaction.save()

        if self.response == "Payment Done":
            order = Order.objects.get(order_number=order_id)
            orderItems = order.orderitem_set.get(product=self.product)
            print(f"orderItems = {orderItems}")
            orderItems.delivery = 'Refunded'
            orderItems.save()

            # Creating New Transaction If Payment Accepted
            transaction = Transaction.objects.get(made_by=order.customer, order_id=order,
             amount=orderItems.get_total)
            transaction.result = "Success"
            transaction.save()

            # Updating Order 
            order.refunded_amount = orderItems.get_total
            # order.get_cart_total = order.get_cart_total - order.refunded_amount
            order.save()


        if self.response == "Rejected":
            order = Order.objects.get(order_number=order_id)
            orderItems = order.orderitem_set.get(product=self.product)
            orderItems.delivery = 'Return Order Request Rejected'
            orderItems.save()

        super().save(*args, **kwargs)
