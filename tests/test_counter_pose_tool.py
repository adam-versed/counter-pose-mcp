"""Test the Counter-Pose MCP Server."""

import json
import sys
from unittest.mock import MagicMock

# Mock FastMCP for testing
sys.modules["fastmcp"] = MagicMock()

# Import after mocking
from src.mcp_server.counter_pose_tool import CounterPoseTool


def test_counter_pose_tool():
    """Test the basic functionality of the CounterPoseTool."""
    tool = CounterPoseTool()
    
    # Test domain detection
    query = "How should I design my software architecture for scalability?"
    domain = tool._determine_domain(query)
    print(f"Detected domain for '{query}': {domain}")
    assert domain == "software_development"
    
    # Test persona selection
    personas = tool._select_persona_pair(domain)
    print(f"Selected personas for {domain}: {personas[0]} and {personas[1]}")
    assert len(personas) == 2
    
    # Test simple query processing (without showing process)
    result = tool.process_query(query, show_full_process=False)
    print(f"Simple result: {json.dumps(result, indent=2)}")
    assert "synthesis" in result
    
    # Test detailed query processing (with full process)
    result = tool.process_query(query, show_full_process=True)
    print(f"Detailed result: {json.dumps(result, indent=2)}")
    assert "domain" in result
    assert "personas" in result
    assert "first_perspective" in result
    assert "critique" in result
    assert "synthesis" in result
    
    print("All tests passed!")


if __name__ == "__main__":
    test_counter_pose_tool()
