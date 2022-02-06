from django.urls import path

from .views import *

# аналогично адресу http://kovach/signal
urlpatterns = [path("signal", Kovach),
               path("1", test_get_data)
               ]
