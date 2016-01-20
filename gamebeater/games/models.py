from __future__ import unicode_literals

from django.db import models

class Platform(models.Model):
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
	platforms = models.ManyToManyField(Platform)
	
	def __unicode__(self):
		return self.title
