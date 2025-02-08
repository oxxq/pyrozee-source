import datetime
import pyrogram
from pyrogram import raw, utils

from ..object import Object


class BotBusinessConnection(Object):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        bot_connection_id: str,
        user: "pyrogram.types.User",
        dc_id: int,
        date: "datetime.datetime",
        can_reply: bool = None,
        is_disabled: bool = None,
    ):
        super().__init__(client)

        self.bot_connection_id = bot_connection_id
        self.user = user
        self.dc_id = dc_id
        self.date = date
        self.can_reply = can_reply
        self.is_disabled = is_disabled

    @staticmethod
    async def _parse(
        client: "pyrogram.Client", bot_connection: "raw.types.BotBusinessConnection"
    ) -> "BotBusinessConnection":
        return BotBusinessConnection(
            bot_connection_id=bot_connection.connection_id,
            user=await client.get_users(bot_connection.user_id),
            dc_id=bot_connection.dc_id,
            date=utils.timestamp_to_datetime(bot_connection.date),
            can_reply=bot_connection.can_reply,
            is_disabled=bot_connection.disabled,
            client=client,
        )
