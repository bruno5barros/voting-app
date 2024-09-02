from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from .views import (
    RestaurantViewSet,
    VotingViewSet,
    VotingHistoryViewSet,
    HealthCheckView
)


router = routers.DefaultRouter()
router.register(
    "restaurant",
    RestaurantViewSet,
    basename="restaurant",
)
router.register(
    "voting",
    VotingViewSet,
    basename="voting",
)
router.register(
    "voting-history", VotingHistoryViewSet, basename="voting-history"
)

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
]

urlpatterns += router.urls
