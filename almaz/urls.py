from django.urls import path

from .views import *

# аналогично адресу http://kovach/signal
urlpatterns = [path("signal", Kovach, name='kovach_input_signals'),
               path("1", test_get_data),
               path("kovach_data", get_kovach_data, name='get_kovach_data')
               ]
