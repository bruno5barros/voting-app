"""
Model for managing the voting lock state, which controls whether voting
is allowed at a given time.
"""

from django.db import models


class VotingLocker(models.Model):
    """
    Represents the lock state for voting, used to prevent or allow
    voting during specific periods.
    """

    voting_locked = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    objects: models.Manager["VotingLocker"] = models.Manager()

    @staticmethod
    def lock_voting() -> None:
        """
        Lock the voting process to prevent any votes from being cast.
        """
        VotingLocker.objects.update(voting_locked=True)

    @staticmethod
    def unlock_voting() -> None:
        """
        Unlock the voting process to allow votes to be cast.
        """
        VotingLocker.objects.update(voting_locked=False)

    @staticmethod
    def is_voting_locked() -> bool:
        """
        Check if the voting process is currently locked.

        Returns:
            bool: True if voting is locked, False otherwise.
        """
        config = VotingLocker.objects.first()
        return config.voting_locked if config else False
