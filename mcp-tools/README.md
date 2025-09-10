# MCP Tools

Model Context Protocol (MCP) server and client implementations for extending AI capabilities.

## Components

- **MCP Servers**: Custom server implementations
- **MCP Clients**: Client libraries for connecting to MCP servers  
- **Tool Integrations**: Bridge between MCP and various APIs/services
- **Protocol Extensions**: Custom MCP protocol enhancements

## Key Features

- Bidirectional communication with AI models
- Real-time data access and manipulation
- Custom tool registration and discovery
- Secure authentication and authorization
- WebSocket and HTTP transport layers

## Installation

```bash
# From root directory
pip install -e .[mcp-tools]

# Or install individually  
cd mcp-tools && pip install -e .
```

## MCP Servers

### File System Server
Provides secure file system access:
```python
from mcp_tools.servers.filesystem_server import FileSystemServer

server = FileSystemServer(allowed_paths=["/safe/directory"])
server.start()
```

### API Gateway Server  
Proxies API calls with rate limiting:
```python
from mcp_tools.servers.api_gateway_server import APIGatewayServer

server = APIGatewayServer()
server.register_api("weather", "https://api.weather.com")
server.start()
```

## MCP Clients

Connect to MCP servers from your applications:

```python
from mcp_tools.clients.mcp_client import MCPClient

client = MCPClient("ws://localhost:8080")
await client.connect()

# Call server tools
result = await client.call_tool("read_file", {"path": "/data/file.txt"})
```

## Custom Tools

Create reusable MCP tools:

```python
from mcp_tools.base import MCPTool

class DatabaseTool(MCPTool):
    name = "query_database"
    description = "Execute SQL queries safely"
    
    async def execute(self, query: str) -> dict:
        # Implementation here
        pass
```

## Security

- Sandboxed execution environments
- Permission-based access control
- Request validation and sanitization
- Rate limiting and abuse prevention
- Audit logging for all operations