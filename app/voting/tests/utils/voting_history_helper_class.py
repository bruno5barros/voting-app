from datetime import date
from django.urls import reverse
from .base_helper_class import BaseTestHelper


class VotingHistoryTestHelper(BaseTestHelper):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.__start_date: date = date.today()
        self.__end_date: date = date.today()

    def get_voting_history_url_list(self) -> str:
        return reverse("voting-history-list")

    def get_voting_history_url_detail(self, voting_history_id: int) -> str:
        return reverse("voting-history-detail", args=[voting_history_id])

    def get_start_date(self) -> date:
        return self.__start_date

    def get_end_date(self) -> date:
        return self.__end_date
