import pyrogram

from pyrogram import raw, types
from ..object import Object


class MediaArea(Object):

    def __init__(self, coordinates: "types.MediaAreaCoordinates"):
        super().__init__()

        self.coordinates = coordinates

    async def _parse(
        self: "pyrogram.Client", media_area: "raw.base.MediaArea"
    ) -> "MediaArea":
        if isinstance(media_area, raw.types.MediaAreaChannelPost):
            try:
                return await types.MediaAreaChannelPost._parse(self, media_area)
            except Exception:
                return None
