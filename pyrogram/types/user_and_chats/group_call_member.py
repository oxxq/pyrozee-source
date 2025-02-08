from datetime import datetime
from typing import Dict

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class GroupCallMember(Object):

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat" = None,
        date: datetime = None,
        active_date: datetime = None,
        volume: int = None,
        can_self_unmute: bool = None,
        is_muted: bool = None,
        is_left: bool = None,
        is_just_joined: bool = None,
        is_muted_by_you: bool = None,
        is_volume_by_admin: bool = None,
        is_self: bool = None,
        is_video_joined: bool = None,
        is_hand_raised: bool = None,
        is_video_enabled: bool = None,
        is_screen_sharing_enabled: bool = None,
    ):
        super().__init__(client)

        self.chat = chat
        self.date = date
        self.active_date = active_date
        self.volume = volume
        self.can_self_unmute = can_self_unmute
        self.is_muted = is_muted
        self.is_left = is_left
        self.is_just_joined = is_just_joined
        self.is_muted_by_you = is_muted_by_you
        self.is_volume_by_admin = is_volume_by_admin
        self.is_self = is_self
        self.is_video_joined = is_video_joined
        self.is_hand_raised = is_hand_raised
        self.is_video_enabled = is_video_enabled
        self.is_screen_sharing_enabled = is_screen_sharing_enabled

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        member: "raw.types.GroupCallParticipant",
        users: Dict[int, "raw.base.User"],
        chats: Dict[int, "raw.base.Chat"],
    ) -> "GroupCallMember":
        peer = member.peer
        peer_id = utils.get_raw_peer_id(peer)

        parsed_chat = types.Chat._parse_chat(
            client,
            users[peer_id] if isinstance(peer, raw.types.PeerUser) else chats[peer_id],
        )

        parsed_chat.bio = getattr(member, "about", None)

        return GroupCallMember(
            chat=parsed_chat,
            date=utils.timestamp_to_datetime(member.date),
            active_date=utils.timestamp_to_datetime(member.active_date),
            volume=getattr(member, "volume", None),
            can_self_unmute=member.can_self_unmute,
            is_muted=member.muted,
            is_left=member.left,
            is_just_joined=member.just_joined,
            is_muted_by_you=member.muted_by_you,
            is_volume_by_admin=member.volume_by_admin,
            is_self=member.is_self,
            is_video_joined=member.video_joined,
            is_hand_raised=bool(getattr(member, "raise_hand_rating", None)),
            is_video_enabled=bool(getattr(member, "video", None)),
            is_screen_sharing_enabled=bool(getattr(member, "presentation", None)),
            client=client,
        )
