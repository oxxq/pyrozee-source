from typing import Union, List

import pyrogram
from pyrogram import raw


class ViewMessages:
    async def view_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: Union[int, List[int]],
    ) -> bool:
        ids = [message_id] if not isinstance(message_id, list) else message_id

        r = await self.invoke(
            raw.functions.messages.GetMessagesViews(
                peer=await self.resolve_peer(chat_id), id=ids, increment=True
            )
        )

        return bool(r)
