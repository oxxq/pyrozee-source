import logging
from typing import Optional

import pyrogram
from pyrogram import raw
from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputLocationMessageContent(InputMessageContent):

    def __init__(
        self,
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
    ):
        super().__init__()

        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius

    async def write(self, client: "pyrogram.Client", reply_markup):
        return raw.types.InputBotInlineMessageMediaGeo(
            geo_point=raw.types.InputGeoPoint(
                lat=self.latitude,
                long=self.longitude,
                accuracy_radius=self.horizontal_accuracy,
            ),
            heading=self.heading,
            period=self.live_period,
            proximity_notification_radius=self.proximity_alert_radius,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
