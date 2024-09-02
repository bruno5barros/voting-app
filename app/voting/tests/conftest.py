"""Fixture configuration for voting tests."""

import pytest
from .utils.restaurant_helper_class import RestaurantTestHelper
from .utils.voting_helper_class import VotingTestHelper
from .utils.voting_history_helper_class import VotingHistoryTestHelper


@pytest.fixture
def voting_test_helper() -> VotingTestHelper:
    """Fixture for providing a VotingTestHelper instance."""
    return VotingTestHelper()


@pytest.fixture
def restaurant_test_helper() -> RestaurantTestHelper:
    """Fixture for providing a RestaurantTestHelper instance."""
    return RestaurantTestHelper()


@pytest.fixture
def voting_history_test_helper() -> VotingHistoryTestHelper:
    """Fixture for providing a VotingHistoryTestHelper instance."""
    return VotingHistoryTestHelper()
