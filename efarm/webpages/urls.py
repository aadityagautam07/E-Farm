from django.urls import path
from . import views

# Custom Urls
urlpatterns = [
    path('', views.home, name='home'),
    path('about us/', views.about, name='about'),
    path('contact us/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
]