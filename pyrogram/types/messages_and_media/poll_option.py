import pyrogram
from ..object import Object
from typing import List, Optional


class PollOption(Object):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        text: str,
        voter_count: int = 0,
        data: bytes = None,
        entities: Optional[List["pyrogram.types.MessageEntity"]] = None,
    ):
        super().__init__(client)

        self.text = text
        self.voter_count = voter_count
        self.data = data
        self.entities = entities

    async def write(self, client, i):
        option, entities = (
            await pyrogram.utils.parse_text_entities(
                client, self.text, None, self.entities
            )
        ).values()
        return pyrogram.raw.types.PollAnswer(
            text=pyrogram.raw.types.TextWithEntities(
                text=option, entities=entities or []
            ),
            option=bytes([i]),
        )
