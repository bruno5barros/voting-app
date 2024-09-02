"""
Utilities for managing the voting system, including weight calculation
and daily vote reset functionality.
"""

import logging
from voting.models.model_voting import Voting
from core.models import User

logger = logging.getLogger(__name__)


def calculate_weight(user_id: int, restaurant_id: int) -> float:
    """
    Calculate the weight of a user's vote for a given restaurant.

    Args:
        user_id (int): The ID of the user.
        restaurant_id (int): The ID of the restaurant.

    Returns:
        float: The weight of the vote based on previous votes.
    """
    vote_quantity = Voting.count_user_vote_restaurant(user_id, restaurant_id)
    return 1 if vote_quantity == 0 else (0.5 if vote_quantity == 1 else 0.25)


def reset_daily_votes() -> None:
    """
    Reset the daily votes by clearing all existing votes and resetting
    the number of votes each user has cast.
    """
    User.reset_number_vote()
    Voting.objects.all().delete()
