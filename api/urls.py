from django.urls import include, re_path

from api.endpoints import config, exchange, loan

urlpatterns = [
    re_path(r'^api/', include(exchange.URLS)),
    re_path(r'^api/', include(config.URLS)),
    re_path(r'^api/', include(loan.URLS))]
