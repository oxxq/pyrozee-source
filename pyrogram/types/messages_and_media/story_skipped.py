from datetime import datetime
from typing import Union

from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object
from ..update import Update


class StorySkipped(Object, Update):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        date: datetime,
        expire_date: datetime,
        close_friends: bool = None,
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.expire_date = expire_date
        self.close_friends = close_friends

    async def _parse(
        client: "pyrogram.Client",
        stories: raw.base.StoryItem,
        peer: Union["raw.types.PeerChannel", "raw.types.PeerUser"],
    ) -> "StorySkipped":
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

        return StorySkipped(
            id=stories.id,
            from_user=from_user,
            sender_chat=sender_chat,
            date=utils.timestamp_to_datetime(stories.date),
            expire_date=utils.timestamp_to_datetime(stories.expire_date),
            close_friends=stories.close_friends,
            client=client,
        )
