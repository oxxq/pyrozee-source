from typing import List

from pyrogram import types, raw
from ..object import Object


class BusinessRecipients(Object):

    def __init__(
        self,
        *,
        existing_chats: bool = None,
        new_chats: bool = None,
        contacts: bool = None,
        non_contacts: bool = None,
        exclude_selected: bool = None,
        users: List[int] = None,
    ):
        self.existing_chats = existing_chats
        self.new_chats = new_chats
        self.contacts = contacts
        self.non_contacts = non_contacts
        self.exclude_selected = exclude_selected
        self.users = users

    @staticmethod
    def _parse(
        client, recipients: "raw.types.BusinessRecipients", users: dict = None
    ) -> "BusinessRecipients":
        return BusinessRecipients(
            existing_chats=getattr(recipients, "existing_chats", None),
            new_chats=getattr(recipients, "new_chats", None),
            contacts=getattr(recipients, "contacts", None),
            non_contacts=getattr(recipients, "non_contacts", None),
            exclude_selected=getattr(recipients, "exclude_selected", None),
            users=(
                types.List(
                    types.User._parse(client, users[i]) for i in recipients.users
                )
                or None
                if getattr(recipients, "users", None)
                else None
            ),
        )
