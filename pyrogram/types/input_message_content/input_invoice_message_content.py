import logging
from typing import Optional, List, Union

import pyrogram
from pyrogram import raw, types
from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputInvoiceMessageContent(InputMessageContent):

    def __init__(
        self,
        title: str,
        description: str,
        payload: Union[str, bytes],
        currency: str,
        prices: List["types.LabeledPrice"],
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: List[int] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
    ):
        super().__init__()

        self.title = title
        self.description = description
        self.payload = payload
        self.currency = currency
        self.prices = prices
        self.provider_token = provider_token
        self.max_tip_amount = max_tip_amount
        self.suggested_tip_amounts = suggested_tip_amounts
        self.provider_data = provider_data
        self.photo_url = photo_url
        self.photo_size = photo_size
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.need_name = need_name
        self.need_phone_number = need_phone_number
        self.need_email = need_email
        self.need_shipping_address = need_shipping_address
        self.send_phone_number_to_provider = send_phone_number_to_provider
        self.send_email_to_provider = send_email_to_provider
        self.is_flexible = is_flexible

    async def write(self, client: "pyrogram.Client", reply_markup):
        return raw.types.InputBotInlineMessageMediaInvoice(
            title=self.title,
            description=self.description,
            photo=(
                raw.types.InputWebDocument(
                    url=self.photo_url,
                    mime_type="image/jpg",
                    size=self.photo_size,
                    attributes=[
                        raw.types.DocumentAttributeImageSize(
                            w=self.photo_width, h=self.photo_height
                        )
                    ],
                )
                if self.photo_url
                else None
            ),
            invoice=raw.types.Invoice(
                currency=self.currency,
                prices=[i.write() for i in self.prices],
                test=client.test_mode,
                name_requested=self.need_name,
                phone_requested=self.need_phone_number,
                email_requested=self.need_email,
                shipping_address_requested=self.need_shipping_address,
                flexible=self.is_flexible,
                phone_to_provider=self.send_phone_number_to_provider,
                email_to_provider=self.send_email_to_provider,
            ),
            payload=(
                self.payload.encode() if isinstance(self.payload, str) else self.payload
            ),
            provider=self.provider_token,
            provider_data=raw.types.DataJSON(
                data=self.provider_data if self.provider_data else "{}"
            ),
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
