from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class GoalText(models.Model):
	GOAL_DEFAULT = 'Complete the game'
	
	text = models.CharField(
		max_length=400,
		primary_key=True
	)
	
	def __unicode__(self):
		return self.text

class ProgressLog(models.Model):
	pub_date = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=400)

	def __unicode__(self):
		return self.text

class Goal(models.Model):
	NOT_STARTED = 'N'
	IN_PROGRESS = 'I'
	COMPLETE = 'C'
	GOAL_STATUS_CHOICES = (
		(NOT_STARTED, 'Not Started'),
		(IN_PROGRESS, 'In Progress'),
		(COMPLETE, 'Complete'),
	)
	
	goal = models.ForeignKey(
		GoalText,
		on_delete=models.CASCADE,
		default=GoalText.GOAL_DEFAULT
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
		choices=GOAL_STATUS_CHOICES,
		default=NOT_STARTED
	)
	progress_logs = models.ManyToManyField(
		ProgressLog,
		blank=True
	)
	# add a slug maybe
	def __unicode__(self):
		return self.goal.text
	