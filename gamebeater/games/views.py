from django.shortcuts import render
from django.views import generic

from .models import Game

class GameIndexView(generic.ListView):
	model = Game
	template_name = 'games/games_index.html'
	context_object_name = 'game_list'