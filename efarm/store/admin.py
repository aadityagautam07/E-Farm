from django.contrib import admin
from django.utils.html import format_html
from .models import all_Product

# Register your models here.
class all_ProductAdmin(admin.ModelAdmin):

    # Properties 
    def myphoto(self, object):
        return format_html('<img src="{}" width="100"/>'.format(object.photo1.url))

    # Overwriting the list.
    list_display = ('stock_status', 'myphoto', 'product_name', 'original_price', 'discount', 'category', 
                    'created_date', 'on_sale', 'is_featured', )
    actions = ['discount_30', 'discount_40', 'discount_60', 'discount_80', 'remove_discount', ]
    list_display_links = ('product_name', )
    search_fields = ('product_name', 'category', 'on_sale',)
    list_filter = ('category', 'on_sale', )
    list_editable = ('category', 'discount', 'on_sale', 'is_featured', )

    def discount_30(self, request, queryset):
        discount = 30 # percentage

        for product in queryset:
            multiplier = discount / 100
            old_price = product.original_price
            new_price = old_price - (old_price * multiplier)
            product.after_discount_price = new_price
            product.discount_amount = old_price * multiplier
            product.discount = '30%'
            product.on_sale = True
            product.save(update_fields=['after_discount_price', 'discount_amount', 'discount', 'on_sale'])
    
    discount_30.short_description = 'Set 30%% discount'

    def discount_40(self, request, queryset):
        discount = 40 # percentage

        for product in queryset:
            multiplier = discount / 100
            old_price = product.original_price
            new_price = old_price - (old_price * multiplier)
            product.after_discount_price = new_price
            product.discount_amount = old_price * multiplier
            product.discount = '40%'
            product.on_sale = True
            product.save(update_fields=['after_discount_price', 'discount_amount', 'discount', 'on_sale'])
    
    discount_40.short_description = 'Set 40%% discount'

    def discount_60(self, request, queryset):
        discount = 60 # percentage

        for product in queryset:
            multiplier = discount / 100
            old_price = product.original_price
            new_price = old_price - (old_price * multiplier)
            product.after_discount_price = new_price
            product.discount_amount = old_price * multiplier
            product.discount = '60%'
            product.on_sale = True
            product.save(update_fields=['after_discount_price', 'discount_amount', 'discount', 'on_sale'])
    
    discount_60.short_description = 'Set 60%% discount'

    def discount_80(self, request, queryset):
        discount = 80 # percentage

        for product in queryset:
            multiplier = discount / 100
            old_price = product.original_price
            new_price = old_price - (old_price * multiplier)
            product.after_discount_price = new_price
            product.discount_amount = old_price * multiplier
            product.discount = '80%'
            product.on_sale = True
            product.save(update_fields=['after_discount_price', 'discount_amount', 'discount', 'on_sale'])
    
    discount_80.short_description = 'Set 80%% discount'

    def remove_discount(self, request, queryset):
        discount = 0 # percentage

        for product in queryset:
            multiplier = discount / 100
            old_price = product.original_price
            new_price = old_price - (old_price * multiplier)
            product.after_discount_price = new_price
            product.discount_amount = old_price * multiplier
            product.discount = '0%'
            product.on_sale = False
            product.save(update_fields=['after_discount_price', 'discount_amount', 'discount', 'on_sale'])
    
    remove_discount.short_description = 'Remove Discount'

    # Stock Status
    def stock_status(self, obj):
        if obj.stock != '0':  
            return format_html('<i class="fa fa-check" style="font-size:20px;color:green"></i>')
        else:
            return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')


admin.site.register(all_Product, all_ProductAdmin)