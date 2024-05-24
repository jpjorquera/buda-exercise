NOT_FOUND_ERROR_MESSAGE = "Not found"
EXTERNAL_API_ERROR_MESSAGE = "External API error"
INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error"


class OrderBookNotFoundError(Exception):
    def __init__(self, market, message=NOT_FOUND_ERROR_MESSAGE):
        self.market = market
        self.message = message
        super().__init__(self.message)


class ExternalAPIError(Exception):
    def __init__(self, message=EXTERNAL_API_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)


class InternalServerError(Exception):
    def __init__(self, message=INTERNAL_SERVER_ERROR_MESSAGE):
        self.message = message
        super().__init__(self.message)
