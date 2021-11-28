from django.http.response import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django import forms

from .models import Review, Equipment

class SearchForm(forms.Form):
    query = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Search Equipment"}))

# Create your views here.
def index(request):
    return render(request, 'iron_arms/index.html')

def contact(request):
    return render(request, 'iron_arms/contact.html')

def location(request):
    return render(request, 'iron_arms/location.html')

def equipment(request):
    search_form = SearchForm()
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            items = Equipment.objects.filter(name__icontains=query)
    else:
        items = Equipment.objects.all()
    return render(request, 'iron_arms/equipment.html', {
        "equipment": items,
        "form": search_form,
    })

def reviews(request):
    user_reviews = Review.objects.all()
    return HttpResponse(serializers.serialize('json', user_reviews))
