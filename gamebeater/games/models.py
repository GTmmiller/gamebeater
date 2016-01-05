from __future__ import unicode_literals

from django.db import models

from goals.models import Goal

class Console(models.Model):
	CURRENT_GEN = 8
	DEFAULT_EMULATABLE = False

	name = models.CharField(
		max_length=200,
		primary_key=True
	)
	emulatable = models.BooleanField(
		default=DEFAULT_EMULATABLE
	)
	generation = models.PositiveSmallIntegerField(
		default=CURRENT_GEN
	)
	
	def __unicode__(self):
		return self.name

class Genre(models.Model):
	DEFAULT_DESCRIPTION = "There's no description for this genre yet."

	name = models.CharField(
		max_length=200,
		primary_key=True
	)
	description = models.CharField(
		max_length = 500,
		default = DEFAULT_DESCRIPTION 
	)
	
	def __unicode__(self):
		return self.name

class Game(models.Model):
	title = models.CharField(
		max_length=200,
		unique=True
	)
	genres = models.ManyToManyField(Genre)
	consoles = models.ManyToManyField(Console)
	goal = models.OneToOneField(
		Goal,
		on_delete=models.CASCADE,
		default=None
	)
	
	def get_goal_start_time(self):
		return self.goal.start_time
	
	def get_goal_status(self):
		return self.goal.get_status_display()
	
	def get_goal_complete_time(self):
		return self.goal.complete_time
	
	def get_goal_text(self):
		return self.goal.goal.text
	
	def __unicode__(self):
		return self.title


	
	
