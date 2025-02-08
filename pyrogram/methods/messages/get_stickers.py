import logging
from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)


class GetStickers:
    async def get_stickers(
        self: "pyrogram.Client", short_name: str
    ) -> List["types.Sticker"]:
        sticker_set = await self.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=short_name),
                hash=0,
            )
        )

        return [
            await types.Sticker._parse(self, doc, {type(a): a for a in doc.attributes})
            for doc in sticker_set.documents
        ]
