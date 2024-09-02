"""Tests for voting-related API endpoints."""

from typing import Any
from datetime import date, timedelta
import pytest
from model_bakery import baker
from django.conf import settings
from rest_framework import status
from voting.models import Restaurant
from voting.models import VotingLocker
from voting.models import Voting
from voting.tasks import calculate_daily_winner, unlock_voting_task
from core.models import User
from .utils.voting_helper_class import VotingTestHelper


@pytest.mark.django_db
class TestVote:
    """Tests for voting locker functionality."""

    @pytest.fixture()
    def test_helper(
        self, voting_test_helper: VotingTestHelper
    ) -> VotingTestHelper:
        """
        Fixture for setting up a test user,
        restaurant, and voting test helper.
        """
        self.user: User = baker.make(
            settings.AUTH_USER_MODEL, max_vote_daily=4
        )
        self.restaurant: Restaurant = baker.make(Restaurant)
        voting_test_helper.set_user(self.user)
        voting_test_helper.set_restaurant_id(self.restaurant.id)
        voting_test_helper.get_authenticated_api_client(self.user)

        return voting_test_helper

    def test_lock_voting_returns_423(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that POST requests to voting endpoint
        with valid data return 423 blocked because voting is blocked.
        """
        number_inserted_vote = 0
        baker.make(VotingLocker)
        VotingLocker.lock_voting()

        res: Any = test_helper.get_api_client().post(
            test_helper.get_voting_url_list(),
            test_helper.get_voting_dict(),
        )

        assert status.HTTP_423_LOCKED == res.status_code
        assert self.user.number_vote == number_inserted_vote

    def test_unlock_voting_returns_201(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that POST requests to voting endpoint
        with valid data return 201 Created.
        """
        number_inserted_vote = 1
        baker.make(VotingLocker)
        VotingLocker.lock_voting()
        unlock_voting_task()

        res: Any = test_helper.get_api_client().post(
            test_helper.get_voting_url_list(),
            test_helper.get_voting_dict(),
        )

        assert status.HTTP_201_CREATED == res.status_code
        assert self.user.number_vote == number_inserted_vote

    def test_lock_voting_multiple_dates_returns_403(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that POST requests to the voting endpoint with valid data
        return 423 blocked because of multiple dates in the voting table.
        """
        number_inserted_vote = 0
        baker.make(VotingLocker)
        baker.make(Voting, date=date.today())
        baker.make(Voting, date=date.today() - timedelta(days=1))

        calculate_daily_winner()
        assert VotingLocker.is_voting_locked()

        unlock_voting_task()
        assert VotingLocker.is_voting_locked()

        res: Any = test_helper.get_api_client().post(
            test_helper.get_voting_url_list(),
            test_helper.get_voting_dict(),
        )

        assert status.HTTP_423_LOCKED == res.status_code
        assert self.user.number_vote == number_inserted_vote
