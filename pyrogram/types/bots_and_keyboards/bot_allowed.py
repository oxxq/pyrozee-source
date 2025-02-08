import pyrogram

from typing import Optional

from pyrogram import raw, types
from ..object import Object


class BotAllowed(Object):

    def __init__(
        self,
        *,
        attach_menu: Optional[bool] = None,
        from_request: Optional[bool] = None,
        domain: Optional[str] = None,
        app: Optional["types.BotApp"] = None,
    ):
        super().__init__()

        self.attach_menu = attach_menu
        self.from_request = from_request
        self.domain = domain
        self.app = app

    @staticmethod
    def _parse(
        client: "pyrogram.Client", bot_allowed: "raw.types.BotAllowed"
    ) -> "BotAllowed":
        bot_app = getattr(bot_allowed, "app", None)
        return BotAllowed(
            attach_menu=getattr(bot_allowed, "attach_menu", None),
            from_request=getattr(bot_allowed, "from_request", None),
            domain=getattr(bot_allowed, "domain", None),
            app=types.BotApp._parse(client, bot_app) if bot_app is not None else None,
        )
