from typing import Optional

from pyrogram import raw
from ..object import Object


class Birthday(Object):

    def __init__(self, *, day: int, month: int, year: int = None):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(birthday: "raw.types.Birthday" = None) -> Optional["Birthday"]:
        if not birthday:
            return

        return Birthday(
            day=birthday.day, month=birthday.month, year=getattr(birthday, "year", None)
        )

    async def write(self) -> "raw.types.Birthday":
        return raw.types.Birthday(day=self.day, month=self.month, year=self.year)
