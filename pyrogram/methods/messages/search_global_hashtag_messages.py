from datetime import datetime
from typing import AsyncGenerator

import pyrogram
from pyrogram import raw, types, utils


class SearchGlobalHashtagMessages:
    async def search_global_hashtag_messages(
        self: "pyrogram.Client",
        hashtag: str = "",
        offset_id: int = 0,
        offset_date: datetime = utils.zero_datetime(),
        limit: int = 0,
    ) -> AsyncGenerator["types.Message", None]:
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_peer = raw.types.InputPeerEmpty()

        while True:
            messages = await utils.parse_messages(
                self,
                await self.invoke(
                    raw.functions.channels.SearchPosts(
                        hashtag=hashtag,
                        offset_rate=utils.datetime_to_timestamp(offset_date),
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit,
                    ),
                    sleep_threshold=60,
                ),
                replies=0,
            )

            if not messages:
                return

            last = messages[-1]

            offset_date = utils.datetime_to_timestamp(last.date)
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
