"""Tests for voting-related API endpoints."""

from typing import Any
from datetime import date
import pytest
from model_bakery import baker
from django.conf import settings
from rest_framework import status
from voting.models import Restaurant, Voting
from voting.utils.voting import reset_daily_votes
from core.models import User
from .utils.voting_helper_class import VotingTestHelper


@pytest.mark.django_db
class TestVote:
    """Tests for voting functionality including creation and restrictions."""

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

    def test_list_voting_returns_405(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that GET requests to the voting list endpoint
        return 405 Method Not Allowed.
        """
        res: Any = test_helper.get_api_client().get(
            test_helper.get_voting_url_list()
        )
        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_get_voting_returns_405(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that GET requests to the voting detail endpoint
        return 405 Method Not Allowed.
        """
        res: Any = test_helper.get_api_client().get(
            test_helper.get_voting_url_detail(1)
        )
        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_put_voting_returns_405(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that PUT requests to the voting detail endpoint
        return 405 Method Not Allowed.
        """
        res: Any = test_helper.get_api_client().put(
            test_helper.get_voting_url_detail(1),
            test_helper.get_voting_dict(),
        )
        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_patch_voting_returns_405(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that PATCH requests to the voting detail endpoint
        return 405 Method Not Allowed.
        """
        res: Any = test_helper.get_api_client().patch(
            test_helper.get_voting_url_detail(1),
            test_helper.get_voting_dict(),
        )
        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_delete_voting_returns_405(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that DELETE requests to the voting detail endpoint
        return 405 Method Not Allowed.
        """
        res: Any = test_helper.get_api_client().delete(
            test_helper.get_voting_url_detail(1),
            test_helper.get_voting_dict(),
        )
        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_create_voting_returns_400(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that POST requests to the voting list endpoint
        with missing data return 400 Bad Request.
        """
        res: Any = test_helper.get_api_client().post(
            test_helper.get_voting_url_list(),
            {},
        )
        assert status.HTTP_400_BAD_REQUEST == res.status_code
        assert res.data["restaurant_id"][0] == test_helper.get_error_message()

    def test_create_voting_returns_201(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that POST requests to the voting list endpoint
        with valid data return 201 Created.
        """
        number_inserted_vote = 1
        res: Any = test_helper.get_api_client().post(
            test_helper.get_voting_url_list(),
            test_helper.get_voting_dict(),
        )
        assert status.HTTP_201_CREATED == res.status_code
        assert res.data["restaurant"]["id"] == self.restaurant.id
        assert res.data["user"]["id"] == self.user.id
        assert res.data["weight"] == test_helper.get_vote_weight(
            "vote_weight_1"
        )
        assert res.data["date"] == date.today().strftime("%Y-%m-%d")
        self.user.refresh_from_db()
        assert self.user.number_vote == number_inserted_vote

    def test_create_2_voting_returns_201(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that posting two votes returns 201 Created
        and updates the number of votes.
        """
        number_inserted_vote = 2
        for _ in range(2):
            res: Any = test_helper.get_api_client().post(
                test_helper.get_voting_url_list(),
                test_helper.get_voting_dict(),
            )
        assert status.HTTP_201_CREATED == res.status_code
        assert res.data["restaurant"]["id"] == self.restaurant.id
        assert res.data["user"]["id"] == self.user.id
        assert res.data["weight"] == test_helper.get_vote_weight(
            "vote_weight_2"
        )
        assert res.data["date"] == date.today().strftime("%Y-%m-%d")
        self.user.refresh_from_db()
        assert self.user.number_vote == number_inserted_vote

    def test_create_3_voting_returns_201(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that posting three votes returns 201 Created
        and updates the number of votes.
        """
        number_inserted_vote = 3
        for _ in range(3):
            res: Any = test_helper.get_api_client().post(
                test_helper.get_voting_url_list(),
                test_helper.get_voting_dict(),
            )
        assert status.HTTP_201_CREATED == res.status_code
        assert res.data["restaurant"]["id"] == self.restaurant.id
        assert res.data["user"]["id"] == self.user.id
        assert res.data["weight"] == test_helper.get_vote_weight(
            "vote_weight_3"
        )
        assert res.data["date"] == date.today().strftime("%Y-%m-%d")
        self.user.refresh_from_db()
        assert self.user.number_vote == number_inserted_vote

    def test_create_4_voting_returns_201(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that posting four votes returns 201 Created
        and updates the number of votes.
        """
        number_inserted_vote = 4
        for _ in range(4):
            res: Any = test_helper.get_api_client().post(
                test_helper.get_voting_url_list(),
                test_helper.get_voting_dict(),
            )
        assert status.HTTP_201_CREATED == res.status_code
        assert res.data["restaurant"]["id"] == self.restaurant.id
        assert res.data["user"]["id"] == self.user.id
        assert res.data["weight"] == test_helper.get_vote_weight(
            "vote_weight_4"
        )
        assert res.data["date"] == date.today().strftime("%Y-%m-%d")
        self.user.refresh_from_db()
        assert self.user.number_vote == number_inserted_vote

    def test_create_5_voting_returns_400(
        self, test_helper: VotingTestHelper
    ) -> None:
        """
        Test that posting five votes returns 400 Bad Request
        due to voting limit exceeded.
        """
        for _ in range(5):
            res: Any = test_helper.get_api_client().post(
                test_helper.get_voting_url_list(),
                test_helper.get_voting_dict(),
            )
        assert status.HTTP_400_BAD_REQUEST == res.status_code
        assert "Voting limit exceeded." == res.data["number_vote"][0]

    def test_reset_daily_votes_returns_200(
        self, test_helper: VotingTestHelper
    ) -> None:
        """Test that resetting daily votes works and clears the votes."""
        number_inserted_vote = 0
        number_voting = 0
        for _ in range(5):
            test_helper.get_api_client().post(
                test_helper.get_voting_url_list(),
                test_helper.get_voting_dict(),
            )
        self.user.refresh_from_db()
        assert (
            Voting.objects.filter(
                user=self.user, restaurant=self.restaurant
            ).count()
            == self.user.number_vote
        )

        reset_daily_votes()

        self.user.refresh_from_db()
        assert self.user.number_vote == number_inserted_vote
        number_votes = Voting.objects.all().count()
        assert number_votes == number_voting
