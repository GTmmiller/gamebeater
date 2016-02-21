from django.conf.urls import url

from . import views
from .views import DashboardView, CompletionStatusUpdateView, AddGamesView, GameOwnershipCreationView, GameOwnershipUpdateView

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
    url(r'^gameownerships/(?P<pk>[0-9]+)/$', GameOwnershipUpdateView.as_view(), name='update_ownership')
]