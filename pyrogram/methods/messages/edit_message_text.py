from typing import Union, List, Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils


class EditMessageText:
    async def edit_message_text(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        invert_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None,
    ) -> "types.Message":

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            no_webpage=disable_web_page_preview or None,
            invert_media=invert_media,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            **await utils.parse_text_entities(self, text, parse_mode, entities),
        )
        session = None
        business_connection = None
        if business_connection_id:
            business_connection = self.business_user_connection_cache[
                business_connection_id
            ]
            if not business_connection:
                business_connection = await self.get_business_connection(
                    business_connection_id
                )
            session = await get_session(self, business_connection._raw.connection.dc_id)
        if business_connection_id:
            r = await session.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc, connection_id=business_connection_id
                )
            )
            # await session.stop()
        else:
            r = await self.invoke(rpc)

        for i in r.updates:
            if isinstance(
                i, (raw.types.UpdateEditMessage, raw.types.UpdateEditChannelMessage)
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )
            elif isinstance(i, (raw.types.UpdateBotEditBusinessMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(
                        i, "connection_id", business_connection_id
                    ),
                    replies=0,
                )
