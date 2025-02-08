from pyrogram import types

from ..object import Object


class InputMediaArea(Object):

    # TODO: InputMediaAreaVenue

    def __init__(self, coordinates: "types.MediaAreaCoordinates"):
        super().__init__()

        self.coordinates = coordinates
