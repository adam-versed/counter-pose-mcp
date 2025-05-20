#!/bin/bash

# Simple test client for the Counter-Pose MCP Server

echo "Testing the Counter-Pose MCP Server"
echo "===================================="

# Test the counter_pose tool with a simple query
echo -e "\nExample 1: Simple query (synthesis only)"
echo '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "callTool",
  "params": {
    "name": "counter_pose",
    "arguments": {
      "query": "How should I implement authentication in my web app?",
      "show_full_process": false
    }
  }
}' | nc -U /tmp/mcp.sock

# Test the counter_pose tool with a more detailed query
echo -e "\nExample 2: Detailed query (full process)"
echo '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "callTool",
  "params": {
    "name": "counter_pose",
    "arguments": {
      "query": "Should I focus on SEO or paid ads for my new SaaS product?",
      "show_full_process": true
    }
  }
}' | nc -U /tmp/mcp.sock

# Get available domains
echo -e "\nExample 3: Get available domains"
echo '{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "callTool",
  "params": {
    "name": "get_counter_pose_domains",
    "arguments": {}
  }
}' | nc -U /tmp/mcp.sock

# Get example templates
echo -e "\nExample 4: Get example templates"
echo '{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "callTool",
  "params": {
    "name": "get_counter_pose_templates",
    "arguments": {}
  }
}' | nc -U /tmp/mcp.sock
