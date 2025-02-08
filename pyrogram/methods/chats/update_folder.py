from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import enums


class UpdateFolder:
    async def update_folder(
        self: "pyrogram.Client",
        folder_id: int,
        title: str,
        included_chats: Union[Union[int, str], List[Union[int, str]]] = None,
        excluded_chats: Union[Union[int, str], List[Union[int, str]]] = None,
        pinned_chats: Union[Union[int, str], List[Union[int, str]]] = None,
        contacts: bool = None,
        non_contacts: bool = None,
        groups: bool = None,
        channels: bool = None,
        bots: bool = None,
        exclude_muted: bool = None,
        exclude_read: bool = None,
        exclude_archived: bool = None,
        color: "enums.FolderColor" = None,
        emoji: str = None,
    ) -> bool:
        if not isinstance(included_chats, list):
            included_chats = [included_chats] if included_chats else []
        if not isinstance(excluded_chats, list):
            excluded_chats = [excluded_chats] if excluded_chats else []
        if not isinstance(pinned_chats, list):
            pinned_chats = [pinned_chats] if pinned_chats else []

        r = await self.invoke(
            raw.functions.messages.UpdateDialogFilter(
                id=folder_id,
                filter=raw.types.DialogFilter(
                    id=folder_id,
                    title=title,
                    pinned_peers=[
                        await self.resolve_peer(user_id) for user_id in pinned_chats
                    ],
                    include_peers=[
                        await self.resolve_peer(user_id) for user_id in included_chats
                    ],
                    exclude_peers=[
                        await self.resolve_peer(user_id) for user_id in excluded_chats
                    ],
                    contacts=contacts,
                    non_contacts=non_contacts,
                    groups=groups,
                    broadcasts=channels,
                    bots=bots,
                    exclude_muted=exclude_muted,
                    exclude_read=exclude_read,
                    exclude_archived=exclude_archived,
                    emoticon=emoji,
                    color=color.value if color else None,
                ),
            )
        )

        return r
