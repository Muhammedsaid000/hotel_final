from .models import Hotel, Room
from modeltranslation.translator import TranslationOptions, register

@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('description',)
