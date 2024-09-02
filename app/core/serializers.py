"""
This module defines serializers for the User model, extending the
default serializers provided by the
Djoser library to include additional fields.
"""

from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for creating a new User. Extends the default Djoser serializer
    to include additional fields like 'max_vote_daily'.
    """

    class Meta(BaseUserCreateSerializer.Meta):
        """
        Meta class to define the fields that
        will be included in the serialized output.
        """

        fields = [
            "username",
            "password",
            "email",
            "max_vote_daily",
        ]


class UserSerializer(BaseUserSerializer):
    """
    Serializer for the User model. Extends the default Djoser serializer
    to include additional fields like 'max_vote_daily' and 'number_vote'.
    """

    class Meta(BaseUserSerializer.Meta):
        """
        Meta class to define the fields that
        will be included in the serialized output.
        """

        fields = [
            "id",
            "username",
            "email",
            "max_vote_daily",
            "number_vote",
        ]
