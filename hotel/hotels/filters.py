import django_filters
from .models import *


class HotelListFilter(django_filters.FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'hotel_name': ['exact'],
            'country': ['exact'],
            'types': ['exact'],
        }


class RoomListFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            'hotel': ['exact'],
            'types': ['exact'],
            'price':['gt', 'lt'],
            'is_available':['exact'],

        }
