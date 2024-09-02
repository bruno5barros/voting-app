"""
Tests for the winner calculation logic in the voting system.
"""

from datetime import date
import pytest
from model_bakery import baker
from voting.models import VotingHistory, Voting, Restaurant
from voting.tasks import calculate_daily_winner
from core.models import User


@pytest.mark.django_db
class TestVotingWinnerCalculation:
    """Tests related to the calculate_daily_winner task."""

    def test_calculate_daily_winner(self) -> None:
        """
        Test that the correct restaurant is
        chosen as the winner based on votes.
        """
        user1 = baker.make(User)
        user2 = baker.make(User)
        restaurant1 = baker.make(Restaurant)
        restaurant2 = baker.make(Restaurant)

        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user1,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user2,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user2,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user2,
            weight=0.5,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user2,
            weight=0.25,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user2,
            weight=0.25,
            date=date.today(),
        )

        calculate_daily_winner()
        winner = VotingHistory.objects.all().first()

        assert winner is not None
        assert winner.restaurant.id == restaurant1.id
        assert winner.date == date.today()
        assert Voting.objects.all().count() == 0

    def test_no_votes(self) -> None:
        """Test that no winner is selected when there are no votes."""
        calculate_daily_winner()

        winner = VotingHistory.objects.all().first()
        assert winner is None
        assert Voting.objects.all().count() == 0

    def test_multiple_restaurants_and_users(self) -> None:
        """
        Test that the correct restaurant is chosen when there are
        multiple votes for different restaurants and users.
        """
        user1 = baker.make(User)
        user2 = baker.make(User)
        user3 = baker.make(User)
        restaurant1 = baker.make(Restaurant)
        restaurant2 = baker.make(Restaurant)

        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user1,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user2,
            weight=0.5,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user3,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user3,
            weight=0.5,
            date=date.today(),
        )

        calculate_daily_winner()
        winner = VotingHistory.objects.all().first()

        assert winner is not None
        assert winner.restaurant.id == restaurant1.id
        assert winner.date == date.today()
        assert Voting.objects.all().count() == 0

    def test_all_votes_to_one_restaurant(self) -> None:
        """
        Test that when all votes go to one restaurant,
        it is selected as the winner.
        """
        user1 = baker.make(User)
        user2 = baker.make(User)
        restaurant1 = baker.make(Restaurant)

        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user1,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user2,
            weight=1.0,
            date=date.today(),
        )

        calculate_daily_winner()
        winner = VotingHistory.objects.all().first()

        assert winner is not None
        assert winner.restaurant.id == restaurant1.id
        assert winner.date == date.today()
        assert Voting.objects.all().count() == 0

    def test_all_votes_to_multiple_restaurants(self) -> None:
        """
        Test that the restaurant with the highest total
        vote weight is selected.
        """
        user1 = baker.make(User)
        user2 = baker.make(User)
        user3 = baker.make(User)
        restaurant1 = baker.make(Restaurant)
        restaurant2 = baker.make(Restaurant)
        restaurant3 = baker.make(Restaurant)

        baker.make(
            Voting,
            restaurant=restaurant3,
            user=user1,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant3,
            user=user2,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant3,
            user=user3,
            weight=1.0,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user2,
            weight=0.5,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user1,
            weight=0.5,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant2,
            user=user3,
            weight=0.5,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user2,
            weight=0.25,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user1,
            weight=0.25,
            date=date.today(),
        )
        baker.make(
            Voting,
            restaurant=restaurant1,
            user=user3,
            weight=0.25,
            date=date.today(),
        )

        calculate_daily_winner()
        winner = VotingHistory.objects.all().first()

        assert winner is not None
        assert winner.restaurant.id == restaurant3.id
        assert winner.date == date.today()
        assert Voting.objects.all().count() == 0
