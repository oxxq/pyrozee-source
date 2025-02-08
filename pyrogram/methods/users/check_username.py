from typing import Union

import pyrogram
from pyrogram import raw


class CheckUsername:
    async def check_username(
        self: "pyrogram.Client", chat_id: Union[int, str], username: str
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.CheckUsername(channel=peer, username=username)
            )
        else:
            r = await self.invoke(
                raw.functions.account.CheckUsername(username=username)
            )

        return bool(r)
