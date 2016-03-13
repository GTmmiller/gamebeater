from django.conf.urls import url

from . import views
from .views import DashboardView, CompletionStatusUpdateView, AddGamesView, GameOwnershipCreationView, GameOwnershipUpdateView, GoalDashboardView, CreateGoalView, GoalCompletionStatusUpdateView, GameOwnershipDeletionView, GoalDeletionView

app_name = 'profiles'
urlpatterns = [
	# ex: /profiles/register/
	url(r'^register/$', views.register, name='register'),
	# ex: /profiles/dashboard/
	url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
	# ex: /profiles/gameownerships/1/completion_status
	url(r'^gameownerships/(?P<pk>[0-9]+)/completion_status/$', CompletionStatusUpdateView.as_view(), name='completion_status_update'),
    # ex: /profiles/add_games/
    url(r'^add_games/$', AddGamesView.as_view(), name='add_games'),
    # ex: /profiles/gameownerships/
    url(r'^gameownerships/$', GameOwnershipCreationView.as_view(), name='create_ownership'),
    # ex: /profiles/gameownerships/1/
    url(r'^gameownerships/(?P<pk>[0-9]+)/$', GameOwnershipUpdateView.as_view(), name='update_ownership'),
    # ex: /profiles/gameownerships/1/delete/
    url(r'^gameownerships/(?P<pk>[0-9]+)/delete/$', GameOwnershipDeletionView.as_view(), name='delete_ownership'),
    # ex: /profiles/gameownerships/1/goals
    url(r'^gameownerships/(?P<pk>[0-9]+)/goals/$', GoalDashboardView.as_view(), name='goal_dashboard'),
    # ex: /profiles/gameownerships/1/add_goals
    url(r'^goals/$', CreateGoalView.as_view(), name='add_goals'),
    # ex: /profiles/goals/1/
    url(r'^goals/(?P<pk>[0-9]+)/$', GoalCompletionStatusUpdateView.as_view(), name='update_goal'),
    # ex: /profiles/goals/1/delete/
    url(r'^goals/(?P<pk>[0-9]+)/delete/$', GoalDeletionView.as_view(), name='delete_goal')
]