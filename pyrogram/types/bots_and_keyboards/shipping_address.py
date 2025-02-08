from ..object import Object


class ShippingAddress(Object):

    def __init__(
        self,
        *,
        street_line1: str,
        street_line2: str,
        city: str,
        state: str,
        post_code: str,
        country_code: str,
    ):
        super().__init__()

        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.city = city
        self.state = state
        self.post_code = post_code
        self.country_code = country_code
