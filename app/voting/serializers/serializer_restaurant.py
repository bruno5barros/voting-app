"""
Serializer for the Restaurant model, handling the representation of
restaurant data.
"""

from rest_framework.serializers import ModelSerializer
from voting.models.model_restaurant import Restaurant


class RestaurantSerializer(ModelSerializer):
    """
    Serializer for the Restaurant model, providing a way to serialize
    restaurant data.
    """

    class Meta:
        """Define the model, fields to be used."""

        model = Restaurant
        fields = ["id", "name"]
        read_only_fields = ["id"]
