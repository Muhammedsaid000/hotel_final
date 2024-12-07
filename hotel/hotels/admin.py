from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from .translation import *


class RoomPhotosInline(admin.TabularInline):
    model = RoomPhotos
    extra = 1


@admin.register(Room,)
class RoomAdmin(TranslationAdmin):
    inlines = [RoomPhotosInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(Hotel)
admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(Rating)

