"""Main entry point for the Counter-Pose MCP Server."""

import uuid
from typing import List, Optional

from fastmcp import FastMCP

from .counter_pose_tool import CounterPoseTool

# Create an instance of the CounterPoseTool
counter_pose = CounterPoseTool()

# Name the FastMCP instance 'mcp' to make it discoverable by the CLI
mcp = FastMCP(
    title="Counter-Pose MCP Server",
    description=(
        "An MCP server implementing the RPT (Reasoning-through-Perspective-Transition) "
        "technique for structured reasoning validation"
    ),
)


@mcp.tool()
def init_counter_pose(reasoning: str, session_id: Optional[str] = None) -> dict:
    """Initialize a Counter-Pose RPT reasoning session.

    The Counter-Pose tool implements the Reasoning-through-Perspective-Transition (RPT) technique
    to improve reasoning by examining it from multiple domain-specific perspectives.

    This is step 1 of a 2-step initialization process:
    1. init_counter_pose - Returns ranked persona pair options based on reasoning content
    2. select_personas - Choose which persona pair to use for critique

    Args:
        reasoning: The initial reasoning to analyze
        session_id: Optional custom session ID (will be generated if not provided)

    Returns:
        A session object with domain detection, ranked persona options, and next step instructions.
    """
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    return counter_pose.init_session(session_id, reasoning)


@mcp.tool()
def select_personas(session_id: str, persona_pair: List[str]) -> dict:
    """Select personas for a Counter-Pose session.

    Args:
        session_id: The session ID from init_counter_pose
        persona_pair: List of exactly 2 persona names to use for critique

    Returns:
        Session information with next steps for critique submission
    """
    return counter_pose.select_personas(session_id, persona_pair)


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


def main() -> None:
    """Run the FastMCP application."""
    mcp.run()


if __name__ == "__main__":
    main()
