from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('reviews', views.reviews, name='reviews'),
    path('equipment', views.equipment, name='equipment'),
    path('location', views.location, name='location'),
]