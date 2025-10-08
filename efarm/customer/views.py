from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from .paytm_process import *

from accounts.email import *

# Create your views here.

def cart(request):
    # If user is logged in then 
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, order_status='Pending', complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            print("Views.py Cart Logged in User")

    # if not 
        else:    
    # Will continue This once we done with logged in user add to cart module
            try:
                cart = json.loads(request.COOKIES['cart'])
            except:
                cart = {}
            print(cart)
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']

            for i in cart:
                cartItems += cart[i]['quantity']

        context = {
            'items': items,
            'order': order,
            'cartItems': cartItems,
        }

        return render(request, "store/cart.html", context)
    
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('ProductId: ', productId)

    customer = request.user.customer
    product = all_Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, order_status='Pending', complete=False)

    item_entries = order.orderitem_set.filter(order_number=order)
    print(f"Items Filter = {item_entries}")

    total_quantity = 0
    for i in item_entries:
        total_quantity += i.quantity
        
    print(f"Total Quantity = {total_quantity}")


    if total_quantity <= 9:
        orderItem, created = OrderItem.objects.get_or_create(order_number=order, product=product)

        if action == 'add':
            if orderItem.quantity <= 9:
                orderItem.quantity = (orderItem.quantity + 1)
                messages.success(request, "Item Added To Cart.")
            else:
                messages.warning(request, "Cart Limit Reached")
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
            messages.success(request, "Item Removed From Cart")

        orderItem.save()

        if orderItem.quantity <= 0 or action == 'delete':
            orderItem.delete()
            messages.success(request, "Item Removed From Cart")
    
    else:
        orderItem = OrderItem.objects.get(order_number=order, product=product)
        if action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
            print(f"Order ITem Quantity = {orderItem.quantity}")
            messages.success(request, "Item Removed From Cart")
            orderItem.save()
        else:
            pass

        if orderItem.quantity <= 0 or action == 'delete':
            orderItem.delete()
            messages.success(request, "Item Removed From Cart")
            
        else:
            messages.warning(request, "Cart Limit Reached")


    return JsonResponse('Item was Added', safe=False)

@login_required
def checkout(request):
    try:
        if request.method == 'POST':
            print("Inside the Checkout view")


            # Billing Form Data 
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            phone = request.POST.get('phnumber')
            email = request.POST.get('email')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            landmark = request.POST.get('landmark')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zipcode')



            # Shipping Method Data
            method = request.POST.get('shipping-option')
            print("Got all data Going for billingAddress module ....")


            # Adding data to the server
            if request.user.is_authenticated:
                customer = request.user.customer
                order = Order.objects.get(customer=customer, order_status='Pending', complete=False)
                print(phone)
                

                # Updating the Total After Shipping Method Choosen
                if method:
                    order.shipping_method = method
                    order.save()


                context = {
                    'customer': customer
                }
            
                billingAddress, created = ShippingAddress.objects.update_or_create(
                    order=order, 
                    defaults={'phone':phone, 'address1':address1, 'address2':address2, 
                    'city':city, 'state':state, 'email':email, 'zipcode':zip_code, 'landmark':landmark, 
                    'shipping_method':method}
                    )
                
                user = request.user
                queryset = Customer.objects.get(user=user)

                
                if queryset.phone == None and queryset.address1 == None and queryset.address2 == None and queryset.city == None and queryset.state == None and queryset.zipcode == None:
                    print("Customer Address Feilds Get Updated")
                    customer, created = Customer.objects.update_or_create(
                        user=user, 
                        defaults={
                            'phone':phone, 'address1':address1, 'address2':address2, 
                            'city':city, 'state':state, 'zipcode':zip_code
                        }
                    )

                print(billingAddress)
                
                print("Data Got and Saved")
                


                # If Cart is Empty then no checkout payment module
                customer = request.user.customer
                order = Order.objects.get(customer=customer, order_status='Pending', complete=False)
                items = order.orderitem_set.all()
                print(items)
                if not items:
                    messages.info(request, "Can't Checkout With Empty Cart.")
                    return redirect('checkout')
                else:
                    # If Cart is not Empty
                    print('Before Paytm module')
                    # Payment Module
                    context = paytm(request)
                    print('After Paytm module')
                    print("Sending the user to Paytm API.")

                    return render(request, 'payment/paytm.html', context)

        return render(request, 'store/checkout.html')
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()
    
def wishlist(request):
    # Not Logged In
    try:
        wishlist_cp = json.loads(request.COOKIES['wishlist'])
    except:
        wishlist_cp = {}
    print(wishlist_cp)
    items_wishlist_cp = []


    for i in wishlist_cp:

        product_wishlist_cp = all_Product.objects.get(id=i)
        print(product_wishlist_cp.original_price)

        items_wishlist_cp2 = {
            'product': {
                'id': product_wishlist_cp.id,
                'name': product_wishlist_cp.product_name,
                'price': product_wishlist_cp.original_price,
                'imageURL': product_wishlist_cp.photo3.url,
                'discount': product_wishlist_cp.discount,
            }
        }
        items_wishlist_cp.append(items_wishlist_cp2)
    context = {
        'items_wishlist_cp': items_wishlist_cp,
    }
    return render(request, "store/wishlist.html", context)

@ensure_csrf_cookie
@csrf_exempt
def callback(request):
    try:
        if request.method == 'POST':
            print("inside callback")
            paytm_checksum = ''
            print(request.body)
            print(request.POST)
            received_data = dict(request.POST)
            print(received_data)


            # Failure response
            failure_response = received_data['RESPMSG']


            # If Paytm Failure 
            for key, value in received_data.items():
                if key == 'STATUS' and value == ['TXN_FAILURE']:
                    print(f"Payment Failed = {key}: {value}")
                    messages.warning(request, str(failure_response))
                    # return redirect('checkout')
                    payment_status = 'failed'
                    return redirect('updation', payment_status)

            paytm_params = {}
            paytm_checksum = received_data['CHECKSUMHASH'][0]
            for key, value in received_data.items():
                if key == 'CHECKSUMHASH':
                    paytm_checksum = value[0]
                else:
                    paytm_params[key] = str(value[0])

            # Verify checksum
            is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
            if is_valid_checksum:
                print("Checksum Matched")
                received_data['message'] = "Checksum Matched"
            else:
                print("Checksum Mismatched")
                received_data['message'] = "Checksum Mismatched"
            
            

            print("Payment Success")



            messages.success(request, "Thanks for Purchasing.")
            payment_status = 'success'
            return redirect('updation', payment_status)
        
        messages.error(request, "Something Went Wrong Please Try Again.")

    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()
        
def updation(request, payment_status):
    try:
        if payment_status == 'success':
            customer = request.user.customer

            order = Order.objects.get(customer=customer, order_status='Pending', complete=False)
            transaction = Transaction.objects.get(made_by=customer, order_id=order)
            shipping_address, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)

            # Updating product stock
            # orderItem = order.orderitem_set.all()
            # product = all_Product.objects.filter(id=orderItem.product.id)
            # product.stock = orderItem.
            
            
            # Updating the current order 
            order.payment_status = 'Done'
            order.order_status = 'Confirm'
            order.complete = True
            order.date_ordered = datetime.datetime.now()
            order.save()

            # Updating the Transaction
            transaction.result = 'Success'
            transaction.made_on = datetime.datetime.now()

            # Send Mail
            invoice_mail(request, request.user, order, transaction, shipping_address)

            # Updating Delivery Status Model
            delivery, created = DeliveryStatus.objects.get_or_create(customer=customer, order=order, transaction_id=transaction,
            shipping_address=shipping_address)
            
            transaction.save()        

            # Creating New Order Entry 
            order_made = order.order_made
            order = Order.objects.create(customer=customer, order_status='Pending', order_made=order_made)
            order.order_made += 1
            order.save()
            print("New Order Created.")
            return render(request, 'payment/paymentstatus.html')

        else:
            # If Payment Failed
            customer = request.user.customer
            order = Order.objects.get(customer=customer, order_status='Pending', complete=False)
            transaction = Transaction.objects.get(made_by=customer, order_id=order, result="Failed")

            print(transaction)
            # Updating the Transaction
            transaction.delete()       

            # Updating the current order 
            order.payment_status = 'Failed'
            order.order_status = 'Pending'
            order.complete = False
            order.date_ordered = datetime.datetime.now()
            order.save()

            return redirect('checkout')

        return render(request, 'payment/paymentstatus.html')
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()