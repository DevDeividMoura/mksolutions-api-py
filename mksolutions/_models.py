from typing import Union, Optional
from typing_extensions import final, ClassVar, Literal

import pydantic
from pydantic import ConfigDict

from ._types import (
    Body,
    Query,
    Headers,
    Timeout,
)

class BaseModel(pydantic.BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

@final
class FinalRequestOptions(BaseModel):
    method: str
    url: str
    params: Optional[Query] = {}
    headers: Optional[Headers] = None
    timeout: Union[float, Timeout, None] = None
