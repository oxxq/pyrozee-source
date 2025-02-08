from typing import Union, BinaryIO, Optional

import pyrogram
from pyrogram import raw


class SetProfilePhoto:
    async def set_profile_photo(
        self: "pyrogram.Client",
        *,
        photo: Optional[Union[str, BinaryIO]] = None,
        video: Optional[Union[str, BinaryIO]] = None,
        is_public: Optional[bool] = None,
    ) -> bool:

        return bool(
            await self.invoke(
                raw.functions.photos.UploadProfilePhoto(
                    fallback=is_public,
                    file=await self.save_file(photo),
                    video=await self.save_file(video),
                )
            )
        )
