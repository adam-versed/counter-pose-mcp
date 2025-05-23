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
def submit_reasoning(reasoning: str, session_id: Optional[str] = None) -> dict:
    """Submit reasoning for Counter-Pose RPT analysis.

    The Counter-Pose tool implements the Reasoning-through-Perspective-Transition (RPT) technique
    to improve reasoning by examining it from multiple domain-specific perspectives.

    This is step 1 of a 3-step analysis process:
    1. submit_reasoning - Submit reasoning and get ranked persona pair options
    2. get_persona_guidance - Get guidance on how to perform critique for selected personas
    3. submit_critique - Submit critiques from both personas and receive synthesis guidance

    Args:
        reasoning: The initial reasoning to analyze
        session_id: Optional custom session ID (will be generated if not provided)

    Returns:
        A session object with domain detection, ranked persona options, and next step instructions.
    """
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    return counter_pose.submit_reasoning(session_id, reasoning)


@mcp.tool()
def get_persona_guidance(session_id: str, persona_pair: List[str]) -> dict:
    """Get guidance for performing critique with selected personas.

    Args:
        session_id: The session ID from submit_reasoning
        persona_pair: List of exactly 2 persona names to use for critique

    Returns:
        Guidance and formatting instructions for performing critiques with the selected personas
    """
    return counter_pose.get_persona_guidance(session_id, persona_pair)


@mcp.tool()
def submit_critique(
    session_id: str, 
    persona1_name: str, 
    persona1_critique: str, 
    persona2_name: str, 
    persona2_critique: str
) -> dict:
    """Submit critiques from both selected personas.

    This function expects exactly 2 persona critiques as determined by the get_persona_guidance step.
    Both personas must match those selected in the previous step.

    Args:
        session_id: The session ID from submit_reasoning
        persona1_name: Name of the first persona (e.g., "Developer")
        persona1_critique: Critique content from the first persona's perspective
        persona2_name: Name of the second persona (e.g., "Security Expert")
        persona2_critique: Critique content from the second persona's perspective

    Returns:
        Complete analysis with synthesis format guidance for the calling LLM
    """
    return counter_pose.submit_critique(session_id, persona1_name, persona1_critique, persona2_name, persona2_critique)


# complete_analysis function removed - synthesis now handled by submit_critique


def main() -> None:
    """Run the FastMCP application."""
    mcp.run()


if __name__ == "__main__":
    main()
