# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
# Initial setup (installs dependencies and configures environment)
./setup.sh

# Run MCP server
./run_server.sh

# Test server functionality
./test_client.sh
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run individual test files
python tests/test_domain_detection.py
python tests/test_session_flow.py
python tests/test_persona_selection.py
python tests/test_error_handling.py

# Test server directly
python test_server.py
```

### Code Quality
```bash
# Format code
black src/ tests/ --line-length 100

# Sort imports
isort src/ tests/ --profile black --line-length 100

# Type checking
mypy src/

# Linting
ruff check src/ tests/
```

## Architecture Overview

This is an MCP (Model Context Protocol) server that implements the RPT (Reasoning-through-Perspective-Transition) technique for AI reasoning validation. The system provides a session-based validation workflow with automatic domain detection and intelligent persona selection.

### Core Components

**Main MCP Server** (`src/mcp_server/main.py`):
- FastMCP-based server with 3 tools: `submit_reasoning`, `get_persona_guidance`, `submit_critique`
- Entry point for MCP protocol communication

**Counter-Pose Engine** (`src/mcp_server/counter_pose_tool.py`):
- `CounterPoseTool`: Main validation logic with domain detection, persona ranking, and session management
- `CounterPoseSession`: Session state management following Sequential Thinking model
- `UsageLogger`: Usage tracking and analytics

### Domain System

The system supports 4 domains with specialized persona pairs:
- **Software Development**: Developer/Security Expert, Frontend/UX, Backend/DevOps, Performance/Maintainability
- **Digital Marketing**: Creative/Analytics, Brand/Conversion, Social/Growth, Content/Performance, B2B/B2C, Landing/SEO
- **Visual Design**: Minimalist/Feature-Rich, Brand/User-Centered, Print/Digital, Artistic/Data-Driven, Accessibility/Visual
- **Product Strategy**: Customer/Business, Innovation/Research, MVP/Quality, Long-term/Quick, Technical PM/Business PM

**Domain Detection**: Automatic keyword-based analysis determines the most relevant domain from reasoning content.

**Persona Ranking**: Within each domain, persona pairs are ranked by keyword relevance to provide intelligent recommendations.

### Session Flow

1. **Submit Reasoning**: Submit reasoning for analysis, get domain detection and ranked persona recommendations
2. **Get Guidance**: Receive persona-specific guidance on how to perform critique  
3. **Submit Critique**: Submit critiques from both personas using explicit parameters and receive synthesis format guidance

Sessions maintain state across the multi-step validation process and provide structured output with confidence assessment, blind spots, contradictions, and actionable recommendations.

## Development Notes

- Uses FastMCP framework for MCP protocol implementation
- Session-based state management prevents mixing validation contexts
- Intelligent keyword matching for both domain detection and persona selection
- Type hints throughout with Pyright configuration for type checking
- Test suite covers domain detection, session flow, persona selection, and error handling

## Configuration

- Python 3.8+ required
- Virtual environment managed by setup script
- Type checking configured via `pyrightconfig.json`
- Code formatting: Black (100 char line length)
- Import sorting: isort with Black profile
- Linting: Ruff with specific rule selection