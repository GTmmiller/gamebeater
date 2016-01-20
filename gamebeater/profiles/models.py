from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from games.models import Game, Platform
from .utils import CompletionStatus

class GamebeaterProfile(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL
	)
	games = models.ManyToManyField(
		Game, 
		through='GameOwnership'
	)
	
	def __unicode__(self):
		return self.user.username 

class GameOwnership(models.Model):
	WANTS = 'W'
	BORROWS = 'B'
	OWNES_PHYSICAL = 'P'
	OWNES_VIRTUAL = 'V'
	OWNERSHIP_STATUS_CHOICES = (
		(WANTS, 'Wants'),
		(BORROWS, 'Borrows'),
		(OWNES_PHYSICAL, 'Owns Physically'),
		(OWNES_VIRTUAL, 'Owns Virtually'),
	)

	owner = models.ForeignKey(
		GamebeaterProfile,
		on_delete=models.CASCADE
	)
	game = models.ForeignKey(
		Game,
		on_delete=models.CASCADE
	)
	platform = models.ForeignKey(
		Platform,
		on_delete=models.CASCADE
	)
	ownership_status = models.CharField(
		max_length=1,
		choices=OWNERSHIP_STATUS_CHOICES,
		default=WANTS
	)
	completion_status = models.CharField(
		max_length=1,
		choices=CompletionStatus.CHOICES,
		default=CompletionStatus.NOT_STARTED
	)
	
	def __unicode__(self):
		return self.owner.user.username + " => " + self.game.title

class Goal(models.Model):
	ownership = models.ForeignKey(GameOwnership)
	
	text = models.CharField(
		max_length=400
	)
	start_time = models.DateTimeField(
		default=None,
		blank=True,
		null=True
	)
	complete_time = models.DateTimeField(
		default=None,
		blank=True,
		null=True
	)
	status = models.CharField(
		max_length=1,
		choices=CompletionStatus.CHOICES,
		default=CompletionStatus.NOT_STARTED
	)

	def __unicode__(self):
		return self.text
		
