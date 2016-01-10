from django.contrib import admin

from .models import Game, Console, Genre

admin.site.register(Game)
admin.site.register(Console)
admin.site.register(Genre)
