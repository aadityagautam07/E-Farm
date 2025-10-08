from django.shortcuts import render
from django.http import JsonResponse
import json
from store.models import all_Product
from .models import *

# For the Guest User only

def extras(request):
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            print(f"Context Processor : {customer}")
            order, created = Order.objects.get_or_create(customer=customer, order_status='Pending', complete=False)
            print(f"Order : {order}")
            items = order.orderitem_set.all()
            print("CART = Logged in User : Context Processor")

            context = {
                'items': items,

                'order': order,
            }

        else:
            # Not Logged In
            try:
                cart_cp = json.loads(request.COOKIES['cart'])
            except:
                cart_cp = {}
            print(cart_cp)
            items_cp = []
            order_cp = {'get_cart_total': 0, 'get_cart_items': 0, 'get_cart_original_total': 0, 'discount_cp': 0}
            cartItems_cp = order_cp['get_cart_items']
            

            for i in cart_cp:
                cartItems_cp += cart_cp[i]['quantity']
                product_cp = all_Product.objects.get(id=i)

                print(product_cp.original_price)

                # Total cart price With Discount
                if product_cp.discount != '0%':
                    total_cp = (product_cp.after_discount_price * cart_cp[i]['quantity'])
                else:
                    total_cp = (product_cp.original_price * cart_cp[i]['quantity'])

                # Total Without Discount
                total_original_cp = (product_cp.original_price * cart_cp[i]['quantity'])

                # Total Discount
                discount_cp = (product_cp.discount_amount * cart_cp[i]['quantity'])

                order_cp['get_cart_total'] += total_cp
                order_cp['get_cart_items'] += cart_cp[i]['quantity']
                order_cp['get_cart_original_total'] += total_original_cp
                order_cp['discount_cp'] += discount_cp

                item_cp = {
                    'product': {
                        'id': product_cp.id,
                        'name': product_cp.product_name,
                        'price': product_cp.original_price,
                        'imageURL': product_cp.front_image.url,
                        'discount': product_cp.discount,
                    },
                    'quantity': cart_cp[i]["quantity"],
                    'get_total_with_discount': total_cp,
                }

                items_cp.append(item_cp)

            context = {
                'items_cp': items_cp,
                'order_cp': order_cp,
                'cartItems_cp': cartItems_cp,
            }


        return context
    except:
        context = {}
        return context