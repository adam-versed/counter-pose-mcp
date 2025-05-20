#!/bin/bash
# Run the Counter-Pose MCP Server

# Activate virtual environment
source .venv/bin/activate

# Run the server using uvicorn
echo "Starting Counter-Pose MCP Server..."
python -m src.mcp_server.main

# Alternatively, if you're using an MCP framework:
# fastmcp run src.mcp_server.main:mcp
