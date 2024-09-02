from typing import Dict
from django.urls import reverse
from .base_helper_class import BaseTestHelper


class RestaurantTestHelper(BaseTestHelper):
    def __init__(
        self,
        name: str = "Restaurant test",
    ):
        super().__init__()
        self.__restaurant_dict: Dict = {
            "name": name,
        }

    def get_restaurant_dict(self) -> Dict:
        return self.__restaurant_dict

    def get_url_list(self) -> str:
        return reverse("restaurant-list")

    def get_url_detail(self, restaurant_id: int) -> str:
        return reverse("restaurant-detail", args=[restaurant_id])
