"""
MCP Server for Predictive Maintenance System

This server provides LLM tools to query machine status from the predictive maintenance backend.
Users can connect their LLM to this server and ask questions like:
- "What is the status of machine 42?"
- "Is machine 15 in good condition?"
- "Tell me about machine 7"
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from tools import get_machine_status
import mcp.types as types
import asyncio
import sys

app = Server("predictive-maintenance")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools for the LLM"""
    return [
        types.Tool(
            name="get_machine_status",
            description="Get the current status, health, and prediction results for a specific machine. "
                       "Returns failure probability, remaining useful life (RUL) in hours, machine age in years, sensor values, and engineered features. ",
            inputSchema={
                "type": "object",
                "properties": {
                    "machine_id": {
                        "type": "integer",
                        "description": "The ID of the machine to query (1-100)"
                    }
                },
                "required": ["machine_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Execute tool calls from the LLM"""
    if name == "get_machine_status":
        machine_id = arguments.get("machine_id")
        result = get_machine_status(machine_id)
        
        import json
        response_text = json.dumps(result, indent=2)
        
        return [
            types.TextContent(
                type="text",
                text=response_text
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the MCP server"""
    print("MCP server is listening...", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped", file=sys.stderr)
        sys.exit(0)
