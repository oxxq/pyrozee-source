from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import errors


class ToggleJoinToSend:
    async def toggle_join_to_send(
        self: "pyrogram.Client", chat_id: Union[int, str], enabled: bool = False
    ) -> bool:
        try:
            r = await self.invoke(
                raw.functions.channels.ToggleJoinToSend(
                    channel=await self.resolve_peer(chat_id), enabled=enabled
                )
            )

            return bool(r)
        except errors.RPCError:
            return False
