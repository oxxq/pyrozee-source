import os
import re
from datetime import datetime
from typing import Union, BinaryIO, List, Optional, Callable

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileType


class SendPhoto:
    async def send_photo(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        photo: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        business_connection_id: str = None,
        reply_to_message_id: int = None,
        reply_to_story_id: int = None,
        reply_to_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        message_effect_id: int = None,
        view_once: bool = None,
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply",
        ] = None,
        progress: Callable = None,
        progress_args: tuple = (),
    ) -> Optional["types.Message"]:
        file = None

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_story_id=reply_to_story_id,
            message_thread_id=message_thread_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode,
        )

        try:
            if isinstance(photo, str):
                if os.path.isfile(photo):
                    file = await self.save_file(
                        photo, progress=progress, progress_args=progress_args
                    )
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file,
                        ttl_seconds=(1 << 31) - 1 if view_once else ttl_seconds,
                        spoiler=has_spoiler,
                    )
                elif re.match("^https?://", photo):
                    media = raw.types.InputMediaPhotoExternal(
                        url=photo,
                        ttl_seconds=(1 << 31) - 1 if view_once else ttl_seconds,
                        spoiler=has_spoiler,
                    )
                else:
                    media = utils.get_input_media_from_file_id(
                        photo,
                        FileType.PHOTO,
                        ttl_seconds=(1 << 31) - 1 if view_once else ttl_seconds,
                    )
            else:
                file = await self.save_file(
                    photo, progress=progress, progress_args=progress_args
                )
                media = raw.types.InputMediaUploadedPhoto(
                    file=file,
                    ttl_seconds=(1 << 31) - 1 if view_once else ttl_seconds,
                    spoiler=has_spoiler,
                )

            while True:
                try:
                    rpc = raw.functions.messages.SendMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=media,
                        silent=disable_notification or None,
                        reply_to=reply_to,
                        random_id=self.rnd_id(),
                        schedule_date=utils.datetime_to_timestamp(schedule_date),
                        noforwards=protect_content,
                        effect=message_effect_id,
                        invert_media=invert_media,
                        reply_markup=(
                            await reply_markup.write(self) if reply_markup else None
                        ),
                        **await utils.parse_text_entities(
                            self, caption, parse_mode, caption_entities
                        ),
                    )
                    if business_connection_id is not None:
                        r = await self.invoke(
                            raw.functions.InvokeWithBusinessConnection(
                                connection_id=business_connection_id, query=rpc
                            )
                        )
                    else:
                        r = await self.invoke(rpc)
                except FilePartMissing as e:
                    await self.save_file(photo, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(
                            i,
                            (
                                raw.types.UpdateNewMessage,
                                raw.types.UpdateNewChannelMessage,
                                raw.types.UpdateNewScheduledMessage,
                                raw.types.UpdateBotNewBusinessMessage,
                            ),
                        ):
                            return await types.Message._parse(
                                self,
                                i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(
                                    i, raw.types.UpdateNewScheduledMessage
                                ),
                                business_connection_id=business_connection_id,
                            )
        except pyrogram.StopTransmission:
            return None
