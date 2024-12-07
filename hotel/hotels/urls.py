from rest_framework import routers
from .views import *
from django.urls import path, include


router=routers.SimpleRouter()
router.register(r'user', ProfileViewSet, basename='user' )
router.register(r'hotel', HotelListViewSet, basename='hotel_list')
router.register(r'hotel_detail', HotelDetailViewSet, basename='hotel_detail')
router.register(r'room', RoomViewSet, basename='room' )
router.register(r'rating', RatingViewSet, basename='rating' )

urlpatterns = [
    path('',include(router.urls)),


    path('country/',CountryListApiView.as_view(), name='country_list'),
    path('country/<int:pk>/', CountryDetailApiView.as_view(), name='country_detail'),


]



