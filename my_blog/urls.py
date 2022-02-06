from django.conf.urls import include
from django.contrib import admin

from my_blog import settings
from almaz.views import *       # мой личное приложение
from django.urls import path
from django.conf.urls.static import static


urlpatterns = [
    path('hedge/', hedge),          # edit json file hedge_martin
    path('trade_extremum/', index_5),        # edit json file trade_extremum
    path('global_levels/', global_levels),   # edit json file global_levels
    path('otchet/', index_6),           # отчет из json
    path('table/', index_7),            # вывод итога из json_files to Html + Css

    path("kovach/", include("almaz.urls")),     # for kovach signals   # аналогично адресу http://kovach/
    path("test/", include("almaz.urls")),        # for test get data(json) from server
    path("umbrella/", include("umbrella.urls"))   # for Umbrella site --> Main page
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = pageNotFound
