import json
import logging
from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, Union, Generic, Mapping, TypeVar, Optional, cast

import httpx
from httpx import URL

from ._qs import Querystring
from ._types import NOT_GIVEN, Timeout, NotGiven, Response, RequestParams
from ._models import FinalRequestOptions
from ._constants import DEFAULT_TIMEOUT
from ._exceptions import (
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
)
from ._utils._utils import is_given, _extract_error_message_from_html

log: logging.Logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT
else:
    try:
        from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT
    except ImportError:
        # taken from https://github.com/encode/httpx/blob/3ba5fe0d7ac70222590e759c31442b1cab263791/httpx/_config.py#L366
        HTTPX_DEFAULT_TIMEOUT = Timeout(5.0)

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[_HttpxClientT]):
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
        timeout: float | Timeout | None = DEFAULT_TIMEOUT,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initializes the BaseClient with version, base_url, and timeout.

        :param version: The version of the client.
        :param base_url: The base URL for the API endpoints.
        :param timeout: The timeout for the HTTP requests.
        """
        self._version = version
        self._base_url = self._enforce_trailing_slash(URL(base_url))
        self.timeout = timeout
        self._custom_headers = custom_headers or {}

    @staticmethod
    def _enforce_trailing_slash(url: URL) -> URL:
        """
        Ensures that the URL ends with a trailing slash.

        :param url: The URL to enforce the trailing slash on.
        :return: The URL with a trailing slash.
        """
        return url if url.raw_path.endswith(b"/") else url.copy_with(raw_path=url.raw_path + b"/")

    def _make_status_error_from_response(
        self,
        response: httpx.Response,
    ) -> APIStatusError:
        """
        Creates an APIStatusError from the given HTTP response.

        :param response: The HTTP response.
        :return: An APIStatusError instance.
        """

        err_text = response.text.strip()
        if response.status_code == 500 and "text/html" in response.headers.get("Content-Type", ""):
            err_msg = _extract_error_message_from_html(err_text)
            body = err_text
        else:
            try:
                body = response.json()
                err_msg = body.get("Mensagem", err_text)
            except (json.JSONDecodeError, AttributeError):
                body = err_text
                err_msg = err_text or f"Error code: {response.status_code}"

        return self._make_status_error(err_msg, body=body, response=response)

    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        """
        Abstract method to create a status error.
        """
        raise NotImplementedError()

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

    def _build_headers(self) -> httpx.Headers:
        """
        Builds the headers for the HTTP request.

        :return: The headers.
        """
        return httpx.Headers(self._custom_headers)

    def _build_request(
        self,
        options: FinalRequestOptions,
    ) -> httpx.Request:
        """
        Builds an HTTP request from the given options.

        :param options: The request options.
        :return: An HTTP request.
        """
        # if log.isEnabledFor(logging.DEBUG):
        log.debug("Request options: %s", options.model_dump(exclude_unset=True))

        headers = self._build_headers()

        return self._client.build_request(
            method=options.method,
            url=self._prepare_url(options.url),
            params=self.qs.stringify(cast(Mapping[str, Any], options.params)) if options.params else None,
            headers=headers,
            timeout=self.timeout if options.timeout is None else options.timeout,
        )
    
    @property
    def qs(self) -> Querystring:
        return Querystring()

    @property
    def base_url(self) -> URL:
        """
        Gets the base URL of the client.

        :return: The base URL as an `httpx.URL` object.
        """
        return self._base_url

    @base_url.setter
    def base_url(self, url: URL | str | None) -> None:
        """
        Sets the base URL of the client, ensuring it ends with a trailing slash.

        :param url: The new base URL, as a string or `httpx.URL` object.
        """
        self._base_url = self._enforce_trailing_slash(url if isinstance(url, URL) else URL(url)) if url else None


class SyncHttpxClientWrapper(httpx.Client):
    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass


class SyncAPIClient(BaseClient[httpx.Client]):
    """
    Synchronous client for making HTTP requests with httpx.
    """

    _client: httpx.Client

    def __init__(
        self,
        *,
        version: str,
        base_url: Union[str, URL],
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initializes the SyncAPIClient with version, base_url, and timeout.

        :param version: The version of the client.
        :param base_url: The base URL for the API endpoints.
        :param timeout: The timeout for the HTTP requests.
        :param http_client: An optional httpx.Client instance.
        """
        if not is_given(timeout):
            # if the user passed in a custom http client with a non-default
            # timeout set then we use that timeout.
            #
            # note: there is an edge case here where the user passes in a client
            # where they've explicitly set the timeout to match the default timeout
            # as this check is structural, meaning that we'll think they didn't
            # pass in a timeout and will ignore it
            if http_client and http_client.timeout != HTTPX_DEFAULT_TIMEOUT:
                timeout = http_client.timeout
            else:
                timeout = DEFAULT_TIMEOUT
        
        if http_client is not None and not isinstance(http_client, httpx.Client):
            raise TypeError(
                f"Invalid `http_client` argument; Expected an instance of `httpx.Client` but got {type(http_client)}"
            )

        super().__init__(
            version=version,
            base_url=base_url,
            timeout=timeout,
            custom_headers=custom_headers,
        )
        self._client = http_client or SyncHttpxClientWrapper(base_url=base_url, timeout=timeout)

    def is_closed(self) -> bool:
        """
        Checks if the underlying HTTPX client is closed.

        :return: True if the client is closed, False otherwise.
        """
        return self._client.is_closed

    def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        # If an error is thrown while constructing a client, self._client
        # may not be present
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self) -> "SyncAPIClient":
        """
        Enter the runtime context related to this object.

        This method is used to initialize resources needed for the client instance.
        It enables the use of the `with` statement with the client, ensuring that resources are properly managed.

        :return: The current instance of the SyncAPIClient.
        :rtype: SyncAPIClient
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Exit the runtime context related to this object.

        This method is used to clean up resources. It is called when exiting the `with` statement block.
        It closes the HTTP session and can handle any exceptions that occurred within the block.

        :param exc_type: The type of the exception raised, if any.
        :param exc_val: The value of the exception raised, if any.
        :param exc_tb: The traceback of the exception, if any.
        """
        self.close()

    def request(
        self,
        options: FinalRequestOptions,
    ) -> httpx.Response:
        """
        Sends an HTTP request with the given options.

        :param options: The request options.
        :return: The HTTP response.
        """
        request = self._build_request(options)
        log.debug(
            "Sending HTTP Request: %s %s %s",
            request.method,
            request.headers,
            request.url,
        )
        try:
            response = self._client.send(request)
        except httpx.TimeoutException as err:
            log.debug("Raising timeout error")
            raise APITimeoutError(request=request) from err
        except Exception as err:
            log.debug("Encountered Exception", exc_info=True)
            log.debug("Raising connection error")
            raise APIConnectionError(request=request) from err

        log.debug(
            'HTTP Response: %s %s "%i %s" %s',
            request.method,
            request.url,
            response.status_code,
            response.reason_phrase,
            response.headers,
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:  # thrown on 4xx and 5xx status code
            log.debug("Encountered httpx.HTTPStatusError", exc_info=True)

            # If the response is streamed then we need to explicitly read the response
            # to completion before attempting to access the response text.
            if not err.response.is_closed:
                err.response.read()

            log.debug("Re-raising status error")
            raise self._make_status_error_from_response(err.response) from None

        if response.status_code == 200:
            body = response.json()
            if body.get("status") == "ERRO":
                raise self._make_status_error_from_response(response)
            
        log.debug(
            'HTTP Response body: %s',
            response.json(),
        )

        return response

    def get(
        self,
        path: str,
        *,
        params: RequestParams = {},
    ) -> Response:
        """
        Send a GET request to the specified URL.

        :param path: The path of the URL to send the request to.
        :param params: (optional) The query parameters to send with the request.
        :param headers: (optional) The headers to send with the request.
        :return: The response object of the GET request.
        """
        log.debug("GET params: %s", params)
        opts = FinalRequestOptions(method="GET", url=path, params=params)
        return self.request(opts)
