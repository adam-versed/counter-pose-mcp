"""Main entry point for the Counter-Pose MCP Server."""

from fastmcp import FastMCP
from .counter_pose_tool import CounterPoseTool

# Create an instance of the CounterPoseTool
counter_pose = CounterPoseTool()

# Name the FastMCP instance 'mcp' to make it discoverable by the CLI
mcp = FastMCP(
    title="Counter-Pose MCP Server",
    description="An MCP server implementing the RPT (Reasoning-through-Perspective-Transition) technique",
)


@mcp.tool()
def counter_pose(query: str, show_full_process: bool = False) -> dict:
    """Process a query using the Counter-Pose RPT technique.
    
    The Counter-Pose tool implements the Reasoning-through-Perspective-Transition (RPT) prompting
    technique that improves AI responses by introducing deliberate perspective conflict.
    
    Args:
        query: The question or problem to analyze from multiple perspectives
        show_full_process: Whether to show the detailed debate process (default: False)
        
    Returns:
        A dictionary containing either just the synthesized answer (default) or the full
        process including each persona's perspective and the final synthesis.
    """
    return counter_pose.process_query(query, show_full_process)


@mcp.tool()
def get_counter_pose_domains() -> dict:
    """Get the available domains and their keywords.
    
    Returns:
        A dictionary mapping domain names to their associated keywords
    """
    return counter_pose.domain_keywords


@mcp.tool()
def get_counter_pose_personas() -> dict:
    """Get the available persona pairs for each domain.
    
    Returns:
        A dictionary mapping domain names to lists of persona pairs
    """
    return counter_pose.persona_pairs


@mcp.tool()
def get_counter_pose_templates() -> dict:
    """Get example templates for using the Counter-Pose tool.
    
    Returns:
        A dictionary of example use cases with sample queries and outputs
    """
    return counter_pose.get_example_templates()


def main() -> None:
    """Run the FastMCP application."""
    mcp.run()


if __name__ == "__main__":
    main()
