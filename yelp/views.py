from django.shortcuts import render, redirect
from .forms import SearchForm
from .yelp_wrapper import YelpWrapper


def home(request):
    return render(request, 'home.html')


def splash(request):
    return render(request, 'splash.html')


def search(request):
    '''
    :param request: search request. Either they wish to submit their query and go to the result page or they hope to start
    :return: corresponding HTTP request
    '''
    if request.method == "POST":
        '''
        when a user has filled out a search request and hit submit, we direct them to the appropriate page that will have
        the information they are looking for.
        '''
        form = SearchForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data["location"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            open_now = form.cleaned_data["hours"]
            return redirect(f"{location}/{price}/{category}/{open_now}")
    else:
        '''
        a user wishes to begin searching
        '''
        form = SearchForm()
    return render(request, 'search.html', {"form": form})


def search_result(request, location, price=1, categories="", open_now="True"):
    '''
    :param request: HTTP request(unused)
    :param location: the location param in the link
    :param price: the price param in the link
    :param categories: the category param in the link
    :param open_now: the opne_now param in the link
    :return: a HTTP response with the list of restaurant information the link is requesting for.
    '''
    yelp = YelpWrapper()
    categories=YelpWrapper.parse(categories)
    result = yelp.search(location=location, categories=categories, open_now=open_now, sort_by="rating", price=str(price))
    context = {'restaurant_list': result}
    return render(request, 'home.html', context)
