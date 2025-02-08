import pyrogram
from pyrogram import raw


class ResetSession:
    async def reset_session(self: "pyrogram.Client", id: int) -> bool:
        r = await self.invoke(raw.functions.account.ResetAuthorization(hash=id))

        return r
