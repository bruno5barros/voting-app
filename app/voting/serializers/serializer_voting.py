"""
Serializers for handling voting-related data, including creating and
validating votes.
"""

from typing import Dict
from django.db import transaction, IntegrityError, DatabaseError
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from core.serializers import BaseUserSerializer
from voting.serializers.serializer_restaurant import RestaurantSerializer
from ..models.model_voting import Voting
from ..utils.voting import calculate_weight


class VotingSerializer(ModelSerializer):
    """
    Serializer for the Voting model, handling the creation and
    validation of voting data.
    """

    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.IntegerField(write_only=True)
    user = BaseUserSerializer(read_only=True)

    class Meta:
        """Define the model, fields to be used."""

        model = Voting
        fields = [
            "id",
            "user",
            "restaurant",
            "restaurant_id",
            "date",
            "weight",
        ]
        read_only_fields = ["id", "user", "date", "weight"]

    def validate(self, attrs: Dict) -> Dict:
        """
        Validate the vote, ensuring the user has not exceeded their
        daily voting limit.

        Args:
            attrs (Dict): The attributes to validate.

        Returns:
            Dict: The validated attributes.

        Raises:
            ValidationError: If the user has exceeded the voting limit.
        """
        user = self.context["user"]
        if user.max_vote_daily == user.number_vote:
            raise ValidationError({"number_vote": "Voting limit exceeded."})

        return attrs

    def update_validated_data(self, validated_data: Dict) -> None:
        """
        Update the validated data with the user ID and calculate the
        vote weight.

        Args:
            validated_data (Dict): The validated data to update.
        """
        user_id = self.context["user"].id
        validated_data["user_id"] = user_id
        validated_data["weight"] = calculate_weight(
            user_id, validated_data["restaurant_id"]
        )

    def create(self, validated_data: Dict) -> Voting:
        """
        Create a new vote record.

        Args:
            validated_data (Dict): The validated data to create the vote.

        Returns:
            Voting: The created voting record.

        Raises:
            ValidationError: If an integrity or database error occurs.
        """
        self.update_validated_data(validated_data)
        try:
            with transaction.atomic():
                self.context["user"].increment_1_number_vote()
                return Voting.objects.create(**validated_data)
        except IntegrityError as exc:
            raise serializers.ValidationError(
                "Integrity error occurred"
            ) from exc
        except DatabaseError as db_exc:
            raise serializers.ValidationError(
                "Database error occurred"
            ) from db_exc
