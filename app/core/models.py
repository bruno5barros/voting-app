"""
This module defines the User model, which extends the AbstractUser model
to include additional fields and methods for voting functionality.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model that extends the default Django AbstractUser model.
    Adds additional fields to manage voting limits and track votes.
    """

    email = models.EmailField(unique=True)
    max_vote_daily = models.PositiveSmallIntegerField(default=5)
    number_vote = models.PositiveSmallIntegerField(default=0)

    def increment_1_number_vote(self) -> None:
        """
        Increments the user's vote count by one and
        saves the updated count to the database.
        """
        self.number_vote += 1
        self.save()

    @staticmethod
    def reset_number_vote() -> None:
        """
        Resets the number of votes for all users to zero.
        This method is typically called at the beginning of a new voting day.
        """
        User.objects.update(number_vote=0)
