from pyrogram import raw
from pyrogram import types
from ..object import Object


class SuccessfulPayment(Object):

    def __init__(
        self,
        *,
        currency: str,
        total_amount: str,
        payload: str,
        telegram_payment_charge_id: str,
        provider_payment_charge_id: str,
        shipping_option_id: str = None,
        payment_info: "types.PaymentInfo" = None,
    ):
        super().__init__()

        self.currency = currency
        self.total_amount = total_amount
        self.payload = payload
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id
        self.shipping_option_id = shipping_option_id
        self.payment_info = payment_info

    @staticmethod
    def _parse(client: "pyrogram.Client", successful_payment) -> "SuccessfulPayment":
        payload = None
        telegram_payment_charge_id = None
        provider_payment_charge_id = None
        shipping_option_id = None
        payment_info = None

        if isinstance(successful_payment, raw.types.MessageActionPaymentSentMe):
            # Try to decode invoice payload into string. If that fails, fallback to bytes instead of decoding by
            # ignoring/replacing errors, this way, button clicks will still work.
            try:
                payload = successful_payment.payload.decode()
            except (UnicodeDecodeError, AttributeError):
                payload = successful_payment.payload

            telegram_payment_charge_id = successful_payment.charge.id
            provider_payment_charge_id = successful_payment.charge.provider_charge_id
            shipping_option_id = successful_payment.shipping_option_id
            payment_info = (
                types.PaymentInfo(
                    name=successful_payment.info.name,
                    phone_number=successful_payment.info.phone,
                    email=successful_payment.info.email,
                    shipping_address=types.ShippingAddress(
                        street_line1=successful_payment.info.shipping_address.street_line1,
                        street_line2=successful_payment.info.shipping_address.street_line2,
                        city=successful_payment.info.shipping_address.city,
                        state=successful_payment.info.shipping_address.state,
                        post_code=successful_payment.info.shipping_address.post_code,
                        country_code=successful_payment.info.shipping_address.country_iso2,
                    ),
                )
                if successful_payment.info
                else None
            )

        return SuccessfulPayment(
            currency=successful_payment.currency,
            total_amount=successful_payment.total_amount,
            payload=payload,
            telegram_payment_charge_id=telegram_payment_charge_id,
            provider_payment_charge_id=provider_payment_charge_id,
            shipping_option_id=shipping_option_id,
            payment_info=payment_info,
        )
