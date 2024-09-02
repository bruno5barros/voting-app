"""
This module contains viewsets for managing Restaurant,
Voting, and VotingHistory models.
It includes:
- RestaurantViewSet for handling CRUD operations on Restaurant records.
- VotingViewSet for handling Voting creation.
- VotingHistoryViewSet for retrieving voting history and
  handling voting history-related API operations.
"""

from typing import Dict
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RestaurantSerializer
from .models.model_restaurant import Restaurant
from .serializers.serializer_voting import VotingSerializer
from .models.model_voting import Voting
from .serializers.serializer_voting_history import (
    DateRangeSerializer,
    VotingHistorySerializer,
)
from .models.model_voting_history import VotingHistory
from .models.model_voting_locker import VotingLocker
from .filters.voting_history import VotingHistoryFilter


class HealthCheckView(APIView):
    """
    A simple health check view that returns a 200 OK response.
    """

    def get(self, request: Request) -> Response:
        """It will return status ok if the API is running."""
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class RestaurantViewSet(ModelViewSet):
    """
    ViewSet for handling CRUD operations on Restaurant records.
    Provides actions for listing, retrieving, creating, updating,
    and deleting restaurant records.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class VotingViewSet(ModelViewSet):
    """
    ViewSet for handling Voting records creation.
    Provides actions for creating and listing voting records.
    Only authenticated users can access these actions.
    """

    http_method_names = ["post", "head", "options"]
    serializer_class = VotingSerializer
    queryset = Voting.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self) -> Dict:
        return {"user": self.request.user}

    def create(
        self, request: Request, *args: list, **kwargs: dict
    ) -> Response:
        """Validate if voting is allowed before creating the vote."""
        if VotingLocker.is_voting_locked():
            return Response(
                {
                    "detail": "Voting is currently locked. \
                    Please try again later."
                },
                status=status.HTTP_423_LOCKED,
            )
        return super().create(request, *args, **kwargs)


class VotingHistoryViewSet(GenericViewSet):
    """
    ViewSet for handling retrieval and listing of VotingHistory records.
    Provides actions for listing voting history based on date ranges and
    handling locked voting scenarios.
    """

    serializer_class = VotingHistorySerializer
    queryset = VotingHistory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = VotingHistoryFilter

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        Handles GET requests for individual voting history records.
        Returns a 405 Method Not Allowed response.
        """
        return Response(
            {"detail": f"Method not allowed. Id: {pk}."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def list(self, request: Request) -> Response:
        """
        Handles GET requests for listing voting history records.
        Returns a 423 Locked response if voting is locked,
        otherwise returns a list of voting history
        records filtered by the provided date range.
        """

        serializer_date = DateRangeSerializer(data=request.query_params)
        serializer_date.is_valid(raise_exception=True)

        queryset = self.filter_queryset(self.queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
