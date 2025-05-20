# Counter-Pose MCP Server

An implementation of the RPT (Reasoning-through-Perspective-Transition) prompting technique as an MCP (Model Context Protocol) server.

## About RPT

The RPT (Reasoning-through-Perspective-Transition) technique is a prompting method that improves AI responses by introducing deliberate perspective conflict between different personas. This approach was discovered by Tsinghua University researchers in January 2025 and has shown to reduce inaccuracies by up to 40%.

The key mechanism is perspective conflict - when different viewpoints clash, the AI must resolve contradictions, which leads to more thorough and balanced responses.

## How it Works

The Counter-Pose MCP Server works in 3 simple steps:

1. It analyzes a query from the first persona's perspective
2. It critiques that initial analysis from a second, contrasting persona's perspective
3. It synthesizes a balanced, comprehensive answer that resolves contradictions between the perspectives

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

- `counter_pose`: Process a query using the Counter-Pose RPT technique
- `get_counter_pose_domains`: Get the available domains and their keywords
- `get_counter_pose_personas`: Get the available persona pairs for each domain
- `get_counter_pose_templates`: Get example templates for using the Counter-Pose tool

## Example

Here's an example of using the Counter-Pose technique:

```json
{
  "query": "Should I post on LinkedIn using my personal profile or the one from the business I want to grow?",
  "show_full_process": true
}
```

Response:

```json
{
  "domain": "digital_marketing",
  "personas": ["Brand Strategist", "Conversion Optimizer"],
  "first_perspective": "...",
  "critique": "...",
  "synthesis": {
    "answer": "...",
    "confidence": "High",
    "resolved_contradictions": [...]
  }
}
```

## License

MIT
