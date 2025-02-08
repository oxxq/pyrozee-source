import pyrogram
from pyrogram import raw, types


class GetCollectibleItemInfo:
    async def get_collectible_item_info(
        self: "pyrogram.Client", username: str = None, phone_number: str = None
    ) -> "types.CollectibleInfo":

        input_collectible = None

        if username:
            input_collectible = raw.types.InputCollectibleUsername(username=username)
        elif phone_number:
            input_collectible = raw.types.InputCollectiblePhone(phone=phone_number)
        else:
            raise ValueError(
                "No argument supplied. Either pass username OR phone_number"
            )

        r = await self.invoke(
            raw.functions.fragment.GetCollectibleInfo(collectible=input_collectible)
        )

        return types.CollectibleItemInfo._parse(r)
