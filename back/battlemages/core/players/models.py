from django.db import models
from django.contrib.auth.models import User


class Player(User):
    registration_date = models.DateField(auto_now_add=True)
    ranking = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', blank=True)
    gold = models.IntegerField(default=0)
    last_activity = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    player_from = models.ForeignKey(Player, related_name='friend_request_from')
    player_to = models.ForeignKey(Player, related_name='friend_request_to')

    class Meta:
        verbose_name = "FriendRequest"
        verbose_name_plural = "FriendRequests"

    def __str__(self):
        return 'From {0} to {1}'.format(self.player_from.username, self.player_to.username)
