from typing import Optional

from pyrogram import types, raw
from ..object import Object


class BusinessInfo(Object):

    def __init__(
        self,
        *,
        address: str = None,
        location: "types.Location" = None,
        greeting_message: "types.BusinessMessage" = None,
        away_message: "types.BusinessMessage" = None,
        working_hours: "types.BusinessWorkingHours" = None,
    ):
        self.address = address
        self.location = location
        self.greeting_message = greeting_message
        self.away_message = away_message
        self.working_hours = working_hours

    @staticmethod
    def _parse(
        client, user: "raw.types.UserFull" = None, users: dict = None
    ) -> Optional["BusinessInfo"]:
        working_hours = getattr(user, "business_work_hours", None)
        location = getattr(user, "business_location", None)
        greeting_message = getattr(user, "business_greeting_message", None)
        away_message = getattr(user, "business_away_message", None)

        if not any((working_hours, location, greeting_message, away_message)):
            return None

        return BusinessInfo(
            address=getattr(location, "address", None),
            location=types.Location._parse(
                client, getattr(location, "geo_point", None)
            ),
            greeting_message=types.BusinessMessage._parse(
                client, greeting_message, users
            ),
            away_message=types.BusinessMessage._parse(client, away_message, users),
            working_hours=types.BusinessWorkingHours._parse(working_hours),
        )
