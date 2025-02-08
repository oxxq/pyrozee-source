import logging
from typing import Optional

import pyrogram
from pyrogram import raw
from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputContactMessageContent(InputMessageContent):

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
    ):
        super().__init__()

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard

    async def write(self, client: "pyrogram.Client", reply_markup):
        return raw.types.InputBotInlineMessageMediaContact(
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            vcard=self.vcard,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
