
# MK Solutions Python API Library
[![PyPI version](https://img.shields.io/pypi/v/openai.svg)](https://pypi.org/project/openai/)

The MK Solutions Python library provides convenient access to the MK Solutions RPC API from any Python 3.8+
application. The library includes type definitions for all request parameters and response fields,
and offers synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

This project is generated from the [OpenAPI specification](https://github.com/DevDeividMoura/mksolutions-api-py/tree/main/mks-api-spec) located in the `mks-api-spec` directory, which was voluntarily created and submitted by [Deivid Carvalho Moura](contato@dmsolucoesemti.com.br).

## Documentation

The RPC API documentation can be found on [Atlassian Docs](https://mkloud.atlassian.net/wiki/spaces/MK30/pages/48699908/APIs+gerais). The full API of this library can be found in [api.md](api.md).

### Installation

You can install the package using `pip`:

```sh
# install from PyPI
pip install mksolutions
```
### Usage

The full API of this library can be found in [api.md](api.md).

```python
import os
from mksolutions import MKSolutions

# Initialize MKSolutions client with environment variables
mks = MKSolutions(
    # This is the default and can be omitted
    # Required
    base_url=os.environ.get("MKS_BASE_URL"),
    # For authenticated calls
    api_key=os.environ.get("MKS_API_KEY"),
    # For specific authorizations
    username=os.environ.get("MKS_USERNAME"),
    password=os.environ.get("MKS_PASSWORD"),
    # For general authorizations
    user_token=os.environ.get("MKS_USER_TOKEN"),
    ws_password=os.environ.get("MKS_WS_PASSWORD"),
    service_id=os.environ.get("MKS_SERVICE_ID"),
    # Defines the type of authentication used,
    # whether general or specific
    auth_type="gerenal",
)

# Find clients by their document (CPF/CNPJ)
result = mks.clients.find_by_doc("12345678901")

print(f"Client ID: {result.id}, Client Name: {result.name}")

for client in result.others:
    print(f"Client ID: {client.id}, Client Name: {client.name}")
```
While you can provide the keyword arguments `base_url`, `api_key`, `username`, `password`, `user_token` and `ws_password`  directly, we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/). This allows you to add variables like `MKS_BASE_URL="My base url"`, `MKS_API_KEY="My API key"`, `MKS_USERNAME="My username"`, `MKS_PASSWORD="My password"`, `MKS_USER_TOKEN="My User token"` and `MKS_WS_PASSWORD="My Web Services password"` to your `.env` file, ensuring that sensitive information is not stored in source control.

### Authentication

The `MKSolutions` client supports multiple methods of authentication. While you can provide the `api_key` directly, if it is not passed, the client can automatically configure static authentication based on the specified `auth_type`. 

If `auth_type` is set to `"general"`, the client will use the `user_token`, `ws_password`, and `service_id` for general service authentication. If `auth_type` is set to `"specific"`, the client will use the `username` and `password` for specific service authentication. If any required parameters are missing, an appropriate error will be raised.

## Async usage

Simply import `AsyncMKSolutions` instead of `MKSolutions` and use `await` with each API call:

```python
import os
import asyncio
from mksolutions import AsyncMKSolutions

# Initialize AsyncMKSolutions client with environment variables
mks = AsyncMKSolutions(
    # This is the default and can be omitted
    # Required
    base_url=os.environ.get("MKS_BASE_URL"),
    # For authenticated calls
    api_key=os.environ.get("MKS_API_KEY"),
    # For specific authorizations
    username=os.environ.get("MKS_USERNAME"),
    password=os.environ.get("MKS_PASSWORD"),
    # For general authorizations
    user_token=os.environ.get("MKS_USER_TOKEN"),
    ws_password=os.environ.get("MKS_WS_PASSWORD"),
    service_id=os.environ.get("MKS_SERVICE_ID"),
    # Defines the type of authentication used,
    # whether general or specific
    auth_type="gerenal",
)


async def main():
    # Find clients by their document (CPF/CNPJ)
    result = await mks.clients.find_by_doc("12345678901")

    print(f"Client ID: {result.id}, Client Name: {result.name}")

    for client in result.others:
        print(f"Client ID: {client.id}, Client Name: {client.name}")


# Run the main coroutine
asyncio.run(main())
```
Functionality between the synchronous and asynchronous clients is otherwise identical.

## Using types

 Nested request parameters are [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict).
 Responses are [Pydantic models](https://docs.pydantic.dev) which also provide helper methods for things like:

- Serializing back into JSON, `model.to_json()`
- Converting to a dictionary, `model.to_dict()`

Typed requests and responses provide autocomplete and documentation within your editor. If you would like to see type errors in VS Code to help catch bugs earlier, set `python.analysis.typeCheckingMode` to `basic`.

## Handling errors

When the library is unable to connect to the API (for example, due to network connection issues or timeouts), a subclass of `mksolutions.APIConnectionError` is raised.

When the API returns a failure status code (i.e. 200 with status="ERROR" or 5xx
response), a subclass of `mksolutions.APIStatusError` is generated, containing `status_code` and `response` properties.

All errors inherit from `mksolutions.APIError`.

```python
import mksolutions
from mksolutions import MKSolutions

mks = MKSolutions()

try:
    clients = mks.clients.find_by_doc("12345678901")
except mksolutions.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except mksolutions.ResultNotFoundError as e:
    print(
        'I received a status code 200 with body["status"]= Error and body["Num. ERRO"] = 003. Indicates that there are no results for the search'
    )
except mksolutions.InvalidDocumentError as e:
    print(
        'I received a status code 200 with body["status"]= Error and body["Num. ERRO"] = 002. Indicates that the parameter was not validated'
    )
    print(e.status_code)
    print(e.response)
```
Error codes are as followed:

| Status Code | Num. ERRO | Error Type                 |
| ----------- | --------- | -------------------------- |
| >=500       | N/A       | `InternalServerError`      |
| N/A         | N/A       | `APIConnectionError`       |
| 200         | 001       | `TokenInvalidError`        |
| 200         | 002       | `InvalidFormatError`       |
| 200         | 003       | `ResultNotFoundError`      |
| 200         | 999       | `TokenExpiredError`        |
| 200         | 999       | `TokenNotFoundError`       |

## Advanced

### Logging

We use the standard library [`logging`](https://docs.python.org/3/library/logging.html) module.

You can enable logging by setting the environment variable `MKS_LOG` to `debug`.

```shell
$ export MKS_LOG=debug
```
You can also set the MKS_LOG_PATH environment variable to specify a file path for saving the logs to a file.

```shell
$ export MKS_LOG_PATH=/path/to/mksolutions.log
```
### Making custom/undocumented requests

This library is typed for convenient access to the documented API.

If you need to access undocumented endpoints, params, or response properties, the library can still be used.

#### Undocumented endpoints

To make requests to undocumented endpoints, you can make requests using `mks.get`, `mks.post`, and other
http verbs. Options on the client will be respected (such as retries) will be respected when making this
request.

```py
from mksolutions import MKSolutions

mks = MKSolutions()

response = mks.get(
    "/mk/FazerAlgumaCoisa.rule?",
    params={
        "sys":"MK0",
        "token": mks.api_key,
        "param": True
    },
)

print(response.json())
```
## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backwards-incompatible changes may be released as minor versions:

1. Changes that only affect static types, without breaking runtime behavior.
2. Changes to library internals which are technically public but not intended or documented for external use. _(Please open a GitHub issue to let us know if you are relying on such internals)_.
3. Changes that we do not expect to impact the vast majority of users in practice.

We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.

We are keen for your feedback; please open an [issue](https://github.com/DevDeividMoura/mksolutions-api-py/issues) with questions, bugs, or suggestions.

## Requirements

Python 3.8 or higher.