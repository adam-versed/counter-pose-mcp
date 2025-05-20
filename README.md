# Counter-Pose MCP Server: Reasoning Validator

An implementation of the RPT (Reasoning-through-Perspective-Transition) technique as an MCP (Model Context Protocol) server focused on validating and critiquing LLM reasoning.

## About RPT and Reasoning Validation

The RPT (Reasoning-through-Perspective-Transition) technique is a prompting method that improves AI responses by introducing deliberate perspective conflict between different personas. This approach was discovered by Tsinghua University researchers in January 2025 and has shown to reduce inaccuracies by up to 40%.

This implementation adapts RPT to function as a reasoning validator, adding a metacognitive layer to LLM reasoning:

1. A reasoning LLM produces initial thoughts about a query
2. Our Counter-Pose tool analyzes this reasoning through multiple domain-specific perspectives
3. The tool provides critique, identifies blind spots, and validates the reasoning
4. The original LLM can then decide whether to adjust its approach based on this feedback

## How It Works

The Counter-Pose Reasoning Validator works through these steps:

1. **Analysis**: The system analyzes the provided reasoning structure, identifying claims, evidence, and assumptions
2. **Domain Detection**: It determines the appropriate domain (e.g., software development, marketing)
3. **Perspective Critique**: It examines the reasoning from two contrasting domain-specific personas
4. **Blind Spot Identification**: It identifies important considerations missing from the original reasoning
5. **Contradiction Detection**: It identifies potential logical tensions or contradictions
6. **Feedback Synthesis**: It provides an overall assessment of confidence and recommends whether changes are needed

## Available Domains

The server supports the following domains with specialized persona pairs:

- **Software Development**: Developer vs Security Expert, Frontend Engineer vs UX Designer, etc.
- **Digital Marketing**: Creative Director vs Analytics Specialist, Brand Strategist vs Conversion Optimizer, etc.
- **Visual Design**: UI Minimalist vs Feature-Rich Designer, Brand Identity Expert vs User-Centered Designer, etc.
- **Product Strategy**: Customer Advocate vs Business Strategist, Innovative Disruptor vs Market Researcher, etc.

## Usage

### Running the Server

```bash
# Run the server
./run_server.sh

# In another terminal, run a test client
./test_client.sh
```

### Available Tools

The server provides the following tools:

- `validate_reasoning`: Validate an LLM's reasoning process using the Counter-Pose RPT technique
- `get_domains`: Get the available domains and their keywords
- `get_personas`: Get the available persona pairs for each domain
- `get_templates`: Get example templates for reasoning validation

## Example

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
    "detailed_feedback": "...",
    "blind_spots_count": 2,
    "contradictions_count": 0
  }
}
```

## Integration with LLM Systems

This tool is designed to be integrated with reasoning LLMs:

1. LLM receives a query and generates initial reasoning
2. LLM sends reasoning to Counter-Pose MCP server for validation
3. Counter-Pose returns critique and recommendations
4. LLM reviews feedback and decides whether to revise its approach
5. LLM provides final response to the user with improved confidence

## License

MIT
