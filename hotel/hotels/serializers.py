from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['username', 'email', 'password', 'first_name','last_name',
                'age','phone_number','account_type',]
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        user=Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
        }


class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh=RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Недействительный или уже отозванный токен'})



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


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields=['room','start_date','end_date','status','types',]


class RoomSerializer(serializers.ModelSerializer):
    room_photos = RoomPhotosSerializer(many=True, read_only=True)
    room_number=BookingSerializer(many=True,read_only=True)
    class Meta:
        model=Room
        fields=['hotel','room_photos','price','is_available','room_number','description']


class HotelDetailSerializer(serializers.ModelSerializer):
    room_books=RoomSerializer(many=True, read_only=True)
    country=CountryListSerializer(read_only=True)
    class Meta:
        model=Hotel
        fields=['hotel_name','country','types','description','hotel_image','room_books']


class CountryDetailSerializer(serializers.ModelSerializer):
    country_hotels=HotelListSerializer(read_only=True, many=True,)
    class Meta:
        model=Country
        fields=['country_name','country_hotels']