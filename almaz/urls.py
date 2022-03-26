from django.urls import path

from .views import *

# аналогично адресу http://kovach/signal
urlpatterns = [path("signal", Kovach, name='kovach_input_signals'),
               path("expire_data", get_expire_data, name='expire_data'),
               path("kovach_data", get_kovach_data, name='get_kovach_data')
               ]
