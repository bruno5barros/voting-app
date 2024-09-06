import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **kwargs):
        verbosity = options.get("verbosity", 1)
        User = get_user_model()

        # Fetch email and password from environment variables
        superuser_email = os.environ.get('SUPERUSER_EMAIL')
        superuser_password = os.environ.get('SUPERUSER_PASSWORD')
        superuser_username = os.environ.get('SUPERUSER_USERNAME')

        # Validate that the environment variables are set
        if not superuser_email or not superuser_password or not superuser_username:
            self.stdout.write(self.style.ERROR('Superuser email and password must be provided via environment variables.'))
            return

        # Check if the superuser already exists
        if not User.objects.filter(email=superuser_email).exists():
            User.objects.create_superuser(
                username=superuser_username,
                email=superuser_email,
                password=superuser_password
            )
            if verbosity:
                self.stdout.write(self.style.SUCCESS(f'Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser already exists.'))
