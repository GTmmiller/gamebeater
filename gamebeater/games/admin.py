from django.contrib import admin

from .models import Game, Platform, Genre

admin.site.register(Game)
admin.site.register(Platform)
admin.site.register(Genre)
