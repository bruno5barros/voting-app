from typing import List, Dict, Any
from django.core.management.base import BaseCommand
from voting.models import VotingLocker


class Command(BaseCommand):
    """Ensure that our voting locker is created."""

    help = "Set up the voting locker if it does not already exist."

    def handle(self, *args: List[Any], **options: Dict[str, Any]) -> None:
        verbosity = options.get("verbosity", 1)

        if not VotingLocker.objects.exists():
            VotingLocker.objects.create()

        if verbosity:
            self.stdout.write(
                self.style.SUCCESS("Voting locker set up successfully.")
            )
