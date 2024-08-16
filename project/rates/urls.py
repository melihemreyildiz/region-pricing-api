from django.urls import path
from .views import AveragePriceView

urlpatterns = [
    path('rates/', AveragePriceView.as_view(), name='average_price'),
]

"""
Both the origin, destination params accept either port codes or region slugs checker endpoints 
http://127.0.0.1:8000/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=china_main&destination=north_europe_main
http://127.0.0.1:8000/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main
http://127.0.0.1:8000/rates/?date_from=2016-01-01&date_to=2016-01-10&origin=china_main&destination=BEZEE
"""