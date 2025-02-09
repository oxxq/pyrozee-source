import pyrogram
from pyrogram import raw
from pyrogram import types
from typing import Union


class UnhideGeneralTopic:
    async def unhide_general_topic(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id), topic_id=1, hidden=False
            )
        )
        return True
