#!/bin/bash

# Test client for the Counter-Pose MCP Reasoning Validator

echo "Testing the Counter-Pose MCP Reasoning Validator"
echo "==============================================="

# Test the validate_reasoning tool with a software development example
echo -e "\nExample 1: Software Development Reasoning"
echo '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "callTool",
  "params": {
    "name": "validate_reasoning",
    "arguments": {
      "reasoning": "I need to implement authentication for our web application. I think we should use JWT tokens since they are stateless and work well with modern frontend frameworks. We can set the expiration time to 24 hours and store the tokens in local storage. This approach will be easy to implement and maintain."
    }
  }
}' | nc -U /tmp/mcp.sock

# Test with a digital marketing example
echo -e "\nExample 2: Digital Marketing Reasoning"
echo '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "callTool",
  "params": {
    "name": "validate_reasoning",
    "arguments": {
      "reasoning": "For our upcoming product launch, I plan to focus heavily on social media marketing. We'll create engaging content across Instagram, Twitter, and TikTok, featuring influencer partnerships. Our messaging will emphasize the innovative features and lifestyle benefits of the product."
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
    "name": "get_domains",
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
    "name": "get_templates",
    "arguments": {}
  }
}' | nc -U /tmp/mcp.sock
