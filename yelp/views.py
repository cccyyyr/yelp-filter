from django.http import HttpResponse
from django.shortcuts import render

from .yelp_wrapper import Restaurant, YelpWrapper
from pymagnitude import *
from .models import Category

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def search_result(request, location, price="1,2,3,4", categories="All", sort_by="rating", open_now=False):
    yelp = YelpWrapper()
    result = yelp.search(location=location, categories=categories, open_now=open_now, sort_by=sort_by, price=price)
    context = {'restaurant_list': result}
    return render(request, 'home.html', context)

