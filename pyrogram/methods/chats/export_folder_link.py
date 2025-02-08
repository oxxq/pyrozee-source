import pyrogram
from pyrogram import raw


class ExportFolderLink:
    async def export_folder_link(self: "pyrogram.Client", folder_id: int) -> str:
        folder = await self.get_folders(folder_id)

        if not folder:
            return

        peers = []

        if folder.included_chats:
            peers.extend(iter(folder.included_chats))

        if folder.excluded_chats:
            peers.extend(iter(folder.included_chats))

        if folder.pinned_chats:
            peers.extend(iter(folder.included_chats))

        r = await self.invoke(
            raw.functions.chatlists.ExportChatlistInvite(
                chatlist=raw.types.InputChatlistDialogFilter(filter_id=folder_id),
                title=folder.title,
                peers=[await self.resolve_peer(i.id) for i in peers],
            )
        )

        return r.invite.url
