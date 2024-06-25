from httpx import Timeout, Response

from typing import (
    Union,
    Mapping,
    TypeVar
)

from typing_extensions import TypedDict, Literal

_T = TypeVar("_T")

Headers = Mapping[str, str]
Query = Mapping[str, object]
Body = object

class RequestOptions(TypedDict, total=False):
    params: Query
    headers: Headers
    timeout: Union[float, Timeout, None]

# Sentinel class used until PEP 0661 is accepted
class NotGiven:
    """
    A sentinel singleton class used to distinguish omitted keyword arguments
    from those passed in with the value None (which may have different behavior).

    For example:

    ```py
    def get(timeout: Union[int, NotGiven, None] = NotGiven()) -> Response:
        ...


    get(timeout=1)  # 1s timeout
    get(timeout=None)  # No timeout
    get()  # Default timeout behavior, which may not be statically known at the method definition.
    ```
    """

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NotGivenOr = Union[_T, NotGiven]
NOT_GIVEN = NotGiven()