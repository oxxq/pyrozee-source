from datetime import datetime
from typing import Dict, Union

import pyrogram
from pyrogram import raw, utils
from pyrogram import types
from ..object import Object
from ..update import Update


class ChatMemberUpdated(Object, Update):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        from_user: "types.User",
        date: datetime,
        old_chat_member: "types.ChatMember",
        new_chat_member: "types.ChatMember",
        invite_link: "types.ChatInviteLink" = None,
        via_join_request: bool = None,
    ):
        super().__init__(client)

        self.chat = chat
        self.from_user = from_user
        self.date = date
        self.old_chat_member = old_chat_member
        self.new_chat_member = new_chat_member
        self.invite_link = invite_link
        self.via_join_request = via_join_request

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: Union[
            "raw.types.UpdateChatParticipant", "raw.types.UpdateChannelParticipant"
        ],
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"],
    ) -> "ChatMemberUpdated":
        chat_id = getattr(update, "chat_id", None) or getattr(update, "channel_id")

        old_chat_member = None
        new_chat_member = None
        invite_link = None
        via_join_request = None

        if update.prev_participant:
            old_chat_member = types.ChatMember._parse(
                client, update.prev_participant, users, chats
            )

        if update.new_participant:
            new_chat_member = types.ChatMember._parse(
                client, update.new_participant, users, chats
            )

        if update.invite:
            invite_link = types.ChatInviteLink._parse(client, update.invite, users)

            if isinstance(update.invite, raw.types.ChatInvitePublicJoinRequests):
                via_join_request = True

        return ChatMemberUpdated(
            chat=types.Chat._parse_chat(client, chats[chat_id]),
            from_user=types.User._parse(client, users[update.actor_id]),
            date=utils.timestamp_to_datetime(update.date),
            old_chat_member=old_chat_member,
            new_chat_member=new_chat_member,
            invite_link=invite_link,
            via_join_request=via_join_request,
            client=client,
        )
