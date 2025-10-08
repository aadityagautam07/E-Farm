from django.urls import path
from . import views
from django.contrib import admin

# Custom Urls
admin.site.site_header = 'FreshShop'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('update_Item/', views.updateItem, name='update_Item'),
    path('checkout/', views.checkout, name='checkout'),
    path('updation/<str:payment_status>/', views.updation, name='updation'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('callback/', views.callback , name='callback'),
]

