from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

# аналогично адресу http://umbrella/main
urlpatterns = [
    path("main", cache_page(60)(main), name='main'),
    path("statistics", cache_page(60)(statistics_site), name="statistics")
]
