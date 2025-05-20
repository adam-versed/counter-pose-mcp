"""Main entry point for the Counter-Pose MCP Server."""

from fastmcp import FastMCP
from .counter_pose_tool import CounterPoseTool

# Create an instance of the CounterPoseTool
counter_pose = CounterPoseTool()

# Name the FastMCP instance 'mcp' to make it discoverable by the CLI
mcp = FastMCP(
    title="Counter-Pose MCP Server",
    description="An MCP server implementing the RPT (Reasoning-through-Perspective-Transition) technique for validating LLM reasoning",
)


@mcp.tool()
def validate_reasoning(reasoning: str) -> dict:
    """Validate an LLM's reasoning process using the Counter-Pose RPT technique.
    
    The Counter-Pose tool implements the Reasoning-through-Perspective-Transition (RPT) technique
    to critique and validate reasoning by examining it from multiple domain-specific perspectives.
    It identifies blind spots, potential contradictions, and provides feedback on whether the
    reasoning should be adjusted.
    
    Args:
        reasoning: The LLM's thought process or reasoning to validate
        
    Returns:
        A dictionary containing domain information, persona-based critiques, and a synthesis
        of feedback including confidence assessment and recommended changes.
    """
    return counter_pose.validate_reasoning(reasoning)


@mcp.tool()
def get_domains() -> dict:
    """Get the available domains and their keywords.
    
    Returns:
        A dictionary mapping domain names to their associated keywords
    """
    return counter_pose.domain_keywords


@mcp.tool()
def get_personas() -> dict:
    """Get the available persona pairs for each domain.
    
    Returns:
        A dictionary mapping domain names to lists of persona pairs
    """
    return counter_pose.persona_pairs


@mcp.tool()
def get_templates() -> dict:
    """Get example templates for reasoning validation.
    
    Returns:
        A dictionary of example reasoning scenarios with sample outputs
    """
    return counter_pose.get_example_templates()


def main() -> None:
    """Run the FastMCP application."""
    mcp.run()


if __name__ == "__main__":
    main()
