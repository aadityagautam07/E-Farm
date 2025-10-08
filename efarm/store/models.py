from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Q

# For Sending Email
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage
from django.conf import settings





# Create your models here.
class all_Product(models.Model):

    category_choices = (
        ('machinery', 'machinery'),
        ('fertilizers', 'fertilizers'),
        ('seeds', 'seeds'),
    )

    photo1 = models.ImageField(upload_to='media/product/%Y/', default=False)
    photo2 = models.ImageField(upload_to='media/product/%Y/', default=False)
    photo3 = models.ImageField(upload_to='media/product/%Y/', default=False)
    front_image = models.ImageField(upload_to='media/product/%Y/', default=False)
    product_name = models.CharField(max_length=255, null=True, default=False)
    on_sale = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    description = RichTextField(null=True, blank=True, default=False)
    after_discount_price = models.FloatField(null=True, blank=True, default=False)
    discount_amount = models.FloatField( blank=True, default=False)
    discount = models.CharField(max_length=100,  blank=True, default='0%')
    original_price = models.FloatField( blank=True, null=False)
    category = models.CharField(choices=category_choices, max_length=255, default="")
    stock = models.CharField(max_length=255, null=True, blank=True, default="0")
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.discount != '0%' or self.discount_amount != 0.0:
            discount = self.discount.replace('%', '')
            multiplier = float(discount )/ 100
            og_price = self.original_price
            print(og_price)
            new_price = og_price - (og_price * multiplier)
            self.discount_amount = og_price * multiplier
            self.after_discount_price = new_price
            self.on_sale = True

            all_product = all_Product.objects.filter(~Q(discount='0%'))
            print(all_product)

        else:
            self.on_sale = False
            self.after_discount_price = 0.0
            self.discount_amount = 0.0

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name    
