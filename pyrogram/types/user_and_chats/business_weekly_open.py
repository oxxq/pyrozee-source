from pyrogram import raw
from ..object import Object


class BusinessWeeklyOpen(Object):

    def __init__(
        self,
        *,
        start_minute: int,
        end_minute: int,
    ):
        self.start_minute = start_minute
        self.end_minute = end_minute

    @staticmethod
    def _parse(
        weekly_open: "raw.types.BusinessWeeklyOpen" = None,
    ) -> "BusinessWeeklyOpen":
        return BusinessWeeklyOpen(
            start_minute=weekly_open.start_minute,
            end_minute=weekly_open.end_minute,
        )
