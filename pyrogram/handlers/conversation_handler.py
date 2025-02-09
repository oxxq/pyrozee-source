import inspect
from typing import Union

import pyrogram
from pyrogram.types import Message, CallbackQuery
from .message_handler import MessageHandler
from .callback_query_handler import CallbackQueryHandler


class ConversationHandler(MessageHandler, CallbackQueryHandler):

    def __init__(self):
        self.waiters = {}

    async def check(
        self, client: "pyrogram.Client", update: Union[Message, CallbackQuery]
    ):
        if isinstance(update, Message) and update.outgoing:
            return False

        try:
            chat_id = (
                update.chat.id
                if isinstance(update, Message)
                else update.message.chat.id
            )
        except AttributeError:
            return False

        waiter = self.waiters.get(chat_id)
        if (
            not waiter
            or not isinstance(update, waiter["update_type"])
            or waiter["future"].done()
        ):
            return False

        filters = waiter.get("filters")
        if callable(filters):
            if inspect.iscoroutinefunction(filters.__call__):
                filtered = await filters(client, update)
            else:
                filtered = await client.loop.run_in_executor(
                    client.executor, filters, client, update
                )
            if not filtered or waiter["future"].done():
                return False

        waiter["future"].set_result(update)
        return True

    @staticmethod
    async def callback(_, __):
        pass

    def delete_waiter(self, chat_id, future):
        if future == self.waiters[chat_id]["future"]:
            del self.waiters[chat_id]
