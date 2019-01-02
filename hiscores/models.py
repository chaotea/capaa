import datetime
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)
    rank = models.CharField(max_length=200)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
