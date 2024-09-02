"""
This module contains Celery tasks for handling voting-related operations.
Tasks include calculating the daily voting winner and unlocking voting.
"""

import logging
from django.db import transaction, DatabaseError
from django.db.models import Count, Sum
from celery import shared_task
from voting.models.model_voting import Voting
from voting.models.model_voting_history import VotingHistory
from .utils.voting import reset_daily_votes
from .models.model_voting_locker import VotingLocker


logger = logging.getLogger(__name__)


@shared_task(max_retries=6, default_retry_delay=1800)
def calculate_daily_winner() -> None:
    """
    Calculates the daily winner of the voting process and
    records it in the VotingHistory model.
    If a winner is found, resets daily votes.
    Locks the voting during the calculation process.
    This task is executed by Celery and
    can be retried up to 6 times with a 30-minute delay between retries.
    """
    VotingLocker.lock_voting()
    votes_dates = (
        Voting.objects.values_list("date", flat=True).distinct().count()
    )
    if votes_dates == 1:
        try:
            with transaction.atomic():
                winner = (
                    Voting.objects.values("restaurant", "date")
                    .annotate(
                        total_weight=Sum("weight"),
                        distinct_users=Count("user", distinct=True),
                    )
                    .order_by("-total_weight", "-distinct_users")
                    .values("restaurant", "date")
                    .first()
                )
                if winner is not None:
                    VotingHistory.objects.create(
                        restaurant_id=winner["restaurant"],
                        date=winner["date"],
                    )
                    reset_daily_votes()
                else:
                    logger.info("Database is empty.")
        except DatabaseError:
            logger.error("Database error, please check your db connection.")
    else:
        logger.error("Multiple voting dates in the db. Emailing dev.")


@shared_task(max_retries=6, default_retry_delay=1800)
def unlock_voting_task() -> None:
    """
    Unlocks the voting process if there are
    any voting records present in the database.
    This task is executed by Celery and can be retried
    up to 6 times with a 30-minute delay between retries.
    """
    if Voting.objects.count() == 0:
        VotingLocker.unlock_voting()
        logger.info("Successfully unlocked the locker.")
    else:
        logger.error("Couldn't unlock the locker. Emailing dev.")
