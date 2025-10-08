from django.urls import path
from . import views

# Custom Urls
urlpatterns = [
    path('login/', views.login, name='login'),
    path('customer/', views.customer, name='customer'),
    path('register/', views.register, name='register'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('verification/', views.verification, name='verification'),
    path('forgotpass_verification/', views.forgotpass_verification, name='forgotpass_verification'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('my-account/', views.myaccount, name='my-account'),
    path('account-information/', views.account_information, name='account-information'),
    path('change-password/', views.change_password, name='change-password'),
    path('address-book/', views.address_book, name='address-book'),
    path('order-history/', views.order_history, name='order-history'),
    path('return_order_request/', views.return_order_request, name='return_order_request'),
    path('return_request/', views.return_request, name='return_request'),
]