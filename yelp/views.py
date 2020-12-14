from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SearchForm
from .yelp_wrapper import Restaurant, YelpWrapper


def home(request):
    return render(request, 'home.html')


def splash(request):
    return render(request, 'splash.html')


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data["location"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            open_now = form.cleaned_data["hours"]
            return redirect(f"{location}/{price}/{category}/{open_now}")
    else:
        form = SearchForm()
    return render(request, 'search.html', {"form": form})


def search_result(request, location, price=1, categories="", open_now="True"):
    yelp = YelpWrapper()
    categories=YelpWrapper.parse(categories)
    result = yelp.search(location=location, categories=categories, open_now=open_now, sort_by="rating", price=str(price))
    context = {'restaurant_list': result}
    return render(request, 'home.html', context)
