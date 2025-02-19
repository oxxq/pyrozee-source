import pyrogram

from pyrogram import raw, types, utils

from .media_area import MediaArea


class MediaAreaChannelPost(MediaArea):

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates",
        chat: "types.Chat",
        message_id: int,
    ):
        super().__init__(coordinates=coordinates)

        self.coordinates = coordinates
        self.chat = chat
        self.message_id = message_id

    async def _parse(
        client: "pyrogram.Client", media_area: "raw.types.MediaAreaChannelPost"
    ) -> "MediaAreaChannelPost":
        channel_id = utils.get_channel_id(media_area.channel_id)
        chat = types.Chat._parse_chat(
            client,
            (
                await client.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await client.resolve_peer(channel_id)]
                    )
                )
            ).chats[0],
        )
        return MediaAreaChannelPost(
            coordinates=types.MediaAreaCoordinates._parse(media_area.coordinates),
            chat=chat,
            message_id=media_area.msg_id,
        )
