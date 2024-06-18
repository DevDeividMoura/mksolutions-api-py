from typing import Union, Optional
from typing_extensions import final, ClassVar

import pydantic
from pydantic import ConfigDict

from ._types import (
    Body,
    Query,
    Headers,
    Timeout,
)

@final
class FinalRequestOptions(pydantic.BaseModel):
    method: str
    url: str
    params: Optional[Query] = {}
    headers: Optional[Headers] = None
    timeout: Union[float, Timeout, None] = None

    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)
