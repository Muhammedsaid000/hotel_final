from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['username', 'email', 'password', 'first_name','last_name',
                'age','phone_number','account_type',]


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields=['country_name']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields=['user','stars','text','created_date']


class HotelListSerializer(serializers.ModelSerializer):
    reviews=RatingSerializer(many=True, read_only=True)
    country=CountryListSerializer(read_only=True)
    class Meta:
        model=Hotel
        fields=['hotel_name','country','types','description','hotel_image','reviews',]


class RoomPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhotos
        fields = ['image']

class RoomSerializer(serializers.ModelSerializer):
    photos = RoomPhotosSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['bron', 'types', 'description', 'photos']


class HotelDetailSerializer(serializers.ModelSerializer):
    rooms=RoomSerializer(many=True, read_only=True)
    country=CountryListSerializer(read_only=True)
    class Meta:
        model=Hotel
        fields=['hotel_name','country','types','description','hotel_image','rooms']


class CountryDetailSerializer(serializers.ModelSerializer):
    country_hotels=HotelListSerializer(read_only=True, many=True,)
    class Meta:
        model=Country
        fields=['country_name','country_hotels']