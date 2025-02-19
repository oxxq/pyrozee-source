from pyrogram import raw
from pyrogram import types
from ..object import Object


class ExtendedMediaPreview(Object):

    def __init__(
        self,
        *,
        width: int = None,
        height: int = None,
        thumb: "types.Thumbnail" = None,
        video_duration: int = None,
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.thumb = thumb
        self.video_duration = video_duration

    @staticmethod
    def _parse(
        client, media: "raw.types.MessageExtendedMediaPreview"
    ) -> "ExtendedMediaPreview":
        thumb = None
        if media.thumb:
            thumb = types.StrippedThumbnail._parse(client, media.thumb)

        return ExtendedMediaPreview(
            width=media.w,
            height=media.h,
            thumb=thumb,
            video_duration=media.video_duration,
        )
