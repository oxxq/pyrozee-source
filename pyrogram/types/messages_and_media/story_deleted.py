from typing import Union

from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

import pyrogram
from pyrogram import raw, types
from ..object import Object
from ..update import Update


class StoryDeleted(Object, Update):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat

    async def _parse(
        client: "pyrogram.Client",
        stories: raw.base.StoryItem,
        peer: Union["raw.types.PeerChannel", "raw.types.PeerUser"],
    ) -> "StoryDeleted":
        from_user = None
        sender_chat = None
        try:
            if isinstance(peer, raw.types.PeerChannel):
                sender_chat = await client.get_chat(peer.channel_id)
            elif isinstance(peer, raw.types.InputPeerSelf):
                from_user = client.me
            else:
                from_user = await client.get_users(peer.user_id)
        except PeerIdInvalid:
            pass

        return StoryDeleted(
            id=stories.id, from_user=from_user, sender_chat=sender_chat, client=client
        )
