from ..object import Object


class RequestPeerTypeChat(Object):
    # TODO user_admin_rights, bot_admin_rights

    def __init__(
        self,
        is_creator: bool = None,
        is_bot_participant: bool = None,
        is_username: bool = None,
        is_forum: bool = None,
        max: int = 1,
    ):
        super().__init__()

        self.is_creator = is_creator
        self.is_bot_participant = is_bot_participant
        self.is_username = is_username
        self.is_forum = is_forum
        self.max = max
