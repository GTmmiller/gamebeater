from django.contrib import admin

from .models import Game, Console, Genre

class GameAdmin(admin.ModelAdmin):
	list_display = ('title', 'get_goal_start_time', 'get_goal_status', 'get_goal_complete_time', 'get_goal_text')

admin.site.register(Game, GameAdmin)
admin.site.register(Console)
admin.site.register(Genre)
