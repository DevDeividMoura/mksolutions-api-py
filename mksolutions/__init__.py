from __future__ import annotations

from ._client import MKSolutions
from ._base_client import DEFAULT_TIMEOUT
from .__version__ import __title__, __version__
from ._exceptions import (
    APIError,
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
    InternalServerError,
    TokenInvalidError,
    InvalidFormatError,
    ResultNotFoundError,
    TokenExpiredError,
    TokenNotFoundError,
)
from ._utils._logs import setup_logging as _setup_logging

__all__ = ["MKSolutions", "DEFAULT_TIMEOUT", "__title__", "__version__"]

_setup_logging()