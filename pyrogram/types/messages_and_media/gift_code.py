from pyrogram import raw, types, utils
from ..object import Object


class GiftCode(Object):

    def __init__(
        self, *, via_giveaway: bool, unclaimed: bool, boost_peer, months: int, slug: str
    ):
        super().__init__()

        self.via_giveaway = via_giveaway
        self.unclaimed = unclaimed
        self.boost_peer = boost_peer
        self.months = months
        self.slug = slug

    @staticmethod
    def _parse(client, giftcode: "raw.types.MessageActionGiftCode", chats):
        peer = chats.get(utils.get_raw_peer_id(getattr(giftcode, "boost_peer")))

        return GiftCode(
            via_giveaway=giftcode.via_giveaway,
            unclaimed=giftcode.unclaimed,
            boost_peer=types.Chat._parse_chat(client, peer) if peer else None,
            months=giftcode.months,
            slug=giftcode.slug,
        )

    @property
    def link(self) -> str:
        return f"https://t.me/giftcode/{self.slug}"
