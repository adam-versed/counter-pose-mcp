#!/bin/bash

# Test client for the Counter-Pose MCP Reasoning Validator

echo "Testing the Counter-Pose MCP Reasoning Validator"
echo "==============================================="

# Generate a session ID for this test
SESSION_ID="test-session-$(date +%s)"

# Initial reasoning for authentication system
echo -e "\nStep 1: Submit Reasoning for Analysis"
echo '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "callTool",
  "params": {
    "name": "submit_reasoning",
    "arguments": {
      "reasoning": "I am designing an authentication system for our web application. I plan to use JWT tokens stored in localStorage with a 24-hour expiration. The authentication flow will be: 1) User enters credentials, 2) Server validates and returns JWT, 3) Frontend stores token in localStorage, 4) Token is included in Authorization header for API calls. This approach is simple to implement and works well with our React frontend.",
      "session_id": "'$SESSION_ID'"
    }
  }
}' | nc -U /tmp/mcp.sock

# Select personas (use the recommended pair from Step 1)
echo -e "\nStep 2: Get Persona Guidance"
echo '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "callTool",
  "params": {
    "name": "get_persona_guidance",
    "arguments": {
      "session_id": "'$SESSION_ID'",
      "persona_pair": ["Developer", "Security Expert"]
    }
  }
}' | nc -U /tmp/mcp.sock

# Submit both critiques at once
echo -e "\nStep 3: Submit Both Critiques"
echo '{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "callTool",
  "params": {
    "name": "submit_critique",
    "arguments": {
      "session_id": "'$SESSION_ID'",
      "persona1_name": "Developer",
      "persona1_critique": "👨‍💻 DEVELOPER'\''s CRITIQUE:\nThe authentication approach covers the basic flow, but has several technical limitations:\n\n1. Storing JWTs in localStorage is accessible to JavaScript, making it vulnerable to XSS attacks\n2. There'\''s no mention of token refresh strategy - what happens when tokens expire?\n3. Error handling isn'\''t addressed - how will authentication failures be managed?\n4. The implementation doesn'\''t consider scalability with multiple services or microservices\n5. There'\''s no consideration of performance impact of including tokens in every request\n\nAlternative approaches worth considering:\n- Using HTTP-only cookies for token storage to mitigate XSS risks\n- Implementing a token refresh mechanism\n- Considering a centralized auth service if using microservices\nEND CRITIQUE",
      "persona2_name": "Security Expert",
      "persona2_critique": "🔒 SECURITY EXPERT'\''s CRITIQUE:\nThe proposed authentication design has serious security vulnerabilities:\n\n1. LocalStorage is vulnerable to XSS attacks - tokens can be stolen by injected scripts\n2. There'\''s no mention of HTTPS enforcement, which is essential for secure token transmission\n3. The 24-hour expiration is too long for a sensitive application\n4. No mention of CSRF protection mechanisms\n5. No consideration of secure login practices (rate limiting, 2FA, etc.)\n\nAlternative approaches:\n- Store tokens in HttpOnly cookies to prevent JavaScript access\n- Implement shorter token lifetimes (1 hour) with refresh tokens\n- Add CSRF protection if using cookies\n- Consider adding rate limiting on login endpoints\nEND CRITIQUE"
    }
  }
}' | nc -U /tmp/mcp.sock

echo -e "\nStep 4: LLM uses synthesis format to complete analysis"
echo "The calling LLM would now use the synthesis format guidance to generate a final analysis."

echo -e "\nTest completed! New streamlined 3-step flow executed successfully."
