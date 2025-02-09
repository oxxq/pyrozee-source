from typing import Union

import pyrogram
from pyrogram import raw


class CloseForumTopic:
    async def close_forum_topic(
        self: "pyrogram.Client", chat_id: Union[int, str], topic_id: int
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id), topic_id=topic_id, closed=True
            )
        )
        return True
