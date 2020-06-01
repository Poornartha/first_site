import requests
from django.shortcuts import render
from . import models
from django.utils import timezone
from bs4 import BeautifulSoup
from requests.compat import quote_plus

BASE_FLIPKART_URL = 'https://www.bewakoof.com/search/{}'

# Create your views here.
'''search?q=xiomi&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off
search?q=realme&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off
/search?q=realme%20phone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'''


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    li = models.Product.objects.filter(name__contains=search)
    context = {
        'search': search,
        'listings': li,
    }
    return render(request, 'first/new_search.html', context)


def new_prod(request):
    return render(request, "first/new_prod.html")


def save_prod(request):
    name = request.POST.get('name')
    prize = request.POST.get('prize')
    image = request.POST.get('image')
    models.Product.objects.create(name=name, prize=prize, image=image)
    return render(request, 'base.html')


def scrape(request):
    search = request.POST.get('search')
    final_url = BASE_FLIPKART_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    wrap = soup.find('div', {'class': 'categoryGridWrapper'})
    image_set = wrap.find_all('img')
    link_set = wrap.find_all('a')
    image_collection = []
    link_collection = []

    for link in link_set:
        check = link.get('href')
        link_collection.append(check)


    for image in image_set:
        check = image['src']
        if check != "https://images.bewakoof.com/web/b-coin-gold-3x.png":
            image_collection.append(check)

    for image in image_collection:
        if image == "https://images.bewakoof.com/web/b-coin-gold-3x.png":
            image_collection.remove(image)

    post_listings = soup.find_all('div', {'class': 'productCardDetail'})
    final_postings = []
    i = 0
    while i<10:
        post = post_listings[i]
        post_title = post.find('h3').text
        post_price = post.find('b').text
        link_base = "https://www.bewakoof.com{}"
        final_postings.append((post_title, post_price, image_collection[i], link_base.format(link_collection[i+5])))
        i = i + 1

    stuff_for_frontend = {
        'search': search,
        'listings': final_postings,
    }

    return render(request, 'first/new_search.html', stuff_for_frontend)

