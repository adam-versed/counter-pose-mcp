# Counter-Pose MCP Server Installation Guide

This guide provides instructions for installing and using the Counter-Pose MCP server with Claude Desktop and Cursor IDE.

## Prerequisites

- Python 3.8 or higher
- Git
- Terminal/Command Prompt access

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/counter-pose-mcp.git
cd counter-pose-mcp
```

### Step 2: Run the Setup Script

The setup script will create a virtual environment and install all necessary dependencies:

```bash
chmod +x setup.sh  # Make setup script executable (if needed)
./setup.sh
```

## Integration with Claude Desktop

Claude Desktop can connect to the Counter-Pose MCP server through the Model Context Protocol (MCP).

### Step 1: Start the Counter-Pose MCP Server

In a terminal window, navigate to the counter-pose-mcp directory and run:

```bash
source .venv/bin/activate
./run_server.sh
```

This will start the server on a local Unix socket at `/tmp/mcp.sock`.

### Step 2: Configure Claude Desktop

1. Open Claude Desktop
2. Go to Settings > Extensions
3. Click "Add Custom MCP Server"
4. Enter the following information:
   - Name: Counter-Pose Reasoning Validator
   - Socket Path: `/tmp/mcp.sock`
   - Description: Validates LLM reasoning using multiple perspectives
5. Click "Add Server"

### Step 3: Using Counter-Pose in Claude Desktop

1. Start a new conversation with Claude
2. When you want to validate your reasoning, click on the "Tools" icon
3. Select "Counter-Pose Reasoning Validator" from the tools list
4. Use the "validate_reasoning" function and paste your reasoning in the text field
5. Click "Run" to get Claude's reasoning validated and critiqued from multiple perspectives

## Integration with Cursor IDE

Cursor IDE can integrate with the Counter-Pose MCP server to validate reasoning within your development workflow.

### Step 1: Start the Counter-Pose MCP Server

In a terminal window, navigate to the counter-pose-mcp directory and run:

```bash
source .venv/bin/activate
./run_server.sh
```

### Step 2: Configure Cursor IDE

1. Open Cursor IDE
2. Go to Settings > Extensions > AI
3. Under "Custom Tools/Models", click "Add Custom Tool"
4. Configure the tool:
   - Name: Counter-Pose
   - Tool Type: MCP
   - Connection URL: `/tmp/mcp.sock`
   - Description: Validates reasoning using multiple perspectives
5. Click "Save"

### Step 3: Using Counter-Pose in Cursor IDE

1. Open or create a file in Cursor IDE
2. Use the Command Palette (Cmd/Ctrl+Shift+P)
3. Type "Counter-Pose: Validate Reasoning" 
4. Select your reasoning text in the editor
5. View the validation results in the Cursor AI panel

## Example Usage

Here's an example of using the Counter-Pose reasoning validator:

```json
{
  "reasoning": "I need to implement authentication for our web application. I think we should use JWT tokens since they are stateless and work well with modern frontend frameworks. We can set the expiration time to 24 hours and store the tokens in local storage. This approach will be easy to implement and maintain."
}
```

Response:

```json
{
  "domain": "software_development",
  "personas": ["Developer", "Security Expert"],
  "first_critique": "...",
  "second_critique": "...",
  "synthesis": {
    "query": "How should I implement authentication for our web app?",
    "confidence": "Medium",
    "changes_needed": true,
    "recommendation": "Consider revising your reasoning to address the identified blind spots and potential contradictions.",
    "detailed_feedback": "The reasoning doesn't address potential security vulnerabilities with storing tokens in local storage. Consider using secure, httpOnly cookies instead...",
    "blind_spots_count": 2,
    "contradictions_count": 0
  }
}
```

## Troubleshooting

- **Connection Refused**: Ensure the server is running and the socket path is correct
- **Permission Denied**: Check file permissions for the socket and consider running with elevated permissions
- **Dependency Issues**: Make sure all requirements are installed with `pip install -r requirements.txt`

## Additional Resources

- [Counter-Pose MCP Documentation](https://github.com/yourusername/counter-pose-mcp)
- [Model Context Protocol Specification](https://github.com/anthropics/anthropic-cookbook/tree/main/mcp)
- [Claude Desktop Documentation](https://claude.ai/docs)

## Support

For issues or questions, please open an issue on the GitHub repository or contact support at support@example.com.
