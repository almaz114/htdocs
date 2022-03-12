from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

# аналогично адресу http://umbrella/main
urlpatterns = [
    path("main", cache_page(1)(main), name='main'),
    path("statistics", cache_page(1)(statistics_site), name="statistics"),
    path("about_system", cache_page(1)(about_system), name="about_system")
]
