from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import errors


class ToggleForumTopics:
    async def toggle_forum_topics(
        self: "pyrogram.Client", chat_id: Union[int, str], enabled: bool = False
    ) -> bool:
        try:
            r = await self.invoke(
                raw.functions.channels.ToggleForum(
                    channel=await self.resolve_peer(chat_id), enabled=enabled
                )
            )

            return bool(r)
        except errors.RPCError:
            return False
