import pyrogram
from pyrogram import raw


class ToggleFolderTags:
    async def toggle_folder_tags(self: "pyrogram.Client", enabled: bool) -> bool:
        r = await self.invoke(
            raw.functions.messages.ToggleDialogFilterTags(enabled=enabled)
        )

        return r
