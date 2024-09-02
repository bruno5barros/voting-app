"""Tests for anonymous voting access."""

import pytest
from rest_framework import status
from .utils.voting_helper_class import VotingTestHelper


@pytest.mark.django_db
class TestAnonymousVoting:
    """Tests for voting access by unauthenticated users."""

    def test_create_voting_returns_401(
        self, voting_test_helper: VotingTestHelper
    ) -> None:
        """
        Test that anonymous users receive 401 Unauthorized
        for POST requests to create voting.
        """
        res = voting_test_helper.get_api_client().post(
            voting_test_helper.get_voting_url_list(),
            voting_test_helper.get_voting_dict(),
        )
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_list_voting_returns_401(
        self, voting_test_helper: VotingTestHelper
    ) -> None:
        """
        Test that anonymous users receive 401 Unauthorized
        for GET requests to list voting.
        """
        res = voting_test_helper.get_api_client().get(
            voting_test_helper.get_voting_url_list()
        )
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_get_voting_returns_401(
        self, voting_test_helper: VotingTestHelper
    ) -> None:
        """
        Test that anonymous users receive 401 Unauthorized
        for GET requests to retrieve voting.
        """
        res = voting_test_helper.get_api_client().get(
            voting_test_helper.get_voting_url_detail(1)
        )
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_put_voting_returns_401(
        self, voting_test_helper: VotingTestHelper
    ) -> None:
        """
        Test that anonymous users receive 401 Unauthorized
        for PUT requests to update voting.
        """
        res = voting_test_helper.get_api_client().put(
            voting_test_helper.get_voting_url_detail(1),
            voting_test_helper.get_voting_dict(),
        )
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_patch_voting_returns_401(
        self, voting_test_helper: VotingTestHelper
    ) -> None:
        """
        Test that anonymous users receive 401 Unauthorized
        for PATCH requests to update voting.
        """
        res = voting_test_helper.get_api_client().patch(
            voting_test_helper.get_voting_url_detail(1),
            voting_test_helper.get_voting_dict(),
        )

        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_delete_voting_returns_401(
        self, voting_test_helper: VotingTestHelper
    ) -> None:
        """
        Test that anonymous users receive 401 Unauthorized
        for DELETE requests to delete voting.
        """
        res = voting_test_helper.get_api_client().delete(
            voting_test_helper.get_voting_url_detail(1)
        )

        assert status.HTTP_401_UNAUTHORIZED == res.status_code
