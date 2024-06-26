from __future__ import annotations

from typing import (
    Any,
    Tuple,
    Mapping,
    TypeVar,
    Callable,
    Iterable,
    Sequence,
)
from typing_extensions import TypeGuard

from bs4 import BeautifulSoup

from .._types import NotGiven, NotGivenOr

_T = TypeVar("_T")
_TupleT = TypeVar("_TupleT", bound=Tuple[object, ...])
_MappingT = TypeVar("_MappingT", bound=Mapping[str, object])
_SequenceT = TypeVar("_SequenceT", bound=Sequence[object])
CallableT = TypeVar("CallableT", bound=Callable[..., Any])


def flatten(t: Iterable[Iterable[_T]]) -> list[_T]:
    return [item for sublist in t for item in sublist]

def is_given(obj: NotGivenOr[_T]) -> TypeGuard[_T]:
    return not isinstance(obj, NotGiven)


# Type safe methods for narrowing types with TypeVars.
# The default narrowing for isinstance(obj, dict) is dict[unknown, unknown],
# however this cause Pyright to rightfully report errors. As we know we don't
# care about the contained types we can safely use `object` in it's place.
#
# There are two separate functions defined, `is_*` and `is_*_t` for different use cases.
# `is_*` is for when you're dealing with an unknown input
# `is_*_t` is for when you're narrowing a known union type to a specific subset


def is_tuple(obj: object) -> TypeGuard[tuple[object, ...]]:
    return isinstance(obj, tuple)


def is_tuple_t(obj: _TupleT | object) -> TypeGuard[_TupleT]:
    return isinstance(obj, tuple)


def is_sequence(obj: object) -> TypeGuard[Sequence[object]]:
    return isinstance(obj, Sequence)


def is_sequence_t(obj: _SequenceT | object) -> TypeGuard[_SequenceT]:
    return isinstance(obj, Sequence)


def is_mapping(obj: object) -> TypeGuard[Mapping[str, object]]:
    return isinstance(obj, Mapping)


def is_mapping_t(obj: _MappingT | object) -> TypeGuard[_MappingT]:
    return isinstance(obj, Mapping)


def is_dict(obj: object) -> TypeGuard[dict[object, object]]:
    return isinstance(obj, dict)


def is_list(obj: object) -> TypeGuard[list[object]]:
    return isinstance(obj, list)


def is_iterable(obj: object) -> TypeGuard[Iterable[object]]:
    return isinstance(obj, Iterable)


def _extract_error_message_from_html(html_text: str) -> str:
    """
    Extrai a mensagem de erro de um HTML.

    :param html_text: O texto HTML da resposta.
    :return: A mensagem de erro extraída.
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        message = p.find('b', string=lambda x: x and 'Message' in x)
        if message: return p.text.strip()
    return html_text.strip()

def _format_address(address: str) -> str:
    """
    Formats an address by replacing ' - ' with ', '.

    :param address: The address to be formatted.
    :type address: str

    :return: The formatted address.
    :rtype: str
    """
    return address.replace(" - ", ", ")