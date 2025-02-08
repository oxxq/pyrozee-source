import pyrogram
from pyrogram import raw


class ResetSessions:
    async def reset_sessions(self: "pyrogram.Client", id: int) -> bool:
        r = await self.invoke(raw.functions.auth.ResetAuthorizations())

        return r
