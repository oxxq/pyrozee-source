from ..object import Object


class RequestPeerTypeChannel(Object):
    # TODO user_admin_rights, bot_admin_rights

    def __init__(self, is_creator: bool = None, is_username: bool = None, max: int = 1):
        super().__init__()

        self.is_creator = is_creator
        self.is_username = is_username
        self.max = max
