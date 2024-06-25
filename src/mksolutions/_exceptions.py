from typing import Optional

import httpx


class MKSError(Exception):
    pass


class APIError(MKSError):
    message: str
    request: httpx.Request

    body: object | None
    """The API response body.

    If the API responded with a valid JSON structure then this property will be the
    decoded result.

    If it isn't a valid JSON structure then this will be the raw response.

    If there was no response associated with this error then it will be `None`.
    """

    code: Optional[str] = None

    def __init__(self, message: str, request: httpx.Request, *, body: object | None) -> None:
        super().__init__(message)
        self.request = request
        self.message = message
        self.body = body
        self.code = None


class APIConnectionError(APIError):
    def __init__(self, *, message: str = "Connection error.", request: httpx.Request) -> None:
        super().__init__(message, request, body=None)


class APITimeoutError(APIConnectionError):
    def __init__(self, request: httpx.Request) -> None:
        super().__init__(message="Request timed out.", request=request)


class APIStatusError(APIError):
    """Raised when an API response has a status code of 4xx or 5xx."""

    response: httpx.Response
    status_code: int
    error_code: Optional[str]

    def __init__(self, message: str, *, response: httpx.Response, body: object | None) -> None:
        super().__init__(message, response.request, body=body)
        self.response = response
        self.status_code = response.status_code
        self.error_code = None


class InternalServerError(APIStatusError):
    pass


class TokenInvalidError(APIError):
    def __init__(self, message: str, request: httpx.Request, *, body: Optional[object] = None) -> None:
        super().__init__(message, request, body=body)
        self.error_code = "001"


class TokenExpiredError(APIError):
    def __init__(self, message: str, request: httpx.Request, *, body: Optional[object] = None) -> None:
        super().__init__(message, request, body=body)
        self.error_code = "999"


class TokenNotFoundError(APIError):
    def __init__(self, message: str, request: httpx.Request, *, body: Optional[object] = None) -> None:
        super().__init__(message, request, body=body)
        self.error_code = "999"


class InvalidFormatError(APIError):
    def __init__(self, message: str, request: httpx.Request, *, body: Optional[object] = None) -> None:
        super().__init__(message, request, body=body)
        self.error_code = "002"


class ResultNotFoundError(APIError):
    def __init__(self, message: str, request: httpx.Request, *, body: Optional[object] = None) -> None:
        super().__init__(message, request, body=body)
        self.error_code = "003"


class MissingBaseUrlError(MKSError):
    pass


class InvalidAuthTypeError(MKSError):
    pass


class MissingGeneralAuthParametersError(MKSError):
    pass


class MissingSpecificAuthParametersError(MKSError):
    pass
