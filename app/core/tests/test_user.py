"""
The tests include creating a user, retrieving user details, and verifying
the correct functionality of the User model's attributes and methods.
"""

from typing import Any
import pytest
from rest_framework import status
from model_bakery import baker
from ..models import User
from .conftest import UnitTestHelper


@pytest.mark.django_db
class TestUser:
    """
    Test cases for the User model API endpoints.
    This class contains tests for creating a user and retrieving user details.
    """

    def test_create_user_returns_201(
        self, unit_test_helper: UnitTestHelper
    ) -> None:
        """
        Tests that a user can be successfully created via the API
        and that the response returns HTTP 201 status.
        """
        res: Any = unit_test_helper.get_api_client().post(
            unit_test_helper.get_url_list(),
            unit_test_helper.get_user_dict(),
        )

        assert status.HTTP_201_CREATED == res.status_code
        assert User.objects.count() == 1
        for index, value in res.data.items():
            assert value == unit_test_helper.get_user_dict()[index]

    def test_get_user_returns_200(
        self, unit_test_helper: UnitTestHelper
    ) -> None:
        """
        Tests that a user's details can be successfully retrieved via the API
        and that the response returns HTTP 200 status.
        """
        user = baker.make(User)
        unit_test_helper.get_api_client().force_authenticate(user=user)

        res: Any = unit_test_helper.get_api_client().get(
            unit_test_helper.get_url_detail(user.id)
        )

        assert status.HTTP_200_OK == res.status_code
        assert user.max_vote_daily == res.data["max_vote_daily"]
        assert user.number_vote == res.data["number_vote"]
