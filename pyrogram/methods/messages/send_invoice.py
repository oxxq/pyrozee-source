import pyrogram

from pyrogram import types, raw, utils
from typing import Union, List


class SendInvoice:
    async def send_invoice(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        title: str,
        description: str,
        currency: str,
        prices: List["types.LabeledPrice"],
        provider: str = None,
        provider_data: str = None,
        payload: str = None,
        photo_url: str = None,
        photo_size: int = None,
        photo_mime_type: str = None,
        start_parameter: str = None,
        extended_media: "types.InputMedia" = None,
        reply_to_message_id: int = None,
        message_thread_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
    ):

        if reply_markup is not None:
            has_buy_button = False
            for i in reply_markup.inline_keyboard:
                for j in i:
                    if isinstance(j, types.InlineKeyboardButtonBuy):
                        has_buy_button = True
            if not has_buy_button:
                text = "Pay"
                if currency == "XTR":
                    prices_total = 0
                    for price in prices:
                        prices_total += price.amount
                    text = f"Pay ⭐️{prices_total}"
                reply_markup.inline_keyboard.insert(
                    0, [types.InlineKeyboardButtonBuy(text=text)]
                )

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            message_thread_id=message_thread_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
        )

        if payload is not None:
            encoded_payload = payload.encode()
        else:
            encoded_payload = f"{(title)}".encode()
        r = await self.invoke(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaInvoice(
                    title=title,
                    description=description,
                    invoice=raw.types.Invoice(
                        currency=currency, prices=[price.write() for price in prices]
                    ),
                    payload=encoded_payload,
                    provider=provider,
                    provider_data=raw.types.DataJSON(
                        data=provider_data if provider_data else "{}"
                    ),
                    photo=(
                        raw.types.InputWebDocument(
                            url=photo_url,
                            size=photo_size or 0,
                            mime_type=photo_mime_type or "image/jpeg",
                            attributes=[],
                        )
                        if photo_url
                        else None
                    ),
                    start_param=start_parameter,
                    extended_media=extended_media,
                ),
                random_id=self.rnd_id(),
                reply_to=reply_to,
                message="",
                reply_markup=(
                    await reply_markup.write(self) if reply_markup is not None else None
                ),
            )
        )

        for i in r.updates:
            if isinstance(
                i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    users={i.id: i for i in r.users},
                    chats={i.id: i for i in r.chats},
                )
