import os
from typing import List, Dict, Any
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args: List[Any], **options: Dict[str, Any]) -> None:
        verbosity = options.get("verbosity", 1)
        user = get_user_model()

        # Fetch email and password from environment variables
        email = os.environ.get('SUPERUSER_EMAIL')
        password = os.environ.get('SUPERUSER_PASSWORD')
        username = os.environ.get('SUPERUSER_USERNAME')
        is_staff = bool(os.environ.get('SUPERUSER_IS_STAFF'))
        is_admin = bool(os.environ.get('SUPERUSER_IS_SUPER_USER'))

        # Validate that the environment variables are set
        if not superuser_email or not superuser_password or not superuser_username:
            self.stdout.write(self.style.ERROR('Superuser email and password must be provided via environment variables.'))
            return

        # Check if the superuser already exists
        if not user.objects.filter(email=superuser_email).exists():
            user.objects.create_superuser(
                username=username,
                email=email,
                is_staff=is_staff,
                is_admin=is_admin,
                password=password
            )
            if verbosity:
                self.stdout.write(self.style.SUCCESS(f'Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser already exists.'))
