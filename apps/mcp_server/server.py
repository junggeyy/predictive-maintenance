from mcp import MCPServer
from tools import TOOLS

server = MCPServer(
    "predictive-maintenance-tools",
    tools=TOOLS
)

if __name__ == "__main__":
    server.run()
