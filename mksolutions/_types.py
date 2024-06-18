from httpx import Timeout, Response

from typing import (
    Union,
    Mapping
)

from typing_extensions import TypedDict

Headers = Mapping[str, str]
Query = Mapping[str, object]
Body = object

class RequestOptions(TypedDict, total=False):
    params: Query
    headers: Headers
    timeout: Union[float, Timeout, None]


