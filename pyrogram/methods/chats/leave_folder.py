import re

import pyrogram
from pyrogram import raw, utils


class LeaveFolder:
    async def leave_folder(
        self: "pyrogram.Client", link: str, keep_chats: bool = True
    ) -> bool:
        match = re.match(
            r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:addlist/|\+))([\w-]+)$",
            link,
        )

        if match:
            slug = match.group(1)
        elif isinstance(link, str):
            slug = link
        else:
            raise ValueError("Invalid folder invite link")

        r = await self.invoke(raw.functions.chatlists.CheckChatlistInvite(slug=slug))

        await self.invoke(
            raw.functions.chatlists.LeaveChatlist(
                chatlist=raw.types.InputChatlistDialogFilter(filter_id=r.filter_id),
                peers=(
                    [
                        await self.resolve_peer(utils.get_peer_id(id))
                        for id in r.already_peers
                    ]
                    if not keep_chats
                    else []
                ),
            )
        )

        return True
