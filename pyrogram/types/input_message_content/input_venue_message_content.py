import logging
from typing import Optional

import pyrogram
from pyrogram import raw
from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputVenueMessageContent(InputMessageContent):

    def __init__(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
    ):
        super().__init__()

        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type
        self.google_place_id = google_place_id
        self.google_place_type = google_place_type

    async def write(self, client: "pyrogram.Client", reply_markup):
        return raw.types.InputBotInlineMessageMediaVenue(
            geo_point=raw.types.InputGeoPoint(lat=self.latitude, long=self.longitude),
            title=self.title,
            address=self.address,
            provider="",  # TODO
            venue_id=self.foursquare_id,
            venue_type=self.foursquare_type,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
