from typing import Union, Iterable

import pyrogram
from pyrogram import raw


class DeleteMessages:
    async def delete_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        revoke: bool = True,
        is_scheduled: bool = None,
    ) -> int:
        peer = await self.resolve_peer(chat_id)
        message_ids = (
            list(message_ids) if not isinstance(message_ids, int) else [message_ids]
        )

        if is_scheduled:
            r = await self.invoke(
                raw.functions.messages.DeleteScheduledMessages(
                    peer=peer, id=message_ids
                )
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.DeleteMessages(channel=peer, id=message_ids)
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteMessages(id=message_ids, revoke=revoke)
            )

        return len(r.updates[0].messages) if is_scheduled else r.pts_count
