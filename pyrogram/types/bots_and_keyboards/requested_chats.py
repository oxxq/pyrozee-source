from typing import List, Union

import pyrogram
from pyrogram import enums
from pyrogram import raw, utils, types

from ..object import Object


class RequestedChats(Object):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        button_id: int,
        chats: List["types.Chat"],
    ):
        super().__init__(client)

        self.button_id = button_id
        self.chats = chats

    @staticmethod
    def _parse(
        client,
        action: Union[
            "raw.types.MessageActionRequestedPeer",
            "raw.types.MessageActionRequestedPeerSentMe",
        ],
    ) -> "RequestedChats":
        _requested_chats = []

        for requested_peer in action.peers:
            peer_id = utils.get_peer_id(requested_peer)
            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                chat_type = enums.ChatType.PRIVATE
            elif peer_type == "chat":
                chat_type = enums.ChatType.GROUP
            else:
                chat_type = enums.ChatType.CHANNEL

            _requested_chats.append(
                types.Chat(
                    id=peer_id,
                    type=chat_type,
                    first_name=getattr(requested_peer, "first_name", None),
                    last_name=getattr(requested_peer, "last_name", None),
                    username=getattr(requested_peer, "username", None),
                    photo=types.ChatPhoto._parse(
                        client, getattr(requested_peer, "photo", None), peer_id, 0
                    ),
                    client=client,
                )
            )

        return RequestedChats(
            button_id=action.button_id,
            chats=types.List(_requested_chats),
            client=client,
        )
