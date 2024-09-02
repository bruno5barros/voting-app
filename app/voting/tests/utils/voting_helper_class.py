from typing import Dict
from django.urls import reverse
from .base_helper_class import BaseTestHelper
from core.models import User


class VotingTestHelper(BaseTestHelper):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.__voting_dict: Dict[str, int] = {}
        self.__vote_weight: Dict[str, float] = {
            "vote_weight_1": 1.0,
            "vote_weight_2": 0.5,
            "vote_weight_3": 0.25,
            "vote_weight_4": 0.25,
        }
        self.__user: User | None = None

    def get_voting_dict(self) -> Dict:
        return self.__voting_dict

    def set_restaurant_id(self, restaurant_id: int) -> None:
        self.__voting_dict["restaurant_id"] = restaurant_id

    def get_voting_url_list(self) -> str:
        return reverse("voting-list")

    def get_voting_url_detail(self, voting_id: int) -> str:
        return reverse("voting-detail", args=[voting_id])

    def get_vote_weight(self, key: str) -> float:
        return self.__vote_weight.get(key, 0.0)

    def set_user(self, user: User) -> None:
        self.__user = user

    def get_user(self) -> User | None:
        return self.__user
