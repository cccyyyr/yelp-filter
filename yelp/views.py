from django.http import HttpResponse
from django.shortcuts import render

from .yelp_wrapper import Restaurant, YelpWrapper
#from pymagnitude import *
from .models import Category

def home(request):
    return render(request, 'home.html')

def splash(request):
    return render(request, 'splash.html')
    
def search(request):
    return render(request, 'search.html')

def search_result(request, location, price, categories, sort_by="rating", open_now=True):
    yelp = YelpWrapper()
    result = yelp.search(location=location, categories=categories, open_now=open_now, sort_by=sort_by, price=price)
    context = {'restaurant_list': result}
    return render(request, 'home.html', context)

