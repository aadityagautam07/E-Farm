from django.shortcuts import render
from .models import OurTeam, LatestBlog, HomeSlider
from store.models import all_Product
from customer.models import *
from django.http import Http404, HttpResponse, HttpResponseForbidden
from contact_Us.models import *
from django.contrib import messages

# Importing below because we have modified the User model
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def home(request):
    # Making user our customer
    try:
        user = get_user_model()

        if request.user.is_authenticated:
            user = request.user
            print(user)

            try:
                if user.customer:
                    print("Yes")
                    customer = Customer.objects.get(user=user)
                    print("Already a Customer")
                
            except:
                print("No")
                customer = Customer.objects.create(user=user, first_name=user.first_name, last_name=user.last_name, email=user.email)
                print("Customer Created")

            

    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

    # Gettings Our Latest Blogs data
    blog = LatestBlog.objects.all()
    
    # Gettings Home Slider data
    sliders = HomeSlider.objects.all()

    sales = all_Product.objects.filter(on_sale=True)      # On sale 
    is_featured = all_Product.objects.filter(is_featured=True)      # Is featured 
    



    context = {
        'blog': blog,
        'sliders': sliders, 
        'sales': sales,
        'is_featured': is_featured,
    }

    # For store filter
    request.session['filter_value'] = '0' 

    return render(request, "webpages/home.html", context)
    
def about(request):

    # Gettings Our Team Members data
    teams = OurTeam.objects.all()

    context = {
        'teams' : teams,
    }

    return render(request, "webpages/about.html", context)  

def contact(request):
    try:
        # Fetching form data
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            contactUs_form = Contact_Mail.objects.create(name=name, email=email, subject=subject, description=message)
            contactUs_form.save()

            messages.success(request, "Will get in touch shortly.")

        return render(request, "webpages/contactUs.html")
    except Exception as e:
        print("Error : ", e)
        return HttpResponseForbidden()

    

def gallery(request):

    machinery_product = all_Product.objects.order_by('created_date').filter(category='machinery')
    crops_product = all_Product.objects.order_by('created_date').filter(category='crops')
    fertilizers_product = all_Product.objects.order_by('created_date').filter(category='fertilizers')
    seeds_product = all_Product.objects.order_by('created_date').filter(category='seeds')

    context = {
        'machinery_product': machinery_product,
        'crops_product': crops_product,
        'fertilizers_product': fertilizers_product,
        'seeds_product': seeds_product,
    }

    print(context)

    return render(request, "webpages/gallery.html", context)
    