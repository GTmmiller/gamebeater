from django.contrib import admin

from .models import GoalText, ProgressLog, Goal

admin.site.register(GoalText)
admin.site.register(ProgressLog)
admin.site.register(Goal)
