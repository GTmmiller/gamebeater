from django.conf.urls import url

from . import views
from .views import DashboardView, CompletionStatusUpdateView

app_name = 'profiles'
urlpatterns = [
	# ex: /profiles/register/
	url(r'^register/$', views.register, name='register'),
	# ex: /profiles/dashboard/
	url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
	# ex: /profiles/gameownership/1/completion_status
	url(r'^gameownership/(?P<pk>[0-9]+)/completion_status/$', CompletionStatusUpdateView.as_view(), name='completion_status_update')
]