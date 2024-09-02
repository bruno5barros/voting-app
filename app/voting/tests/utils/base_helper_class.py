from rest_framework.test import APIClient
from django.contrib.auth.models import User


class BaseTestHelper:
    def __init__(self) -> None:
        self.__api_client = APIClient()
        self.__invalid_id = -5
        self.__error_message = "This field is required."

    def get_api_client(self) -> APIClient:
        return self.__api_client

    def get_authenticated_api_client(self, user: User) -> APIClient:
        self.__api_client.force_authenticate(user=user)
        return self.__api_client

    def get_invalid_id(self) -> int:
        return self.__invalid_id

    def get_error_message(self) -> str:
        return self.__error_message
