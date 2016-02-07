from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from games.models import Game, Platform
from .utils import CompletionStatus, OwnershipStatus, GameOwnershipsByCompletionStatus

class GamebeaterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL
    )
    games = models.ManyToManyField(
        Game,
        through='GameOwnership'
    )

    def get_gameownerships_by_completion(self, completion_status):
        return self.gameownership_set.filter(completion_status=completion_status)

    def get_all_gameownerships_by_completion(self):
        gameownerships_by_completion_status_list = []
        game_total = self.games.count()

        for completion_status in CompletionStatus.CHOICES:
            gameownerships_by_completion_status_list.append(
                GameOwnershipsByCompletionStatus(
                    completion_status=completion_status[1],
                    gameownership_list=self.get_gameownerships_by_completion(completion_status[0]),
                    game_total=game_total
                )
            )
        return tuple(gameownerships_by_completion_status_list)

    def __unicode__(self):
        return self.user.username

class GameOwnership(models.Model):
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
        choices=OwnershipStatus.CHOICES,
        default=OwnershipStatus.WANTS
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
