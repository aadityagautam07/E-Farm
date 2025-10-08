from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):

    # Overwriting the list.
    list_display = ('total_orders', 'first_name', 'last_name', 'city', 'state', 'created_date')
    list_display_links = ('total_orders', 'first_name')
    search_fields = ('first_name', 'last_name', 'city', 'zipcode', 'state', )
    list_filter = ('first_name', )

    def total_orders(self, customer):
        total_orders = Order.objects.filter(customer=customer)
        return (total_orders[len(total_orders) - 1].order_made) - 1
    

class OrderAdmin(admin.ModelAdmin):
    # Overwriting the list.
    list_display = ('Overall_status', 'customer', 'order_number', 'total_orders', 'order_status',  'payment_status', 'cart_total_price', 'refunded_amount', 'total_cart_items', 'delivery_status', 'date_ordered')
    list_display_links = ('order_number', )
    search_fields =  ('order_status', 'payment_status', 'date_ordered', )
    list_filter = ('customer', 'delivery_status', )
    list_editable = ('order_status', 'payment_status', )

    actions = ['remove_order', ] 

    def total_cart_items(self, queryset):
        return queryset.get_cart_items

    def cart_total_price(self, queryset):
        return queryset.get_cart_total

    def total_orders(self, queryset):
        return queryset.order_made

    def remove_order(self, request, queryset):
        for order in queryset:
            if order.customer == None:
                order.delete()
    
    remove_order.short_description = 'Remove Unwanted Orders'

    # Order Status 
    def Overall_status(self, obj):
        if obj.payment_status == 'Failed':  
            return format_html('<i class="fa fa-credit-card" style="font-size:20px;color:red">></i>')
        elif obj.order_status == 'Confirm' and obj.delivery_status == 'Received':
            return format_html('<i class="fa fa-check" style="font-size:20px;color:green"></i>')
        elif obj.order_status == 'Cancelled':
            return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')
        elif obj.order_status == 'Confirm' and obj.delivery_status != 'Received':
            return format_html('<i class="fas fa-shipping-fast" style="font-size:20px;color:orange"></i>')
        else:
            return format_html('<i class="fa fa-clock-o" style="font-size:20px;color:orange"></i>')


class OrderItemAdmin(admin.ModelAdmin):
    # Overwriting the list.
    list_display = ('overall_status', 'customer_name', 'order_number', 'product', 'get_total', 'quantity', 'product_status', 'date_added', )
    list_display_links = ('order_number', )
    search_fields = ('', )
    list_filter = ('order_number__customer', 'order_number__order_status', 'order_number__delivery_status', )

    actions = ['remove_orderItems', ]

    def remove_orderItems(self, request, queryset):

        for order in queryset:
            if order.order_number == None:
                order.delete()
    
    remove_orderItems.short_description = 'Remove Unwanted Order Items'

    def customer_name(self, orderItem):
        if orderItem.order_number:
            customer = orderItem.order_number.customer
            return customer
        else:
            return None

    def product_status(self, queryset):
        if queryset.order_number:
            if queryset.delivery == "Return Order Request Got":
                return queryset.delivery
            elif queryset.delivery == "Return Order Request Accepted":
                return queryset.delivery 
            elif queryset.delivery == "Refunded":
                return queryset.delivery
            elif queryset.delivery == "Return Order Request Rejected":
                return queryset.delivery 
            return queryset.order_number.delivery_status
        else:
            return None

    # def return_status(self, queryset):
    #     return queryset.delivery

    

    # OrderItem Status 
    def overall_status(self, obj):
        if obj.order_number:
            if obj.order_number.payment_status == 'Failed':  
                return format_html('<i class="fa fa-credit-card" style="font-size:20px;color:red">></i>')
            elif obj.delivery == "Return Order Request Got" or obj.delivery == "Return Order Request Accepted":
                return format_html('<i class="fas fa-shipping-fast" style="font-size:20px;color:red"></i>')
            elif obj.delivery == "Refunded":
                return format_html('<i class="fa-solid fa-money-bill-transfer"  style="font-size:20px;color:green"></i>')
            elif obj.delivery == "Return Order Request Rejected":
                return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')
            elif obj.order_number.order_status == 'Confirm' and obj.order_number.delivery_status == 'Received':
                return format_html('<i class="fa fa-check" style="font-size:20px;color:green"></i>')
            elif obj.order_number.order_status == 'Cancelled':
                return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')
            elif obj.order_number.order_status == 'Confirm' and obj.order_number.delivery_status != 'Received':
                return format_html('<i class="fas fa-shipping-fast" style="font-size:20px;color:orange"></i>')
            else:
                return format_html('<i class="fa fa-clock-o" style="font-size:20px;color:orange"></i>')
        else:
            return None


class ShippingAddressAdmin(admin.ModelAdmin):
    # Overwriting the list.
    list_display = ('customer_name', 'order', 'shipping_method', 'state', 'city', 'date_added', )
    list_display_links = ('customer_name', 'order', 'shipping_method', 'date_added', )
    search_fields = ('shipping_method', 'state', 'city')
    list_filter = ('shipping_method', 'order__customer')

    actions = ['remove_unwanted_addresses', ]

    def remove_unwanted_addresses(self, request, queryset):
        for address in queryset:
            if address.order == None:
                address.delete()
    
    remove_unwanted_addresses.short_description = 'Remove Unwanted Addresses'

    def customer_name(self, shipping):
        if shipping.order:
            customer = shipping.order.customer
            return customer
        return None

class TransactionAdmin(admin.ModelAdmin):
    # Overwriting the list.
    list_display = ('payment_status', 'payee_and_receivee', 'payer_and_receiver',  'transaction_id', 'made_by', 'amount', 'order_id',  'made_on', )
    list_display_links = ('transaction_id', 'made_by', )
    search_fields = ('transaction_id', 'made_on', )
    list_filter = ('made_by', )

    # Payment Status 
    def payment_status(self, obj):
        if obj.result == 'Failed':  
            return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')
        else:
            return format_html('<i class="fa fa-check" style="font-size:20px;color:green"></i>')

    # Payment Incoming or Outgoing
    def payee_and_receivee(self, obj):
        if obj.payer_and_receiver == 'Debit':
            return format_html('<i class="fa fa-arrow-up" style="font-size:20px;color:orange"></i>')
        elif obj.payer_and_receiver == 'Credit':
            return format_html('<i class="fa fa-arrow-down" style="font-size:20px;color:green"></i>')

class DeliveryStatusAdmin(admin.ModelAdmin):
    # Overwriting the list.
    list_display = ('customer', 'order', 'delivery_status', 'transaction_id', )
    list_display_links = ('transaction_id', 'customer', )
    search_fields = ('order', 'transaction_id', )
    list_filter = ('customer', 'delivery_status', )
    list_editable = ('delivery_status', )


class ReturnOrderRequestAdmin(admin.ModelAdmin):
    # Overwriting the list.
    list_display = ('response', 'customer', 'order', 'transaction_id', 'product', 'item_Price')
    list_display_links = ('transaction_id', 'customer', )
    search_fields = ('order', 'transaction_id', )
    list_filter = ('customer', 'response', )
    list_editable = ('response', )

    # Display OrderItem Price
    def item_Price(self, obj):
        order  = obj.order
        customer = obj.customer
        print(customer)
        print(order)
        order = Order.objects.get(customer=customer, order_number=order)
        orderItem = order.orderitem_set.get(product=obj.product)
        # print("OrderItem =  ", orderItem)
        return orderItem.get_total

    # Showing Delivery status
    def delivery_status(self, obj):
        order  = obj.order
        return order.delivery_status


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(DeliveryStatus, DeliveryStatusAdmin)
admin.site.register(ReturnOrderRequest, ReturnOrderRequestAdmin)


