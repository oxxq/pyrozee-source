import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils

log = logging.getLogger(__name__)


# TODO: Rewrite using a flag for replied messages and have message_ids non-optional


class GetMessages:
    async def get_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str] = None,
        message_ids: Union[int, Iterable[int]] = None,
        reply_to_message_ids: Union[int, Iterable[int]] = None,
        replies: int = 1,
        link: str = None,
    ) -> Union["types.Message", List["types.Message"]]:
        if chat_id:
            ids, ids_type = (
                (message_ids, raw.types.InputMessageID)
                if message_ids
                else (
                    (reply_to_message_ids, raw.types.InputMessageReplyTo)
                    if reply_to_message_ids
                    else (None, None)
                )
            )

            if ids is None:
                raise ValueError(
                    "No argument supplied. Either pass message_ids or reply_to_message_ids"
                )

            peer = await self.resolve_peer(chat_id)

            is_iterable = not isinstance(ids, int)
            ids = list(ids) if is_iterable else [ids]
            ids = [ids_type(id=i) for i in ids]

            if replies < 0:
                replies = (1 << 31) - 1

            if isinstance(peer, raw.types.InputPeerChannel):
                rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
            else:
                rpc = raw.functions.messages.GetMessages(id=ids)

            r = await self.invoke(rpc, sleep_threshold=-1)

            messages = await utils.parse_messages(self, r, replies=replies)

            return messages if is_iterable else messages[0] if messages else None

        if link:
            linkps = link.split("/")
            raw_chat_id, message_thread_id, message_id = None, None, None
            if len(linkps) == 7 and linkps[3] == "c":
                # https://t.me/c/1192302355/322/487
                raw_chat_id = utils.get_channel_id(int(linkps[4]))
                message_thread_id = int(linkps[5])
                message_id = int(linkps[6])
            elif len(linkps) == 6:
                if linkps[3] == "c":
                    # https://t.me/c/1387666944/609282
                    raw_chat_id = utils.get_channel_id(int(linkps[4]))
                    message_id = int(linkps[5])
                else:
                    # https://t.me/TheForum/322/487
                    raw_chat_id = linkps[3]
                    message_thread_id = int(linkps[4])
                    message_id = int(linkps[5])
            elif len(linkps) == 5:
                # https://t.me/pyrogramchat/609282
                raw_chat_id = linkps[3]
                message_id = int(linkps[4])
            return await self.get_messages(chat_id=raw_chat_id, message_ids=message_id)

        raise ValueError(
            "No argument supplied. Either pass link OR (chat_id, message_ids or reply_to_message_ids)"
        )
