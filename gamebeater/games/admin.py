from django.contrib import admin

from .models import Game, Console, Genre

class GameAdmin(admin.ModelAdmin):
	fieldsets = [
		('Start time', {'fields': ['get_goal_start_time']}),
		('Status', {'fields': ['get_goal_status']}),
		('Complete time', {'fields': ['get_goal_complete_time']}),
		('Goal', {'fields': ['get_goal_text']}),
	]

	list_display = ('title', 'get_goal_start_time', 'get_goal_status', 'get_goal_complete_time', 'get_goal_text')
	search_fields = ['title']

admin.site.register(Game, GameAdmin)
admin.site.register(Console)
admin.site.register(Genre)
