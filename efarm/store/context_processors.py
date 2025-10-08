from .models import *
from customer.models import *

# For the Guest User only

def extras(request):

    
    discounts = all_Product.objects.all()
    print(discounts)

    context = {
        'discounts': discounts,
    }

    return context
