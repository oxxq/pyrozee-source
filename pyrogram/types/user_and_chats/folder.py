from typing import List, Union

import pyrogram
from pyrogram import enums
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from ..object import Object


class Folder(Object):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        included_chats: List["types.Chat"] = None,
        excluded_chats: List["types.Chat"] = None,
        pinned_chats: List["types.Chat"] = None,
        contacts: bool = None,
        non_contacts: bool = None,
        groups: bool = None,
        channels: bool = None,
        bots: bool = None,
        exclude_muted: bool = None,
        exclude_read: bool = None,
        exclude_archived: bool = None,
        emoji: str = None,
        color: "enums.FolderColor" = None,
        has_my_invites: bool = None,
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.included_chats = included_chats
        self.excluded_chats = excluded_chats
        self.pinned_chats = pinned_chats
        self.contacts = contacts
        self.non_contacts = non_contacts
        self.groups = groups
        self.channels = channels
        self.bots = bots
        self.exclude_muted = exclude_muted
        self.exclude_read = exclude_read
        self.exclude_archived = exclude_archived
        self.emoji = emoji
        self.color = color
        self.has_my_invites = has_my_invites

    @staticmethod
    def _parse(client, folder: "raw.types.DialogFilter", users, chats) -> "Folder":
        included_chats = []
        excluded_chats = []
        pinned_chats = []

        for peer in folder.include_peers:
            try:
                included_chats.append(
                    types.Chat._parse_dialog(client, peer, users, chats)
                )
            except KeyError:
                pass

        if getattr(folder, "exclude_peers", None):
            for peer in folder.exclude_peers:
                try:
                    excluded_chats.append(
                        types.Chat._parse_dialog(client, peer, users, chats)
                    )
                except KeyError:
                    pass

        for peer in folder.pinned_peers:
            try:
                pinned_chats.append(
                    types.Chat._parse_dialog(client, peer, users, chats)
                )
            except KeyError:
                pass

        return Folder(
            id=folder.id,
            title=folder.title,
            included_chats=types.List(included_chats) or None,
            excluded_chats=types.List(excluded_chats) or None,
            pinned_chats=types.List(pinned_chats) or None,
            contacts=getattr(folder, "contacts", None),
            non_contacts=getattr(folder, "non_contacts", None),
            groups=getattr(folder, "groups", None),
            channels=getattr(folder, "broadcasts", None),
            bots=getattr(folder, "bots", None),
            exclude_muted=getattr(folder, "exclude_muted", None),
            exclude_read=getattr(folder, "exclude_read", None),
            exclude_archived=getattr(folder, "exclude_archived", None),
            emoji=folder.emoticon or None,
            color=enums.FolderColor(getattr(folder, "color", None)),
            has_my_invites=getattr(folder, "has_my_invites", None),
            client=client,
        )

    async def delete(self):
        return await self._client.delete_folder(self.id)

    async def update(
        self,
        included_chats: List[Union[int, str]] = None,
        excluded_chats: List[Union[int, str]] = None,
        pinned_chats: List[Union[int, str]] = None,
        title: str = None,
        contacts: bool = None,
        non_contacts: bool = None,
        groups: bool = None,
        channels: bool = None,
        bots: bool = None,
        exclude_muted: bool = None,
        exclude_read: bool = None,
        exclude_archived: bool = None,
        emoji: str = None,
        color: "enums.FolderColor" = None,
    ):
        if not included_chats:
            included_chats = [i.id for i in self.included_chats or []]

        if not included_chats:
            excluded_chats = [i.id for i in self.excluded_chats or []]

        if not included_chats:
            pinned_chats = [i.id for i in self.pinned_chats or []]

        return await self._client.update_folder(
            folder_id=self.id,
            title=title or self.title,
            included_chats=included_chats,
            excluded_chats=excluded_chats,
            pinned_chats=pinned_chats,
            contacts=contacts or self.contacts,
            non_contacts=non_contacts or self.non_contacts,
            groups=groups or self.groups,
            channels=channels or self.channels,
            bots=bots or self.bots,
            exclude_muted=exclude_muted or self.exclude_muted,
            exclude_read=exclude_read or self.exclude_read,
            exclude_archived=exclude_archived or self.exclude_archived,
            emoji=emoji or self.emoji,
            color=color or self.color,
        )

    async def include_chat(self, chat_id: Union[int, str]):
        return await self.update(
            included_chats=[i.id for i in self.included_chats or []] + [chat_id],
            excluded_chats=[i.id for i in self.excluded_chats or []],
            pinned_chats=[i.id for i in self.pinned_chats or []],
        )

    async def exclude_chat(self, chat_id: Union[int, str]):
        return await self.update(
            included_chats=[i.id for i in self.included_chats or []],
            excluded_chats=[i.id for i in self.excluded_chats or []] + [chat_id],
            pinned_chats=[i.id for i in self.pinned_chats or []],
        )

    async def update_color(self, color: "enums.FolderColor"):
        return await self.update(color=color)

    async def pin_chat(self, chat_id: Union[int, str]):
        return await self.update(
            included_chats=[i.id for i in self.included_chats or []] + [chat_id],
            excluded_chats=[i.id for i in self.excluded_chats or []],
            pinned_chats=[i.id for i in self.pinned_chats or []] + [chat_id],
        )

    async def remove_chat(self, chat_id: Union[int, str]):
        peer = await self._client.resolve_peer(chat_id)
        peer_id = utils.get_peer_id(peer)

        return await self.update(
            included_chats=[i.id for i in self.included_chats or [] if peer_id != i.id],
            excluded_chats=[i.id for i in self.excluded_chats or [] if peer_id != i.id],
            pinned_chats=[i.id for i in self.pinned_chats or [] if peer_id != i.id],
        )

    async def export_link(self):
        return await self._client.export_folder_link(folder_id=self.id)
