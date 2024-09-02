"""
This module contains filters for querying VotingHistory records.
Includes filters for date ranges and restaurants.
"""

import django_filters
from voting.models.model_voting_history import VotingHistory


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """
    Custom filter for handling 'in' queries on character fields.
    Inherits from BaseInFilter and
    CharFilter to support filtering by multiple values.
    """


class VotingHistoryFilter(django_filters.FilterSet):
    """
    FilterSet for querying VotingHistory records.
    Includes filters for start_date, end_date, and restaurant_id.
    """

    start_date = django_filters.DateFilter(
        field_name="date", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    restaurants = CharInFilter(field_name="restaurant_id", lookup_expr="in")

    class Meta:
        """Define the fields and the model to be used."""

        model = VotingHistory
        fields = ["start_date", "end_date", "restaurant_id"]
