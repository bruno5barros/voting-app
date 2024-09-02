"""
This module contains tests for the VotingHistory API endpoint.
Includes tests for GET requests,
handling of missing date parameters, and correct responses
for different date ranges and scenarios.
"""

from datetime import date, timedelta
from typing import Any
import pytest
from model_bakery import baker
from rest_framework import status
from voting.models.model_voting_history import VotingHistory
from .conftest import VotingHistoryTestHelper


@pytest.mark.django_db
class TestVotingHistory:
    """
    Test suite for the VotingHistory API endpoint.

    Includes tests for various HTTP methods and
    date range queries to ensure correct
    responses and handling of errors and edge cases.
    """

    def test_get_history_voting_returns_405(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that GET requests to a voting history detail endpoint
        return a 405 Method Not Allowed response.
        Uses the VotingHistoryTestHelper to perform
        the API call and check the response status.
        """
        res: Any = voting_history_test_helper.get_api_client().get(
            voting_history_test_helper.get_voting_history_url_detail(1)
        )

        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_create_history_voting_returns_405(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that POST requests to the voting history list endpoint
        return a 405 Method Not Allowed response.
        Uses the VotingHistoryTestHelper to perform
        the API call and check the response status.
        """
        res: Any = voting_history_test_helper.get_api_client().post(
            voting_history_test_helper.get_voting_history_url_list()
        )

        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_put_history_voting_returns_405(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that PUT requests to a voting history detail endpoint
        return a 405 Method Not Allowed response.
        Uses the VotingHistoryTestHelper to perform
        the API call and check the response status.
        """
        res: Any = voting_history_test_helper.get_api_client().put(
            voting_history_test_helper.get_voting_history_url_detail(1)
        )

        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_patch_history_voting_returns_405(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that PATCH requests to a voting history detail endpoint
        return a 405 Method Not Allowed response.
        Uses the VotingHistoryTestHelper to perform
        the API call and check the response status.
        """
        res: Any = voting_history_test_helper.get_api_client().patch(
            voting_history_test_helper.get_voting_history_url_detail(1)
        )

        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_delete_history_voting_returns_405(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that DELETE requests to a voting history detail
        endpoint return a 405 Method Not Allowed response.
        Uses the VotingHistoryTestHelper to perform
        the API call and check the response status.
        """
        res: Any = voting_history_test_helper.get_api_client().delete(
            voting_history_test_helper.get_voting_history_url_detail(1)
        )

        assert status.HTTP_405_METHOD_NOT_ALLOWED == res.status_code

    def test_list_history_voting_no_end_date_400(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that GET requests to the voting history list endpoint
        with missing end_date return a 400 Bad Request response.
        Uses the VotingHistoryTestHelper to perform
        the API call and check the response status and error message.
        """
        res: Any = voting_history_test_helper.get_api_client().get(
            voting_history_test_helper.get_voting_history_url_list(),
            {"start_date": voting_history_test_helper.get_start_date()},
        )

        assert status.HTTP_400_BAD_REQUEST == res.status_code
        assert (
            voting_history_test_helper.get_error_message()
            == res.data["end_date"][0]
        )

    def test_list_history_voting_no_start_date_400(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that GET requests to the voting history list endpoint
        with missing start_date return a 400 Bad Request response.
        Uses the VotingHistoryTestHelper to perform the API call and
        check the response status and error message.
        """
        res: Any = voting_history_test_helper.get_api_client().get(
            voting_history_test_helper.get_voting_history_url_list(),
            {"end_date": voting_history_test_helper.get_end_date()},
        )

        assert status.HTTP_400_BAD_REQUEST == res.status_code
        assert (
            voting_history_test_helper.get_error_message()
            == res.data["start_date"][0]
        )

    def test_list_history_voting_returns_200(
        self, voting_history_test_helper: VotingHistoryTestHelper
    ) -> None:
        """
        Tests that GET requests to the voting history list endpoint
        with valid date ranges return a 200 OK response.
        Verifies that the response data matches the expected voting
        history records within the given date range.
        """
        today = date.today()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        tomorrow = today + timedelta(days=1)
        two_days_forward = today + timedelta(days=2)
        today_winner: VotingHistory = baker.make(VotingHistory, date=today)
        yesterday_winner: VotingHistory = baker.make(
            VotingHistory, date=yesterday
        )
        baker.make(VotingHistory, date=two_days_ago)
        tomorrow_winner: VotingHistory = baker.make(
            VotingHistory, date=tomorrow
        )
        baker.make(VotingHistory, date=two_days_forward)
        winners_history = {
            today_winner.id: today_winner,
            yesterday_winner.id: yesterday_winner,
            tomorrow_winner.id: tomorrow_winner,
        }

        res: Any = voting_history_test_helper.get_api_client().get(
            voting_history_test_helper.get_voting_history_url_list(),
            {
                "start_date": yesterday.strftime("%Y-%m-%d"),
                "end_date": tomorrow.strftime("%Y-%m-%d"),
            },
        )

        assert status.HTTP_200_OK == res.status_code
        assert len(res.data) == len(winners_history)
        for winner in res.data:
            expected_response = winners_history[winner["id"]]
            for key, value in winner.items():
                expected_value = getattr(expected_response, key)
                if key == "restaurant":
                    assert value["id"] == expected_value.id
                elif isinstance(expected_value, date):
                    assert value == expected_value.strftime("%Y-%m-%d")
                else:
                    assert value == expected_value
