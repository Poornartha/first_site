from django.urls import path
from . import views, admin


urlpatterns = [
    path('', views.home, name='home'),
    path('new_search', views.new_search, name="new_search"),
    path('new_prod', views.new_prod, name="new_prod"),
    path('save_product', views.save_prod, name="save_prod"),
    path('new_scrape', views.scrape, name="new_scrape"),
]

