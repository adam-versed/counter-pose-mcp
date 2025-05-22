# Counter-Pose MCP Server: Reasoning Validator

An implementation of the RPT (Reasoning-through-Perspective-Transition) technique as an MCP (Model Context Protocol) server focused on validating and critiquing LLM reasoning.

## About RPT and Reasoning Validation

The RPT (Reasoning-through-Perspective-Transition) technique is a prompting method that improves AI responses by introducing deliberate perspective conflict between different personas. This approach was discovered by Tsinghua University researchers in January 2025 and has shown to reduce inaccuracies by up to 40%.

This implementation adapts RPT specifically for **reasoning validation and improvement**, adding a metacognitive layer to LLM reasoning:

1. **LLM Reasoning**: A reasoning LLM produces initial thoughts about a query
2. **Domain-Aware Analysis**: Counter-Pose automatically detects the domain and selects relevant expert personas
3. **Multi-Expert Critique**: Domain experts provide structured critique identifying blind spots and weaknesses
4. **Validation Synthesis**: Combines perspectives into actionable recommendations with confidence assessment
5. **Reasoning Refinement**: Original LLM can revise its approach based on expert feedback

**Key Advantages:**

- **Automatic Domain Detection**: No manual domain specification required
- **Intelligent Expert Selection**: Gets the most relevant expert pairing for your content
- **Structured Validation Output**: Standardized format for confidence, blind spots, and recommendations
- **Session-Based**: Maintains context across multi-step validation process

## How It Works

The Counter-Pose Reasoning Validator uses a session-based flow with intelligent persona selection:

1. **Domain Detection**: Analyzes the reasoning text to automatically determine the most relevant domain (software development, digital marketing, visual design, or product strategy)
2. **Intelligent Persona Ranking**: Uses keyword matching to rank persona pairs within the detected domain, recommending the most relevant experts for your specific reasoning
3. **Persona Selection**: LLM chooses from ranked persona pair options (or can specify custom personas)
4. **Multi-Perspective Critique**: Each selected persona provides detailed critique from their domain expertise
5. **Synthesis & Validation**: Combines all perspectives to identify blind spots, contradictions, confidence level, and recommendations for improvement

**Key Features:**

- **Automatic Domain Detection**: No need to manually specify domain
- **Smart Persona Recommendations**: Gets the most relevant expert pairing based on content analysis
- **Session-Based Flow**: Maintains context across multiple tool calls
- **Comprehensive Validation**: Structured output with confidence assessment and actionable recommendations

## Available Domains

The server supports the following domains with specialized persona pairs:

### **Software Development**

- Developer vs Security Expert
- Frontend Engineer vs UX Designer
- Backend Engineer vs DevOps Engineer
- Performance Engineer vs Maintainability Advocate

### **Digital Marketing**

- Creative Director vs Analytics Specialist
- Brand Strategist vs Conversion Optimizer
- Social Media Expert vs Growth Hacker
- Content Creator vs Performance Marketer
- B2B Marketer vs B2C Marketer
- Landing Page Expert vs SEO Specialist

### **Visual Design**

- UI Minimalist vs Feature-Rich Designer
- Brand Identity Expert vs User-Centered Designer
- Print Design Specialist vs Digital-First Designer
- Artistic Creative vs Data-Driven Designer
- Accessibility Expert vs Visual Artist

### **Product Strategy**

- Customer Advocate vs Business Strategist
- Innovative Disruptor vs Market Researcher
- MVP Champion vs Quality Perfectionist
- Long-term Strategist vs Quick-to-Market Tactician
- Technical PM vs Business PM

**Smart Persona Selection**: The system automatically ranks these pairs based on keyword analysis of your reasoning content, recommending the most relevant expert pairing for your specific use case.

## Installation and Setup

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions on:

- Setting up the Counter-Pose MCP server
- Integrating with Claude Desktop
- Integrating with Cursor IDE
- Troubleshooting common issues

### Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd counter-pose-mcp

# Run the setup script (installs dependencies)
./setup.sh

# Run the server (starts MCP server)
./run_server.sh

# In another terminal, test the server
./test_client.sh
```

### Testing

Run the included test suite to verify functionality:

```bash
# Run all tests
python -m pytest tests/ -v

# Test individual components
python tests/test_domain_detection.py
python tests/test_session_flow.py
python tests/test_persona_selection.py
python tests/test_error_handling.py

# Test MCP server interface
./test_client.sh
```

## Available Tools

The server provides the following tools for a session-based reasoning validation flow:

- `init_counter_pose`: Initialize a session and get ranked persona pair recommendations
- `select_personas`: Choose which persona pair to use for critique
- `submit_critique`: Submit critiques from each selected persona
- `submit_synthesis`: Submit the final synthesis of all perspectives

## Example Usage Flow

Here's an example of the complete reasoning validation flow:

### Step 1: Initialize Session

```json
// Call: init_counter_pose
{
  "reasoning": "I need to implement authentication for our web application. I think we should use JWT tokens since they are stateless and work well with modern frontend frameworks. We can set the expiration time to 24 hours and store the tokens in local storage. This approach will be easy to implement and maintain."
}
```

Response:

```json
{
  "session_id": "uuid-here",
  "domain": "software_development",
  "persona_options": [
    {
      "personas": ["Developer", "Security Expert"],
      "score": 3,
      "reason": "Matched keywords: authentication, JWT, security",
      "recommended": true
    }
  ],
  "next_step": "select_personas"
}
```

### Step 2: Select Personas

```json
// Call: select_personas
{
  "session_id": "uuid-here",
  "persona_pair": ["Developer", "Security Expert"]
}
```

### Step 3: Submit Critiques

```json
// Call: submit_critique (for each persona)
{
  "session_id": "uuid-here",
  "persona": "Developer",
  "critique": "The approach has technical limitations..."
}
```

### Step 4: Submit Synthesis

```json
// Call: submit_synthesis
{
  "session_id": "uuid-here",
  "synthesis": "After considering both perspectives, significant security improvements are needed..."
}
```

Final response includes confidence assessment, blind spots identified, and recommendations for improvement.

## Validation Output Format

The final synthesis provides structured validation results:

```json
{
  "session_id": "uuid-here",
  "domain": "software_development",
  "personas": ["Developer", "Security Expert"],
  "steps_completed": 3,
  "complete": true,
  "confidence": "Low|Medium|High",
  "changes_needed": true,
  "session_summary": {
    "blind_spots": ["XSS vulnerability", "No token refresh", "..."],
    "contradictions": ["..."],
    "recommendations": ["Use HttpOnly cookies", "Implement HTTPS", "..."]
  }
}
```

**Confidence Levels:**

- **High**: Reasoning is sound with minor or no issues identified
- **Medium**: Some concerns raised but overall approach is viable
- **Low**: Significant issues identified, changes strongly recommended

**Changes Needed**: Boolean indicating whether the original reasoning should be revised based on expert feedback.

## Integration with LLM Systems

This tool is designed to be integrated with reasoning LLMs as an external validation service:

1. **Initial Reasoning**: LLM receives a query and generates initial reasoning
2. **Validation Request**: LLM sends reasoning to Counter-Pose MCP server for validation
3. **Expert Analysis**: Counter-Pose returns structured critique and recommendations
4. **Reasoning Refinement**: LLM reviews feedback and decides whether to revise its approach
5. **Improved Response**: LLM provides final response to the user with enhanced confidence

### **Why Use MCP Server vs Direct RPT Prompting?**

- **Consistent Domain Expertise**: Pre-trained persona knowledge vs ad-hoc prompt personas
- **Intelligent Matching**: Automatic domain detection and expert selection
- **Structured Output**: Standardized validation format for programmatic use
- **Separation of Concerns**: Keep validation logic separate from main reasoning
- **Reusable**: Single server serves multiple LLM applications
- **Stateful Sessions**: Maintain context across multi-step validation processes

### **Supported Integrations**

- **Claude Desktop**: Direct MCP integration
- **Cursor IDE**: Code reasoning validation
- **Custom Applications**: Direct MCP protocol integration

## License

MIT
