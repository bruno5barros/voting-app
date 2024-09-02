"""Define all the models we need to show in the admin panel"""

from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the User model.
    This admin interface displays the id and
    email of the user in the list view.
    """

    list_display = ["id", "email"]
