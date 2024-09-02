"""
Model representing the voting process, including the association
between users and restaurants.
"""

from datetime import date
from django.db import models
from django.db.models import Manager
from django.conf import settings
from .model_restaurant import Restaurant


class Voting(models.Model):
    """
    Represents a user's vote for a restaurant on a specific date,
    including the weight of the vote.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    weight = models.FloatField()

    objects: Manager["Voting"] = models.Manager()

    class Meta:
        """Create a composite index to improve query performance."""

        indexes = [models.Index(fields=["user", "restaurant"])]

    @staticmethod
    def count_user_vote_restaurant(user_id: int, restaurant_id: int) -> int:
        """
        Count how many times a user has voted for a particular restaurant.

        Args:
            user_id (int): The ID of the user.
            restaurant_id (int): The ID of the restaurant.

        Returns:
            int: The number of votes the user has cast for the restaurant.
        """
        return Voting.objects.filter(
            user_id=user_id, restaurant_id=restaurant_id
        ).count()
