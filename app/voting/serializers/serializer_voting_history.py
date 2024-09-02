"""
Serializers for handling voting history data and date range validations.
"""

# pylint: disable=W0223

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
from ..models import VotingHistory
from .serializer_restaurant import RestaurantSerializer


class DateRangeSerializer(Serializer):
    """
    Serializer for handling date range inputs and validation for
    filtering voting history.
    """

    start_date = serializers.DateField()
    end_date = serializers.DateField()
    restaurants = serializers.CharField(required=False)

    def validate(self, attrs: dict) -> dict:
        """
        Validate that the start date is before or equal to the end date.

        Args:
            attrs (dict): The attributes to validate.

        Returns:
            dict: The validated attributes.

        Raises:
            ValidationError: If the start date is after the end date.
        """
        if attrs["start_date"] > attrs["end_date"]:
            raise ValidationError(
                "Start date must be before or equal to end date."
            )

        return attrs

    def validate_restaurants(self, value: str) -> list:
        """
        Validate and split the comma-separated restaurant IDs string.

        Args:
            value (str): The comma-separated string of restaurant IDs.

        Returns:
            list: The list of restaurant IDs.

        Raises:
            ValidationError: If the input is not
            a valid comma-separated string.
        """
        try:
            restaurant_ids = list(value.split(","))
        except ValueError as exc:
            raise ValidationError(
                {"restaurants": "Must be a valid comma-separated string."}
            ) from exc

        return restaurant_ids


class VotingHistorySerializer(ModelSerializer):
    """
    Serializer for the VotingHistory model, representing a history
    record of restaurant votes.
    """

    restaurant = RestaurantSerializer()

    class Meta:
        """Define the model, fields to be used."""

        model = VotingHistory
        fields = ["id", "restaurant", "date"]
        read_only_fields = ["id"]
