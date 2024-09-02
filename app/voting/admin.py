"""
This module registers Voting and
VotingHistory models with the Django admin site.
It provides a basic admin interface
for managing voting and voting history records.
"""

from django.contrib import admin
from .models.model_voting import Voting
from .models.model_voting_history import VotingHistory
from .models import VotingLocker


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Voting records.
    This class provides a basic configuration for
    the Voting model in the Django admin site.
    """

    list_display = ["id"]


@admin.register(VotingHistory)
class VotingHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing VotingHistory records.
    This class provides a basic configuration for
    the VotingHistory model in the Django admin site.
    """

    list_display = ["id"]


@admin.register(VotingLocker)
class VotingLockerAdmin(admin.ModelAdmin):
    """
    Admin interface for managing VotingLocker records.
    This class provides a basic configuration for
    the VotingLocker model in the Django admin site.
    """

    list_display = ["id"]
