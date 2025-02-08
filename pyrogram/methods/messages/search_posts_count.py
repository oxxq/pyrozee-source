import pyrogram
from pyrogram import raw


class SearchPostsCount:
    async def search_posts_count(
        self: "pyrogram.Client",
        hashtag: str,
    ) -> int:
        r = await self.invoke(
            raw.functions.channels.SearchPosts(
                hashtag=hashtag,
                offset_rate=0,
                offset_peer=raw.types.InputPeerEmpty(),
                offset_id=0,
                limit=1,
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)
