import logging
from typing import Union, List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils

log = logging.getLogger(__name__)


class GetScheduledMessages:
    async def get_scheduled_messages(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> List["types.Message"]:
        r = await self.invoke(
            raw.functions.messages.GetScheduledHistory(
                peer=await self.resolve_peer(chat_id), hash=0
            )
        )

        return await utils.parse_messages(self, r, replies=0)
