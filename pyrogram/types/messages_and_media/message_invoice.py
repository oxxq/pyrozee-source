import pyrogram

from pyrogram import raw, types, utils
from ..object import Object


class MessageInvoice(Object):

    def __init__(
        self,
        *,
        title: str,
        description: str,
        currency: str,
        total_amount: int,
        start_parameter: str,
        shipping_address_requested: bool = None,
        test: bool = None,
        receipt_message_id: int = None,
        # TODO: Implement photo, extended_media parameters
    ):
        super().__init__()

        self.title = title
        self.description = description
        self.currency = currency
        self.total_amount = total_amount
        self.start_parameter = start_parameter
        self.shipping_address_requested = shipping_address_requested
        self.test = test
        self.receipt_message_id = receipt_message_id

    @staticmethod
    def _parse(message_invoice: "raw.types.MessageMediaInvoice") -> "MessageInvoice":
        return MessageInvoice(
            title=message_invoice.title,
            description=message_invoice.description,
            currency=message_invoice.currency,
            total_amount=message_invoice.total_amount,
            start_parameter=message_invoice.start_param,
            shipping_address_requested=message_invoice.shipping_address_requested,
            test=message_invoice.test,
            receipt_message_id=message_invoice.receipt_msg_id,
        )
