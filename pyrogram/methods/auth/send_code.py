import logging
from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.errors import PhoneMigrate, NetworkMigrate
from pyrogram.session import Session, Auth

log = logging.getLogger(__name__)


class SendCode:
    async def send_code(
        self: "pyrogram.Client",
        phone_number: str,
        current_number: bool = None,
        allow_flashcall: bool = None,
        allow_app_hash: bool = None,
        allow_missed_call: bool = None,
        allow_firebase: bool = None,
        logout_tokens: List[bytes] = None,
        token: str = None,
        app_sandbox: bool = None,
    ) -> "types.SentCode":
        phone_number = phone_number.strip(" +")

        while True:
            try:
                r = await self.invoke(
                    raw.functions.auth.SendCode(
                        phone_number=phone_number,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        settings=raw.types.CodeSettings(
                            allow_flashcall=allow_flashcall,
                            current_number=current_number,
                            allow_app_hash=allow_app_hash,
                            allow_missed_call=allow_missed_call,
                            allow_firebase=allow_firebase,
                            logout_tokens=logout_tokens,
                            token=token,
                            app_sandbox=app_sandbox,
                        ),
                    )
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                await self.session.stop()

                await self.storage.dc_id(e.value)
                await self.storage.auth_key(
                    await Auth(
                        self, await self.storage.dc_id(), await self.storage.test_mode()
                    ).create()
                )
                self.session = Session(
                    self,
                    await self.storage.dc_id(),
                    await self.storage.auth_key(),
                    await self.storage.test_mode(),
                )

                await self.session.start()
            else:
                return types.SentCode._parse(r)
