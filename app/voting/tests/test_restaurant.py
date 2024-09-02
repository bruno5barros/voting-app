"""
Tests for the Restaurant API endpoints.
"""

from typing import Any
import pytest
from model_bakery import baker
from rest_framework import status
from voting.models.model_restaurant import Restaurant
from .conftest import RestaurantTestHelper


@pytest.mark.django_db
class TestRestaurant:
    """
    Test class for verifying the functionality of Restaurant API endpoints.

    This class contains test cases to validate the creation, retrieval,
    updating, and deletion of restaurants via the API. It ensures that
    the API behaves as expected under different scenarios, including
    invalid data and non-existent restaurant IDs.
    """

    def test_get_all_restaurants_returns_200(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """
        Test that GET request to list restaurants
        returns 200 OK and the correct data.
        """
        restaurant_qnt = 3
        restaurants = baker.make(Restaurant, _quantity=restaurant_qnt)

        res: Any = restaurant_test_helper.get_api_client().get(
            restaurant_test_helper.get_url_list()
        )

        assert status.HTTP_200_OK == res.status_code
        assert restaurant_qnt == len(res.data)
        for index, item in enumerate(res.data):
            assert restaurants[index].name == item["name"]

    def test_create_restaurant_return_201(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """
        Test that POST request to create a
        restaurant returns 201 Created.
        """
        res: Any = restaurant_test_helper.get_api_client().post(
            restaurant_test_helper.get_url_list(),
            restaurant_test_helper.get_restaurant_dict(),
        )

        assert status.HTTP_201_CREATED == res.status_code
        assert (
            restaurant_test_helper.get_restaurant_dict()["name"]
            == res.data["name"]
        )

    def test_create_restaurant_return_400(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that POST request with invalid data returns 400 Bad Request."""
        res: Any = restaurant_test_helper.get_api_client().post(
            restaurant_test_helper.get_url_list()
        )

        assert status.HTTP_400_BAD_REQUEST == res.status_code
        assert (
            restaurant_test_helper.get_error_message() == res.data["name"][0]
        )

    def test_patch_restaurant_return_200(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that PATCH request to update a restaurant returns 200 OK."""
        restaurant = baker.make(Restaurant)

        res: Any = restaurant_test_helper.get_api_client().patch(
            restaurant_test_helper.get_url_detail(restaurant.id),
            restaurant_test_helper.get_restaurant_dict(),
        )

        assert status.HTTP_200_OK == res.status_code
        assert (
            restaurant_test_helper.get_restaurant_dict()["name"]
            == res.data["name"]
        )

    def test_patch_restaurant_return_404(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that PATCH request with an invalid ID returns 404 Not Found."""
        baker.make(Restaurant)

        res: Any = restaurant_test_helper.get_api_client().patch(
            restaurant_test_helper.get_url_detail(
                restaurant_test_helper.get_invalid_id()
            )
        )

        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_put_restaurant_return_200(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that PUT request to update a restaurant returns 200 OK."""
        restaurant = baker.make(Restaurant)

        res: Any = restaurant_test_helper.get_api_client().put(
            restaurant_test_helper.get_url_detail(restaurant.id),
            restaurant_test_helper.get_restaurant_dict(),
        )

        assert status.HTTP_200_OK == res.status_code
        assert (
            restaurant_test_helper.get_restaurant_dict()["name"]
            == res.data["name"]
        )

    def test_put_restaurant_return_400(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that PUT request with an invalid ID returns 400 Bad Request."""
        restaurant = baker.make(Restaurant)

        res: Any = restaurant_test_helper.get_api_client().put(
            restaurant_test_helper.get_url_detail(restaurant.id)
        )

        assert status.HTTP_400_BAD_REQUEST == res.status_code
        assert (
            restaurant_test_helper.get_error_message() == res.data["name"][0]
        )

    def test_put_restaurant_return_404(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that PUT request with an invalid ID returns 404 Not Found."""
        res = restaurant_test_helper.get_api_client().put(
            restaurant_test_helper.get_url_detail(
                restaurant_test_helper.get_invalid_id()
            )
        )

        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_get_restaurant_return_200(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that GET request with a valid ID returns 200 Ok."""
        restaurant = baker.make(Restaurant)

        res: Any = restaurant_test_helper.get_api_client().get(
            restaurant_test_helper.get_url_detail(restaurant.id)
        )

        assert status.HTTP_200_OK == res.status_code
        assert restaurant.name == res.data["name"]

    def test_get_restaurant_return_404(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """Test that GET request with an invalid ID returns 404 Not Found."""
        res = restaurant_test_helper.get_api_client().get(
            restaurant_test_helper.get_url_detail(
                restaurant_test_helper.get_invalid_id()
            )
        )

        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_delete_restaurant_return_204(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """
        Test that DELETE request to remove a
        restaurant returns 204 No Content.
        """
        restaurant = baker.make(Restaurant)

        res: Any = restaurant_test_helper.get_api_client().delete(
            restaurant_test_helper.get_url_detail(restaurant.id)
        )

        assert status.HTTP_204_NO_CONTENT == res.status_code

    def test_delete_restaurant_return_404(
        self, restaurant_test_helper: RestaurantTestHelper
    ) -> None:
        """
        Test that DELETE request with an
        invalid ID returns 404 Not Found.
        """
        baker.make(Restaurant)

        res: Any = restaurant_test_helper.get_api_client().delete(
            restaurant_test_helper.get_url_detail(
                restaurant_test_helper.get_invalid_id()
            )
        )

        assert status.HTTP_404_NOT_FOUND == res.status_code
