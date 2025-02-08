from pyrogram import raw
from ..object import Object


class LabeledPrice(Object):

    def __init__(self, label: str, amount: int):
        self.label = label
        self.amount = amount

    def write(self):
        return raw.types.LabeledPrice(label=self.label, amount=self.amount)
