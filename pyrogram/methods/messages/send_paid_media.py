import os
import re

from datetime import datetime
from pymediainfo import MediaInfo
from typing import Union, List, Optional

import pyrogram
from pyrogram import raw, utils, enums
from pyrogram import types
from pyrogram.file_id import FileType


class SendPaidMedia:
    async def send_paid_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        stars_amount: int,
        media: List[
            Union[
                "types.InputMediaAnimation",
                "types.InputMediaPhoto",
                "types.InputMediaVideo",
            ]
        ],
        caption: str = "",
        caption_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        disable_notification: bool = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        invert_media: bool = None,
    ) -> "types.Message":
        multi_media = []

        for i in media:
            if isinstance(i, types.InputMediaPhoto):
                if isinstance(i.media, str):
                    if os.path.isfile(i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(i.media),
                                    spoiler=i.has_spoiler,
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaPhotoExternal(
                                    url=i.media, spoiler=i.has_spoiler
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.PHOTO
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedPhoto(
                                file=await self.save_file(i.media),
                                spoiler=i.has_spoiler,
                            ),
                        )
                    )

                    media = raw.types.InputMediaPhoto(
                        id=raw.types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference,
                        ),
                        spoiler=i.has_spoiler,
                    )
            elif isinstance(i, types.InputMediaVideo) or isinstance(
                i, types.InputMediaAnimation
            ):
                if isinstance(i.media, str):
                    is_animation = False
                    if os.path.isfile(i.media):
                        try:
                            videoInfo = MediaInfo.parse(i.media)
                        except OSError:
                            is_animation = (
                                True
                                if isinstance(i, types.InputMediaAnimation)
                                else False
                            )
                        else:
                            if not any(
                                [
                                    track.track_type == "Audio"
                                    for track in videoInfo.tracks
                                ]
                            ):
                                is_animation = True
                        attributes = [
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=(
                                    True
                                    if is_animation
                                    else (i.supports_streaming or None)
                                ),
                                duration=i.duration,
                                w=i.width,
                                h=i.height,
                            ),
                            raw.types.DocumentAttributeFilename(
                                file_name=os.path.basename(i.media)
                            ),
                        ]
                        if is_animation:
                            attributes.append(raw.types.DocumentAttributeAnimated())
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedDocument(
                                    file=await self.save_file(i.media),
                                    thumb=await self.save_file(i.thumb),
                                    spoiler=i.has_spoiler,
                                    mime_type=self.guess_mime_type(i.media)
                                    or "video/mp4",
                                    nosound_video=is_animation,
                                    attributes=attributes,
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media, spoiler=i.has_spoiler
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.VIDEO
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumb),
                                spoiler=i.has_spoiler,
                                mime_type=self.guess_mime_type(
                                    getattr(i.media, "name", "video.mp4")
                                )
                                or "video/mp4",
                                attributes=[
                                    raw.types.DocumentAttributeVideo(
                                        supports_streaming=i.supports_streaming or None,
                                        duration=i.duration,
                                        w=i.width,
                                        h=i.height,
                                    ),
                                    raw.types.DocumentAttributeFilename(
                                        file_name=getattr(i.media, "name", "video.mp4")
                                    ),
                                ],
                            ),
                        )
                    )

                    media = raw.types.InputMediaDocument(
                        id=raw.types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference,
                        ),
                        spoiler=i.has_spoiler,
                    )
            else:
                raise ValueError(
                    f"{i.__class__.__name__} is not a supported type for send_paid_media"
                )
            multi_media.append(media)

        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=raw.types.InputMediaPaidMedia(
                stars_amount=stars_amount, extended_media=multi_media
            ),
            silent=disable_notification or None,
            random_id=self.rnd_id(),
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            invert_media=invert_media,
            **await utils.parse_text_entities(
                self, caption, parse_mode, caption_entities
            ),
        )
        r = await self.invoke(rpc, sleep_threshold=60)

        return await utils.parse_messages(
            self,
            raw.types.messages.Messages(
                messages=[
                    m.message
                    for m in filter(
                        lambda u: isinstance(
                            u,
                            (
                                raw.types.UpdateNewMessage,
                                raw.types.UpdateNewChannelMessage,
                                raw.types.UpdateNewScheduledMessage,
                                raw.types.UpdateBotNewBusinessMessage,
                            ),
                        ),
                        r.updates,
                    )
                ],
                users=r.users,
                chats=r.chats,
            ),
        )
