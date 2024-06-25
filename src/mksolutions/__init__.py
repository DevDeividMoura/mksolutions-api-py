from __future__ import annotations

from ._client import MKSolutions
from .__version__ import __title__, __version__
from ._exceptions import (
    APIError,
    APIStatusError,
    APITimeoutError,
    TokenExpiredError,
    TokenInvalidError,
    APIConnectionError,
    InvalidFormatError,
    TokenNotFoundError,
    InternalServerError,
    ResultNotFoundError,
)
from ._base_client import DEFAULT_TIMEOUT
from ._utils._logs import setup_logging as _setup_logging

__all__ = [
    "MKSolutions",
    "DEFAULT_TIMEOUT",
    "__title__",
    "__version__",
    "APIError",
    "APIStatusError",
    "APITimeoutError",
    "TokenExpiredError",
    "TokenInvalidError",
    "APIConnectionError",
    "InvalidFormatError",
    "TokenNotFoundError",
    "InternalServerError",
    "ResultNotFoundError",
]

_setup_logging()
