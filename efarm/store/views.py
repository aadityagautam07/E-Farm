from django.shortcuts import render
from .models import all_Product
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# Create your views here.
def store(request):

    # Sort By
    filter = request.session.get('filter_value')
    print(filter)

    # Catergory Wise
    category_filter = request.session.get('category_filter')
    print("Catergory filter = ", category_filter)

    h_l = all_Product.objects.all().order_by('-original_price')  # High to low
    l_h = all_Product.objects.all().order_by('original_price')   # Low to High
    sales = all_Product.objects.filter(on_sale=True)      # On sale 
    print(F"Sales = {sales}")

        # if filter == '0':
        #     del request.session['filter_value']

    print("Session = ",request.session.get('filter_value'))


    # sort and category at same time
    machinery_h_l = all_Product.objects.order_by('-original_price').filter(category='machinery')  # High to low
    fertilizer_h_l = all_Product.objects.order_by('-original_price').filter(category='fertilizers')  # High to low
    seed_h_l = all_Product.objects.order_by('-original_price').filter(category='seeds')  # High to low

    machinery_l_h = all_Product.objects.order_by('original_price').filter(category='machinery')  # Low to High
    fertilizer_l_h = all_Product.objects.order_by('original_price').filter(category='fertilizers')  # Low to High
    seed_l_h = all_Product.objects.order_by('original_price').filter(category='seeds')  # Low to High

    machinery_sales = all_Product.objects.filter(on_sale=True, category='machinery')      # On sale 
    fertilizer_sales = all_Product.objects.filter(on_sale=True, category='fertilizers')   # Low to High
    seed_sales = all_Product.objects.filter(on_sale=True, category='seeds')   # Low to High

    print(machinery_sales)



    all_products = all_Product.objects.all()
    machinery_product = all_Product.objects.order_by('created_date').filter(category='machinery')
    # crops_product = all_Product.objects.order_by('created_date').filter(category='crops')
    fertilizers_product = all_Product.objects.order_by('created_date').filter(category='fertilizers')
    seeds_product = all_Product.objects.order_by('created_date').filter(category='seeds')

    print(sales)

    context = {
        'all_products': all_products,
        'machinery_product': machinery_product,
        'fertilizers_product': fertilizers_product,
        'seeds_product': seeds_product,

        # Filter
        'h_l': h_l,
        'l_h': l_h,
        'sales': sales,

        # Catergory and Filter same time
        'machinery_h_l': machinery_h_l,
        'fertilizer_h_l': fertilizer_h_l,
        'seed_h_l': seed_h_l,
        'machinery_l_h': machinery_l_h,
        'fertilizer_l_h': fertilizer_l_h,
        'seed_l_h': seed_l_h,
        'machinery_sales': machinery_sales,
        'fertilizer_sales': fertilizer_sales,
        'seed_sales': seed_sales,
    }

    print(filter)

    return render(request, "store/store.html", context)

def product_detail(request, id):
    product = get_object_or_404(all_Product, pk=id)

    is_featured = all_Product.objects.filter(is_featured=True)
    data = {
        'product': product,
        'is_featured': is_featured,
    }

    return render(request, "store/product_details.html", data)

def search(request):

    if 'keyword' in request.GET:
        queryset= request.GET.get('keyword', '').split(" ")
        submitbutton= request.GET.get('submit')

        if queryset is not None:

            queryset_list1= Q()

            for query in queryset:
                queryset_list1 |= (
                Q(product_name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
                )
            
            products = all_Product.objects.filter(queryset_list1).distinct().order_by('-created_date')

            context={
                'products': products,
                'submitbutton': submitbutton
            }
            print(context)
            return render(request, 'store/search.html', context)

def store_filter(request):
    # Fetching the Store Filter 
    data = json.loads(request.body)
    filter_value = data['Selected_Value']

    print("Filter: ", filter_value)

    request.session['filter_value'] = filter_value
    
    

    return JsonResponse(filter_value, safe=False)

def category_filter(request):
    # Fetching the Store Filter 
    data = json.loads(request.body)

    if data['machinery']:
        request.session['category_filter'] = 'machinery'
    elif data['fertilizer']:
        request.session['category_filter'] = 'fertilizer'
    elif data['seed']:
        request.session['category_filter'] = 'seed'
    elif data['all']:
        if request.session.get('category_filter'):
            del request.session['category_filter']


    return JsonResponse(request.session.get('category_filter'), safe=False)