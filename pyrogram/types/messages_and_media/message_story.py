from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object
from typing import Union


class MessageStory(Object):

    def __init__(
        self,
        *,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        story_id: int,
    ):
        super().__init__()

        self.from_user = from_user
        self.sender_chat = sender_chat
        self.story_id = story_id

    @staticmethod
    async def _parse(
        client: "pyrogram.Client", message_story: "raw.types.MessageMediaStory"
    ) -> Union["MessageStory", "types.Story"]:
        from_user = None
        sender_chat = None
        user_id = None
        chat_id = None
        try:
            if isinstance(message_story.peer, raw.types.PeerChannel):
                chat_id = utils.get_channel_id(message_story.peer.channel_id)
                chat = await client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await client.resolve_peer(chat_id)]
                    )
                )
                sender_chat = types.Chat._parse_chat(client, chat.chats[0])
            else:
                user_id = message_story.peer.user_id
                from_user = await client.get_users(user_id)
            if not client.me.is_bot:
                return await client.get_stories(user_id or chat_id, message_story.id)
        except PeerIdInvalid:
            pass
        except Exception:
            pass
        return MessageStory(
            from_user=from_user, sender_chat=sender_chat, story_id=message_story.id
        )
