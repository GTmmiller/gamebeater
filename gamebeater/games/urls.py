from django.conf.urls import url

from . import views

app_name = 'games'
urlpatterns = [
	# ex: /games/
	url(r'^$', views.GameIndexView.as_view(), name='games')
]