from django.urls import path
from . import views, admin


urlpatterns = [
    path('https://poornartha.github.io/webscraper/', views.home, name='home'),
    path('https://poornartha.github.io/webscraper/new_search', views.new_search, name="new_search"),
    path('https://poornartha.github.io/webscraper/new_prod', views.new_prod, name="new_prod"),
    path('https://poornartha.github.io/webscraper/save_product', views.save_prod, name="save_prod"),
    path('https://poornartha.github.io/webscraper/new_scrape', views.scrape, name="new_scrape"),
]

