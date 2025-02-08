from ..object import Object

from pyrogram import raw
import pyrogram


class InlineKeyboardButtonBuy(Object):

    def __init__(self, text: str):
        super().__init__()

        self.text = str(text)

    @staticmethod
    def read(b):
        return InlineKeyboardButtonBuy(text=b.text)

    async def write(self, _: "pyrogram.Client"):
        return raw.types.KeyboardButtonBuy(text=self.text)
