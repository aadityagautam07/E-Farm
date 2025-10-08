from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('search/', views.search, name='search'),
    path('product/<int:id>/', views.product_detail, name='product_details'),
    path('store_filter/', views.store_filter, name='store_filter'),
    path('category_filter/', views.category_filter, name='category_filter'),
]