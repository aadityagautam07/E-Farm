from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *

# Email
from .email import *

# Importing below because we have modified the User model
from django.contrib.auth import get_user_model
User = get_user_model()

from customer.models import *
from store.models import *

from django.http import Http404, HttpResponse, HttpResponseForbidden

from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


from django.contrib.auth import logout

import uuid                                     # To Generate Token
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

from django.http import JsonResponse
import json


# Create your views here.

# REGISTER     
def register(request):

    if request.method == "POST":
        print("Hlo")
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        conf_pass = request.POST['pass2']
        print(f"{'-'*20} Got {username} info & Going for Validation {'-'*20}")
        User = get_user_model()
        if username != '' and fname != '' and lname != '' and password != '' and conf_pass != '': 
            if username != password:
                if password == conf_pass:
                    if User.objects.filter(username=username).exists():
                        messages.warning(request, "User Already exists.")
                        return redirect('register')
                    
                    print("hello")
                    if User.objects.filter(email=email).exists():
                        messages.warning(request, "Email already exists.")
                        return redirect('register')
                    
                    print("hello")
                    user = User.objects.create_user(
                                    username=username, first_name=fname, last_name=lname, email=email, password=password)
                    user.save()
                    messages.success(request, "Thanks For Registering.")
                    print(f"{'-'*20} {username} = Validation Done {'-'*20}")
                    # Otp Process
                    print(f"{'-'*20} {username} = Otp Started Not Verified{'-'*20}")
                    user = auth.authenticate(request, username=username, password=password)
                    if user is not None:
                        user.is_active = True
                        # Storing user.pk in session
                        request.session['pk'] = user.pk
                        user.save()
                        return redirect('verification')    # After Successfully Crossing all Validations
                else:
                    print('Confirm Password Donot Match.')
                    messages.warning(request, "Confirm Password Donot Match.")
                    return redirect('register')
            else:
                print("Username Can't be Your Passoword.")
                messages.warning(request, "Username Can't be Your Passoword.")
                return redirect('register')
        else:
            print("Fields can't be Empty")
            messages.warning(request, "Fields Can't be Empty")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

# LOGIN
def login(request):
    try:
        User = get_user_model()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass1')

            print(f"username = {username}")
            print(f"password = {password}")

            print(f"{'-'*20} Got {username} info & Going Login {'-'*20}")
            user = auth.authenticate(username=username, password=password)
            print(user)

            if user is not None:
                if user.is_verified == True:
                    print(f"{'-'*20} {username} = Just Above Login() {'-'*20}")
                    auth.login(request, user)
                    print(f"{'-'*20} {username} = Login Done Successfully {'-'*20}")
                    request.session['pk'] = user.pk
                    messages.success(request, "Logged In Successfully")
                    return redirect('home')
                else:
                    user.delete()
                    print(f"{'-'*20} {username} = Account Verfication not Done {'-'*20}")
                    messages.warning(request, "Your Account is not Verfied, Please Register again")
                    return redirect('register')
            
            print(f"{'-'*20} {username} = User Not Found {'-'*20}")
            messages.warning(request, "Wrong Credentials Entered")
            return redirect('login')
        
        return render(request, 'accounts/login.html')

    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()


def customer(request):
    try:
        User = get_user_model()
        pk = request.session.get('pk')
        user = User.objects.get(pk=pk)
        customer, created = Customer.objects.get_or_create(user=user)
        customer = request.user.customer
        print(customer)
        return redirect('home')
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

# LOGOUT
def logout_user(request):
    try:
        print(f"{'-'*20} Inside Logout View {'-'*20}")
        user = request.user
        logout(request)

        print(f"{'-'*20} {user} Logout Done {'-'*20}")
        messages.success(request, "Logged Out Successfully!!")
        return redirect('home')

    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

# FORGOT PASSWORD
def forgot_pass(request):
    try:
        User = get_user_model()
        if request.method == "POST":
            email = request.POST.get('email')
            print(f"{'-'*20} Got Email {'-'*20}")

            if User.objects.filter(email=email).exists():
                email = User.objects.get(email=email)

                # Storing user.pk in session
                request.session['pk'] = email.pk

                print(f"{'-'*20} Redirecting to Verify User {'-'*20}")
                return redirect('forgotpass_verification')

            print(f"{'-'*20} {email} = No Matching Email in Database Found {'-'*20}")
            messages.warning(request, "No Matching Email Found ...")
            return render(request, 'accounts/forgot_pass.html')

        return render(request, 'accounts/forgot_pass.html')

    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

# REGISTER OTP CODE
def verification(request):
    try:
        User = get_user_model()
        pk = request.session.get('pk')

        if pk:
            print(f"{'-'*20} {pk} = Got Pk {'-'*20}")
            # Fetching Otp Number Generated
            otp = OtpCode.objects.get(pk=pk)

            user = get_user_model()

            # Fetching User to alter is_verified=True
            main_user = user.objects.filter(pk=pk).get()

            print(f"{main_user} = OTP : {otp}")

            if not request.POST:
                # Send Email
                verification_email(request, otp)

            if request.method == 'POST':
                num = request.POST.get('number')

                print(f"{'-'*20} {num} = Otp Entered {'-'*20}")

                if str(otp) == num:
                    messages.success(request, "Account Verified") 

                    print(f"{'-'*20} {main_user} = Otp Verified {'-'*20}")

                    main_user.is_verified = True
                    main_user.save()
                    otp.save()

                    print(f"{'-'*20} {main_user} = Going Login Page {'-'*20}")
                    return redirect('login')
                
                messages.warning(request, "Wrong OTP")
                print(f"{'-'*20} {main_user} = Not Verified Wrong Code {'-'*20}")
                return redirect('verification')

            # else:
            #     main_user.delete()
            #     print(f"{'-'*20} {username} = Account Verfication not Done {'-'*20}")
            #     messages.warning(request, "Your Account is not Verfied, Please Register again")
            #     return redirect('register')

            

        return render(request, 'accounts/register_otp.html')


    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()


# FORGOT OTP CODE
def forgotpass_verification(request):
    try:
        User = get_user_model()
        pk = request.session.get('pk')

        if pk:
            print(f"{'-'*20} {pk} = Got Pk {'-'*20}")
            # Fetching Otp Number Generated
            otp = OtpCode.objects.get(pk=pk)

            # Fetching User to alter is_verified=True
            main_user = User.objects.filter(pk=pk).get()

            print(f"{main_user} = OTP : {otp}")

            if not request.POST:
                # Send Email
                verification_email(request, otp)


            if request.method == 'POST':
                num = request.POST.get('number')

                print(f"{'-'*20} {num} = Otp Entered {'-'*20}")

                if str(otp) == num:
                    messages.success(request, "Account Verified") 
                    print(f"{'-'*20} {main_user} = Otp Verified {'-'*20}")


                    otp.save()  # This will change the Otp

                    return redirect('change_pass')

                messages.warning(request, 'Incorrect OTP')
                return redirect('forgotpass_verification')

            return render(request, 'accounts/forgotPass_otp.html')

    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

def change_pass(request):
    try:
        User = get_user_model()
        pk = request.session.get('pk')
        print("Inside Change Pass")

        if pk:
            if request.method == 'POST':
                new_pass = request.POST.get('pass1')   
                print(f"New Pass = {new_pass}") 

                # Fetching User to alter is_verified=True
                main_user = User.objects.filter(pk=pk).get()

                if new_pass != '':
                    if main_user.check_password(new_pass):
                        messages.warning(request, "You Entered Old Password")
                        return redirect('change_pass')

                    # Resetting Password
                    main_user.set_password(new_pass)
                    main_user.save()
                    print(f"{'-'*20} {main_user} = Password Changed Successfully {'-'*20}")
                    messages.success(request, 'Password Changed Successfully')
                    return redirect('login')

                messages.warning(request, 'Please Enter Your Password')
                return redirect('change_pass')

        return render(request, 'accounts/change_pass.html')
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()



# Dasboard
def myaccount(request):
    try:
        return render(request, 'user-dashboard/my-account.html')
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()
    

# Update Account Information
@login_required
def account_information(request):
    try:    
        if request.method == 'POST':
            # Collecting Users Data
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            user = request.user
            # user = User.objects.get(username=user.username)
            user = get_user_model().objects.get(username=user.username)
            customer = user.customer

            message = []
            # First Name 
            if user.first_name == fname:
                pass
            else:
                user.first_name = fname
                customer.first_name = fname
                message.append(f"First Name Updated.")
            
            # Last Name
            if user.last_name == lname:
                pass
            else:
                user.last_name = lname
                customer.last_name = lname
                message.append(f"Last Name Updated.")

            # Email
            if user.email == email:
                pass
            else:
                user.email = email
                message.append(f"Email Updated.")


            # Phone
            if user.phone == phone:
                pass
            else:
                user.phone = phone
                message.append(f"Phone Number Updated.")

            message = ", ".join(message)

            if message != "":
                message +=  " Please Refresh The Page To See Changes."

            messages.success(request, message)

            user.save()
            customer.save()

            print("Profile Updated ....")

        return render(request, 'user-dashboard/account-information.html')
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()
    
# Change Passwod
@login_required
def change_password(request):
    try:
        User = get_user_model()
        if request.method == "POST":
            # Collecting User Data
            old_pass = request.POST.get('oldpass')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            user = request.user
            user = User.objects.get(username=user.username)

            # Check for Current Password if True
            if user.check_password(old_pass):
                # Check for pass1 == pass2
                if pass1 == pass2:
                    # Check for New And Old Password
                    if user.check_password(pass1):
                        messages.warning(request, "You Entered Old Password.")
                        return redirect('change-password')

                    user.set_password(pass1)
                    auth.login(request, user)
                    user.save()

                    print(f"{'-'*20} {user} = Password Changed Successfully {'-'*20}")
                    messages.success(request, 'Password Changed Successfully')

                    print("Passowrd Changed ... ")

                else:
                    # if not pass1 == pass2
                    message.warning(request, "New Password and Confirm Password Do not Match.")
                    return redirect('change-password')

            else:
                messages.info(request, "Wrong Current Password.")
                return redirect('change-password')
        
        return render(request, 'user-dashboard/change-password.html')
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()
    
@login_required
def address_book(request):
    try:
        User = get_user_model()
        # Connect with Shipping Address Model
        customer = request.user.customer
        order = Order.objects.get(customer=customer, order_status="Pending", payment_status="Pending")
        print("Order1")
        shipping_address, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        print(order)

        # Fetching user's Data
        if request.method == "POST":
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            landmark = request.POST.get('landmark')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            city = request.POST.get('city')
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            print("HELLO")
            print(city)

            message = []
            # Address 1
            if shipping_address.address1 == address1:
                pass
            else:
                shipping_address.address1 = address1
                customer.address1 = address1
                message.append(f"Address1 Updated.")

            # Address 2
            if shipping_address.address2 == address2:
                pass
            else:
                shipping_address.address2 = address2
                customer.address2 = address2
                message.append(f"Address2 Updated.")
            
            # landmark
            if shipping_address.landmark == landmark:
                pass
            else:
                shipping_address.landmark = landmark
                customer.landmark = landmark
                message.append(f"Landmark Updated.")

            # state
            if shipping_address.state == state:
                pass
            else:
                shipping_address.state = state
                customer.state = state
                message.append(f"State Updated.")


            # Zipcode
            if shipping_address.zipcode == zipcode:
                pass
            else:
                shipping_address.zipcode = zipcode
                customer.zipcode = zipcode
                message.append(f"Zipcode Updated.")

            # City
            if shipping_address.city == city:
                pass
            else:
                shipping_address.city = city
                customer.city = city
                message.append(f"City Updated.")

            # Phone
            if shipping_address.phone == phone:
                pass
            else:
                shipping_address.phone = phone
                customer.phone = phone
                message.append(f"Phone Updated.")

            # Email
            if shipping_address.email == email:
                pass
            else:
                shipping_address.email = email
                message.append(f"Email Updated.")

            message = ", ".join(message)

            if message != "":
                message += " Please Refresh The Page To See Changes."

            messages.success(request, message)

            shipping_address.save()
            customer.save()

            print("Profile Updated ....")

        context = {
            'shipping_address': shipping_address,
        }

            


        return render(request, 'user-dashboard/address-book.html', context)
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()
    
@login_required
def order_history(request):
    try:
        User = get_user_model()
        # Fetching the customer's order details and order items
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, order_status="Confirm", payment_status="Done", complete=True)
        order_items = []
        for i in range(0, len(order)):
            order_items += order[i].orderitem_set.all()
        print(order_items)
            
        context = {
            'order_items': order_items,
        }


        return render(request, 'user-dashboard/order-history.html', context)
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

def return_order_request(request):
    try:
        User = get_user_model()
        # Fetching the customer's order details and order items
        data = json.loads(request.body)
        orderId = data['orderId']
        productId = data['productId']

        print('OrderID: ', orderId)
        print('ProductID: ', productId)


        customer = request.user.customer
        product = all_Product.objects.get(id=productId)
        order = Order.objects.get(customer=customer, order_number=orderId)
  

        
        print("helllo1")
        transaction_id = Transaction.objects.get(made_by=customer, order_id=order)
        print("helllo2")
        return_request, created = ReturnOrderRequest.objects.get_or_create(customer=customer, order=order, 
                    transaction_id=transaction_id, product=product)
        messages.success(request, "Your Return Order Request for Item"+ str(return_request.product) + "has been register, we will contact you asap.")
        return_request.save()

        return JsonResponse('Return Request Sent', safe=False)
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

def return_request(request):
    try:
        User = get_user_model()
        # Fetching the customer's order details and order items
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, order_status="Confirm", payment_status="Done", complete=True)
        items = []
        for i in range(0, len(order)):
            if order[i].orderitem_set.filter(delivery='Return Order Request Accepted').exists():
                items += order[i].orderitem_set.fliter(delivery='Return Order Request Accepted')
            elif order[i].orderitem_set.filter(delivery='Refunded').exists():
                items += order[i].orderitem_set.filter(delivery='Refunded')
                
        print(items)

            
        context = {
            'items': items,
        }

        return render(request, 'user-dashboard/return-order.html', context)
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()