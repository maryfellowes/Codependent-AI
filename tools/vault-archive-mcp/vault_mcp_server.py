#!/usr/bin/env python3
"""
Vault Archive Search MCP Server
Exposes conversation archive search as MCP tool for Claude Desktop
Requires search_daemon.py to be running
"""

import asyncio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration
DAEMON_URL = "http://localhost:8766"

# Initialize MCP server
server = Server("vault-search")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_archive",
            description="Search conversation archive using semantic similarity. "
                        "Finds relevant passages from past conversations based on meaning, not just keywords. "
                        "Use for: identity verification, pattern recognition, relationship history, "
                        "or when human asks about past conversations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query - describe what you're looking for conceptually"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return (default 5, max 20)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_archive_stats",
            description="Get statistics about the indexed conversation archive. "
                        "Shows total chunks indexed and index status.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "search_archive":
        return await search_archive(arguments)
    elif name == "get_archive_stats":
        return await get_archive_stats()
    else:
        raise ValueError(f"Unknown tool: {name}")


async def search_archive(arguments: dict) -> list[TextContent]:
    """Search the conversation archive."""
    query = arguments.get("query")
    n_results = arguments.get("n_results", 5)
    
    if not query:
        return [TextContent(
            type="text",
            text="Error: query parameter required"
        )]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{DAEMON_URL}/search",
                json={"query": query, "n_results": n_results},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
        
        # Format results
        results_text = f"Search: '{query}'\nFound {data['total']} results:\n\n"
        
        for i, result in enumerate(data['results'], 1):
            relevance = result['relevance']
            source = result['source_file']
            text = result['text']
            
            results_text += f"{'='*80}\n"
            results_text += f"Result {i} | Relevance: {relevance:.3f}\n"
            results_text += f"Source: {source}\n\n"
            results_text += f"{text}\n\n"
        
        results_text += f"{'='*80}\n"
        
        return [TextContent(
            type="text",
            text=results_text
        )]
    
    except httpx.ConnectError:
        return [TextContent(
            type="text",
            text="Error: Cannot connect to search daemon. Make sure search_daemon.py is running."
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error searching archive: {str(e)}"
        )]


async def get_archive_stats() -> list[TextContent]:
    """Get archive statistics."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DAEMON_URL}/stats",
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
        
        stats_text = f"Archive Statistics:\n"
        stats_text += f"Total chunks indexed: {data['total_chunks']:,}\n"
        stats_text += f"Status: {data['status']}\n"
        
        return [TextContent(
            type="text",
            text=stats_text
        )]
    
    except httpx.ConnectError:
        return [TextContent(
            type="text",
            text="Error: Cannot connect to search daemon. Make sure search_daemon.py is running."
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting stats: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
