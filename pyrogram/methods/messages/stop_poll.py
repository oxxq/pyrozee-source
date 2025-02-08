from typing import Union

import pyrogram
from pyrogram import raw, types

from .inline_session import get_session


class StopPoll:
    async def stop_poll(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        business_connection_id: str = None,
    ) -> "types.Poll":
        poll = (await self.get_messages(chat_id=chat_id, message_ids=message_id)).poll

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            media=raw.types.InputMediaPoll(
                poll=raw.types.Poll(
                    id=int(poll.id), closed=True, question="", answers=[]
                )
            ),
            reply_markup=await reply_markup.write(self) if reply_markup else None,
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

        return types.Poll._parse(self, r.updates[0])
