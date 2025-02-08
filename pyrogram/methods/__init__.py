from .advanced import Advanced
from .auth import Auth
from .bots import Bots
from .chats import Chats
from .invite_links import InviteLinks
from .messages import Messages
from .pyromod import Pyromod
from .users import Users
from .utilities import Utilities


class Methods(
    Advanced,
    Auth,
    Bots,
    Pyromod,
    Chats,
    Users,
    Messages,
    Utilities,
):
    pass
