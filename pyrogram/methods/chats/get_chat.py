from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils


class GetChat:
    async def get_chat(
        self: "pyrogram.Client", chat_id: Union[int, str], force_full: bool = True
    ) -> Union["types.Chat", "types.ChatPreview"]:
        match = self.INVITE_LINK_RE.match(str(chat_id))

        if match:
            r = await self.invoke(
                raw.functions.messages.CheckChatInvite(hash=match.group(1))
            )

            if isinstance(r, raw.types.ChatInvite):
                return types.ChatPreview._parse(self, r)

            await self.fetch_peers([r.chat])

            if isinstance(r.chat, raw.types.Chat):
                chat_id = -r.chat.id

            if isinstance(r.chat, raw.types.Channel):
                chat_id = utils.get_channel_id(r.chat.id)

        peer = await self.resolve_peer(chat_id)

        if force_full:
            if isinstance(peer, raw.types.InputPeerChannel):
                r = await self.invoke(
                    raw.functions.channels.GetFullChannel(channel=peer)
                )
            elif isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
                r = await self.invoke(raw.functions.users.GetFullUser(id=peer))
            else:
                r = await self.invoke(
                    raw.functions.messages.GetFullChat(chat_id=peer.chat_id)
                )

            return await types.Chat._parse_full(self, r)
        else:
            if isinstance(peer, raw.types.InputPeerChannel):
                r = await self.invoke(raw.functions.channels.GetChannels(id=[peer]))
            elif isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
                r = await self.invoke(raw.functions.users.GetUsers(id=[peer]))
            else:
                r = await self.invoke(
                    raw.functions.messages.GetChats(id=[peer.chat_id])
                )

            return types.Chat._parse_chat(
                self, r.chats[0] if isinstance(r, raw.types.messages.Chats) else r[0]
            )
