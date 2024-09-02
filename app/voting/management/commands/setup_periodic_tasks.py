from typing import List, Dict, Any
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule


class Command(BaseCommand):
    """Make sure that our periodic task is created"""

    help = "Set up periodic tasks after migrations."

    def handle(self, *args: List[Any], **options: Dict[str, Any]) -> None:
        task_name = "Every day periodic task"
        verbosity = options.get("verbosity", 1)

        if not PeriodicTask.objects.filter(name=task_name).exists():
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute="0",
                hour="23",
                day_of_month="*",
                month_of_year="*",
                day_of_week="*",
            )

            PeriodicTask.objects.create(
                crontab=schedule,
                name=task_name,
                task="voting.tasks.calculate_daily_winner",
            )

        task_name = "Unlock voting at 12AM"
        if not PeriodicTask.objects.filter(name=task_name).exists():
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute="0",
                hour="0",
                day_of_month="*",
                month_of_year="*",
                day_of_week="*",
            )
            PeriodicTask.objects.create(
                crontab=schedule,
                name=task_name,
                task="voting.tasks.unlock_voting_task",
            )

        if verbosity:
            self.stdout.write(
                self.style.SUCCESS("Periodic tasks set up successfully.")
            )
