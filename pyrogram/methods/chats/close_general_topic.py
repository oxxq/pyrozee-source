from typing import Union

import pyrogram
from pyrogram import raw


class CloseGeneralTopic:
    async def close_general_topic(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id), topic_id=1, closed=True
            )
        )
        return True
