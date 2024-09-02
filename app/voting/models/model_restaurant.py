"""
Model representing a restaurant in the voting system.
"""

from django.db import models


class Restaurant(models.Model):
    """
    Represents a restaurant that users can vote for in the system.
    """

    name = models.CharField(max_length=255)

    objects: models.Manager["Restaurant"] = models.Manager()
