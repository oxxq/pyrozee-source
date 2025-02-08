import pyrogram
from pyrogram import raw


class DeleteFolder:
    async def delete_folder(self: "pyrogram.Client", folder_id: int) -> bool:
        r = await self.invoke(raw.functions.messages.UpdateDialogFilter(id=folder_id))

        return r
