import pyrogram
from pyrogram import raw


class AnswerPreCheckoutQuery:
    async def answer_pre_checkout_query(
        self: "pyrogram.Client",
        pre_checkout_query_id: str,
        success: bool = None,
        error: str = None,
    ):
        return await self.invoke(
            raw.functions.messages.SetBotPrecheckoutResults(
                query_id=int(pre_checkout_query_id),
                success=success or None,
                error=error or None,
            )
        )
