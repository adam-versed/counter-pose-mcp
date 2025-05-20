"""Main entry point for the Counter-Pose MCP Server."""

from fastmcp import FastMCP
from .counter_pose_tool import CounterPoseTool
import uuid

# Create an instance of the CounterPoseTool
counter_pose = CounterPoseTool()

# Name the FastMCP instance 'mcp' to make it discoverable by the CLI
mcp = FastMCP(
    title="Counter-Pose MCP Server",
    description="An MCP server implementing the RPT (Reasoning-through-Perspective-Transition) technique for structured reasoning validation",
)


@mcp.tool()
def init_counter_pose(reasoning: str, session_id: str = None) -> dict:
    """Initialize a Counter-Pose RPT reasoning session.
    
    The Counter-Pose tool implements the Reasoning-through-Perspective-Transition (RPT) technique
    to improve reasoning by examining it from multiple domain-specific perspectives.
    
    Args:
        reasoning: The initial reasoning to analyze
        session_id: Optional custom session ID (will be generated if not provided)
        
    Returns:
        A session object with information about the domain, selected personas, and next steps.
    """
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())
    
    return counter_pose.init_session(session_id, reasoning)


@mcp.tool()
def submit_critique(session_id: str, persona: str, critique: str) -> dict:
    """Submit a critique from a specific persona's perspective.
    
    Args:
        session_id: The session ID from init_counter_pose
        persona: The persona providing the critique
        critique: The critique content
        
    Returns:
        Updated session information with next steps
    """
    return counter_pose.submit_critique(session_id, persona, critique)


@mcp.tool()
def submit_synthesis(session_id: str, synthesis: str) -> dict:
    """Submit the final synthesis for a Counter-Pose session.
    
    Args:
        session_id: The session ID from init_counter_pose
        synthesis: The synthesized conclusion
        
    Returns:
        Session summary with metadata
    """
    return counter_pose.submit_synthesis(session_id, synthesis)


@mcp.tool()
def get_session(session_id: str) -> dict:
    """Get information about a Counter-Pose session.
    
    Args:
        session_id: The session ID to retrieve
        
    Returns:
        Complete session information and history
    """
    return counter_pose.get_session(session_id)


@mcp.tool()
def get_domains() -> dict:
    """Get the available domains and their keywords.
    
    Returns:
        A dictionary mapping domain names to their associated keywords
    """
    return counter_pose.get_domains()


@mcp.tool()
def get_personas() -> dict:
    """Get the available persona pairs for each domain.
    
    Returns:
        A dictionary mapping domain names to lists of persona pairs
    """
    return counter_pose.get_personas()


@mcp.tool()
def get_templates() -> dict:
    """Get example templates for Counter-Pose reasoning validation.
    
    Returns:
        A dictionary of example reasoning scenarios with sample critiques
    """
    return counter_pose.get_example_templates()


def main() -> None:
    """Run the FastMCP application."""
    mcp.run()


if __name__ == "__main__":
    main()
