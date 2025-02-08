import pyrogram
from pyrogram import raw, types


class GetActiveSessions:
    async def get_active_sessions(self: "pyrogram.Client") -> "types.ActiveSessions":
        r = await self.invoke(raw.functions.account.GetAuthorizations())

        return types.ActiveSessions._parse(r)
