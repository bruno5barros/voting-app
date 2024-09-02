"""
A helper class to facilitate unit testing of
the User model and related API endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


class UnitTestHelper:
    """
    UnitTestHelper provides methods to:
    - Initialize test data for a user with default or custom values.
    - Retrieve an instance of APIClient for making API calls.
    - Generate URLs for user-related API endpoints.
    - Provide user data in dictionary form for testing purposes.
    """

    def __init__(
        self,
        username: str = "test",
        password: str = "pass_test",
        email: str = "test@gmail.com",
        max_vote_daily: int = 5,
        number_vote: int = 0,
    ):
        self.__api_client = APIClient()
        self.__user_dict = {
            "username": username,
            "password": password,
            "email": email,
            "max_vote_daily": max_vote_daily,
            "number_vote": number_vote,
        }

    def get_api_client(self) -> APIClient:
        """Get the the api client instance to call http methods."""
        return self.__api_client

    def get_user_dict(self) -> dict:
        """Get the user dict to create new user."""
        return self.__user_dict

    def get_url_list(self) -> str:
        """Get the path to create or list users."""
        return reverse("user-list")

    def get_url_detail(self, user_id: int) -> str:
        """Get the path to get, put, patch and delete users."""
        return reverse("user-detail", args=[user_id])


@pytest.fixture
def unit_test_helper() -> UnitTestHelper:
    """Create and return an instance of the helper class to the test class."""
    return UnitTestHelper()
