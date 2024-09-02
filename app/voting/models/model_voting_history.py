"""
Model representing the voting history, which tracks the winning
restaurant each day.
"""

from datetime import date
from django.db import models
from .model_restaurant import Restaurant


class VotingHistory(models.Model):
    """
    Represents a record of the daily voting history, storing which
    restaurant won on a particular date.
    """

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    objects: models.Manager["VotingHistory"] = models.Manager()
