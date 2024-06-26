# Clients

Types:

```python
from mksolutions.types import ClientByDoc, ClientByDocResponse
```

Methods:

- <code title="get /mk/WSMKConsultaDoc.rule">client.clients.<a href="./src/mksolutions/resources/clients.py">find_by_doc</a>(\*\*<a href="./src/mksolutions/types/clients_find_by_doc_params.py">params</a>) -> <a href="./src/mksolutions/types/clients_by_doc_response.py">ClientByDocResponse</a> | <a href="./src/mksolutions/types/clients_by_doc.py">List[ClientByDoc]</a></code>

# Connections

Types:

```python
from mksolutions.types import ConnectionByClientID, ConnectionsByClientIDResponse
```

Methods:

- <code title="get /mk/WSMKConexoesPorCliente.rule">client.connections.<a href="./src/mksolutions/resources/connections.py">find_by_client_id</a>(\*\*<a href="./src/mksolutions/types/connections_find_by_client_id_params.py">params</a>) -> <a href="./src/mksolutions/types/connections_by_client_id_response.py">ConnectionsByClientIDResponse</a> | <a href="./src/mksolutions/types/connections_by_client_id.py">List[ConnectionByClientID]</a></code>

- <code title="get /mk/WSMKConsultaDoc.rule">client.connections.<a href="./src/mksolutions/resources/connections.py">find_by_client_doc</a>(client_doc) -> <a href="./src/mksolutions/types/connections_by_client_id.py">List[ConnectionByClientID]</a></code>
