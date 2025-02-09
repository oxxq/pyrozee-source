from typing import Union

import pyrogram
from pyrogram import raw, enums


class SendChatAction:
    async def send_chat_action(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        action: "enums.ChatAction",
        message_thread_id: int = None,
        business_connection_id: str = None,
    ) -> bool:

        action_name = action.name.lower()

        if "upload" in action_name or "history" in action_name:
            action = action.value(progress=0)
        else:
            action = action.value()
        rpc = raw.functions.messages.SetTyping(
            peer=await self.resolve_peer(chat_id),
            action=action,
            top_msg_id=message_thread_id,
        )
        if business_connection_id:
            return await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    connection_id=business_connection_id, query=rpc
                )
            )
        return await self.invoke(rpc)
