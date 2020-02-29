import requests
from django.shortcuts import render
from . import models
from django.utils import timezone
from bs4 import BeautifulSoup

BASE_FLIPKART_URL = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
BASE_IMAGE_URL = 'https://rukminim1.flixcart.com/image/312/312/k0lbdzk0pkrrdj/mobile-refurbished/z/j/2/c2-16-u-rmx1945-realme-2-original-imaffnumygt8wgfx.jpeg?q=70'

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
    final_url = BASE_FLIPKART_URL.format(search)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('div', {'class': '_1UoZlX'})
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='_3wU53n').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='_1vC4OE _2rQ-NK').text
        else:
            post_price = 'N/A'

        post_image_url = BASE_IMAGE_URL

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'listings': final_postings,
    }

    return render(request, 'first/sc_post.html', stuff_for_frontend)

