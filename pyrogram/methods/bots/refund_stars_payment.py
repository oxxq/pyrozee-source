from typing import Union

import pyrogram
from pyrogram import raw


class RefundStarPayment:
    async def refund_star_payment(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        telegram_payment_charge_id: str,
    ) -> bool:
        await self.invoke(
            raw.functions.payments.RefundStarsCharge(
                user_id=await self.resolve_peer(user_id),
                charge_id=telegram_payment_charge_id,
            )
        )

        return True
