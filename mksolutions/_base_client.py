import httpx
from httpx import URL, Timeout
from typing import TypeVar, Union

from ._constants import DEFAULT_TIMEOUT

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])

class BaseClient:
    """
    Base client for making HTTP requests with httpx.

    Attributes:
        _client: An instance of httpx.Client or httpx.AsyncClient.
        _version: The version of the client.
        _base_url: The base URL for the API endpoints.
        timeout: The timeout for the HTTP requests.
    """
    _client: _HttpxClientT
    _version: str
    _base_url: URL
    timeout: Union[float, Timeout, None]

    def __init__(
        self, 
        *,
        version: str,
        base_url: Union[str, URL], 
        timeout: float | Timeout | None = DEFAULT_TIMEOUT
    )-> None:
        """
        Initializes the BaseClient with version, base_url, and timeout.

        :param version: The version of the client.
        :param base_url: The base URL for the API endpoints.
        :param timeout: The timeout for the HTTP requests.
        """
        self._version = version
        self._base_url = self._enforce_trailing_slash(URL(base_url))
        self.timeout = timeout

    def _enforce_trailing_slash(self, url: URL) -> URL:
        """
        Ensures that the URL ends with a trailing slash.

        :param url: The URL to enforce the trailing slash on.
        :return: The URL with a trailing slash.
        """
        if url.raw_path.endswith(b"/"):
            return url
        return url.copy_with(raw_path=url.raw_path + b"/")
    
    def _prepare_url(self, url: str) -> URL:
        """
        Merges a relative URL with the base URL to create a full URL.

        :param url: The relative URL to merge.
        :return: The merged full URL.
        """
        # Copied from httpx's `_merge_url` method.
        merge_url = URL(url)
        if merge_url.is_relative_url:
            merge_raw_path = self.base_url.raw_path + merge_url.raw_path.lstrip(b"/")
            return self.base_url.copy_with(raw_path=merge_raw_path)

        return merge_url
    
    @property
    def base_url(self) -> URL:
        """
        Gets the base URL of the client.

        :return: The base URL as an `httpx.URL` object.
        """
        return self._base_url
    
    @base_url.setter
    def base_url(self, url: URL | str) -> None:
        """
        Sets the base URL of the client, ensuring it ends with a trailing slash.

        :param url: The new base URL, as a string or `httpx.URL` object.
        """
        self._base_url = self._enforce_trailing_slash(url if isinstance(url, URL) else URL(url))