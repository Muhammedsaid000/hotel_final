from random import choices
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser



class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(
        default=18, null=True, blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(70)]
    )
    phone_number = PhoneNumberField(region='', null=True, blank=True)
    STATUS_CHOICES = (
        ('owner', 'Owner'),
        ('client', 'Client')
    )
    account_type = models.CharField(max_length=16, choices=STATUS_CHOICES, default='client', null=True, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Country(models.Model):
    country_name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.country_name


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='country_hotels', on_delete=models.CASCADE)
    TYPES_CHOICES = (
        ('«I звезд»', '«I звезд»'),
        ('«II звезд»', '«II звезд»'),
        ('«III звезд»', '«III звезд»'),
        ('«IV звезд»', '«IV звезд»'),
        ('«V звезд»', '«V звезд»'),
    )
    types = MultiSelectField(choices=TYPES_CHOICES, max_length=100, max_choices=15)
    description = models.TextField()
    hotel_image = models.ImageField(upload_to='hotel_img/')
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel_name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    price=models.PositiveSmallIntegerField(default=0)
    BRON_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован', 'забронирован'),
        ('занят', 'занят'),
    )
    bron = models.CharField(choices=BRON_CHOICES, max_length=15)
    TYPES_CHOICES = (
        ('«Двухместный номер с 1 кроватью»', '«Двухместный номер с 1 кроватью»'),
        ('«Одноместный номер эконом-класса»', '«Одноместный номер эконом-класса»'),
        ('«Улучшенный люкс с кроватью размера «king-size»', '«Улучшенный люкс с кроватью размера «king-size»'),
        ('«Семейный номер»', '«Семейный номер»'),
    )
    types = MultiSelectField(choices=TYPES_CHOICES)
    description = models.TextField()
    user=models.ForeignKey(Profile, on_delete=models.CASCADE)


class RoomPhotos(models.Model):
    room = models.ForeignKey(Room, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_img/')


class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews',)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг", null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)