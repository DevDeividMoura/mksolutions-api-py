import os
import contextlib
from typing import Iterator


@contextlib.contextmanager
def update_env(**new_env: str) -> Iterator[None]:
    old = os.environ.copy()

    try:
        os.environ.update(new_env)

        yield None
    finally:
        os.environ.clear()
        os.environ.update(old)