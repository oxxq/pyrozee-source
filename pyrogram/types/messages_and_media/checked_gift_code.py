from datetime import datetime

from pyrogram import raw, types, utils
from ..object import Object


class CheckedGiftCode(Object):

    def __init__(
        self,
        *,
        date: datetime,
        months: int,
        via_giveaway: bool = None,
        from_chat: "types.Chat" = None,
        winner: "types.User" = None,
        giveaway_message_id: int = None,
        used_date: datetime = None,
    ):
        super().__init__()

        self.date = date
        self.months = months
        self.via_giveaway = via_giveaway
        self.from_chat = from_chat
        self.winner = winner
        self.giveaway_message_id = giveaway_message_id
        self.used_date = used_date

    @staticmethod
    def _parse(
        client, checked_gift_code: "raw.types.payments.CheckedGiftCode", users, chats
    ):
        from_chat = None
        winner = None

        if getattr(checked_gift_code, "from_id", None):
            from_chat = types.Chat._parse_chat(
                client, chats.get(utils.get_raw_peer_id(checked_gift_code.from_id))
            )
        if getattr(checked_gift_code, "to_id", None):
            winner = types.User._parse(client, users.get(checked_gift_code.to_id))

        return CheckedGiftCode(
            date=utils.timestamp_to_datetime(checked_gift_code.date),
            months=checked_gift_code.months,
            via_giveaway=getattr(checked_gift_code, "via_giveaway", None),
            from_chat=from_chat,
            winner=winner,
            giveaway_message_id=getattr(checked_gift_code, "giveaway_msg_id", None),
            used_date=(
                utils.timestamp_to_datetime(checked_gift_code.used_date)
                if getattr(checked_gift_code, "used_date")
                else None
            ),
        )
