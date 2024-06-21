
# MK Solutions Client Library

MK Solutions Client Library is a Python package that provides an easy-to-use client for interacting with the MK Solutions API. The library supports both synchronous and asynchronous requests using `httpx`.

## Features

- Synchronous and asynchronous API clients
- Modular and organized structure
- Support for client, contract, and connection operations
- Extensible and maintainable codebase

## Installation

You can install the package using `pip`:

```bash
pip install mksolutions
```

## Usage

### Synchronous Client

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
    token=os.environ.get("MKS_TOKEN"),
    ws_password=os.environ.get("MKS_WS_PASSWORD"),
    service_id=os.environ.get("MKS_SERVICE_ID"),
)

# Find a client by their document (CPF/CNPJ)
clients = mks.clients.find_by_doc('12345678901')

for client in clients:
    print(client.name)

    # Access contracts and connections of the client
    print(f"Client {client.name} has {len(client.contracts)} contracts and {len(client.connections)} connections.")

    # Iterate through and print details of each contract
    for contract in client.contracts:
        print(f"Contract ID: {contract.id}, Status: {contract.status}")

    # Iterate through and print details of each connection
    for connection in client.connections:
        print(f"Connection ID: {connection.id}, Status: {connection.status}")

```

### Asynchronous Client

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
    token=os.environ.get("MKS_TOKEN"),
    ws_password=os.environ.get("MKS_WS_PASSWORD"),
    service_id=os.environ.get("MKS_SERVICE_ID"),
)

async def main():
    # Find a client by their document (CPF/CNPJ)
    client = await mks.clients.find_by_doc('12345678901')
    print(client.name)

    # Access contracts and connections of the client
    print(f"Client {client.name} has {len(client.contracts)} contracts and {len(client.connections)} connections.")

    # Iterate through and print details of each contract
    for contract in client.contracts:
        print(f"Contract ID: {contract.id}, Status: {contract.status}")

    # Iterate through and print details of each connection
    for connection in client.connections:
        print(f"Connection ID: {connection.id}, Status: {connection.status}")

# Run the main coroutine
asyncio.run(main())

```

## Project Structure

```
mksolutions/
├── __init__.py
├── _base_client.py
├── _client.py
├── resources/
│   ├── __init__.py
│   ├── clients.py
│   ├── contracts.py
│   ├── connections.py
├── schemas.py
├── utils.py
tests/
├── __init__.py
├── test_client.py
├── resources/
│   ├── __init__.py
│   ├── test_clients.py
│   ├── test_contracts.py
│   ├── test_connections.py
README.md
requirements.txt
.gitignore
setup.py
```

## Running Tests

To run the tests, you need to install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Then, you can use `pytest` to run the tests:

```bash
pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Convenção de Commits

- **perf**: Melhorias de performance.
- **style**: Alterações que não afetam a lógica (formatação, ponto e vírgula, etc.).
- **build**: Mudanças que afetam o sistema de build ou dependências externas.
- **chore**: Tarefas menores que não mudam a lógica.
- **ci**: Mudanças nos arquivos de configuração e scripts de CI.
- **feat**: Adição de novas funcionalidades.
- **wip**: Trabalho em progresso.
- **fix**: Correção de bugs.
- **refactor**: Alterações de código que não corrigem bugs nem adicionam funcionalidades.
- **test**: Adição ou modificação de testes.
- **docs**: Adição ou modificação de documentação.

## License

This project is licensed under the MIT License.
