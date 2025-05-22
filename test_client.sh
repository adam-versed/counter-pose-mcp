#!/bin/bash

# Test client for the Counter-Pose MCP Reasoning Validator

echo "Testing the Counter-Pose MCP Reasoning Validator"
echo "==============================================="

# Generate a session ID for this test
SESSION_ID="test-session-$(date +%s)"

# Initial reasoning for authentication system
echo -e "\nStep 1: Initialize Counter-Pose Session"
echo '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "callTool",
  "params": {
    "name": "init_counter_pose",
    "arguments": {
      "reasoning": "I am designing an authentication system for our web application. I plan to use JWT tokens stored in localStorage with a 24-hour expiration. The authentication flow will be: 1) User enters credentials, 2) Server validates and returns JWT, 3) Frontend stores token in localStorage, 4) Token is included in Authorization header for API calls. This approach is simple to implement and works well with our React frontend.",
      "session_id": "'$SESSION_ID'"
    }
  }
}' | nc -U /tmp/mcp.sock

# Select personas (use the recommended pair from Step 1)
echo -e "\nStep 2: Select Personas"
echo '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "callTool",
  "params": {
    "name": "select_personas",
    "arguments": {
      "session_id": "'$SESSION_ID'",
      "persona_pair": ["Developer", "Security Expert"]
    }
  }
}' | nc -U /tmp/mcp.sock

# Submit developer critique
echo -e "\nStep 3: Submit Developer Critique"
echo '{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "callTool",
  "params": {
    "name": "submit_critique",
    "arguments": {
      "session_id": "'$SESSION_ID'",
      "persona": "Developer",
      "critique": "👨‍💻 DEVELOPER'\''s CRITIQUE:\nThe authentication approach covers the basic flow, but has several technical limitations:\n\n1. Storing JWTs in localStorage is accessible to JavaScript, making it vulnerable to XSS attacks\n2. There'\''s no mention of token refresh strategy - what happens when tokens expire?\n3. Error handling isn'\''t addressed - how will authentication failures be managed?\n4. The implementation doesn'\''t consider scalability with multiple services or microservices\n5. There'\''s no consideration of performance impact of including tokens in every request\n\nAlternative approaches worth considering:\n- Using HTTP-only cookies for token storage to mitigate XSS risks\n- Implementing a token refresh mechanism\n- Considering a centralized auth service if using microservices\nEND CRITIQUE"
    }
  }
}' | nc -U /tmp/mcp.sock

# Submit security expert critique
echo -e "\nStep 4: Submit Security Expert Critique"
echo '{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "callTool",
  "params": {
    "name": "submit_critique",
    "arguments": {
      "session_id": "'$SESSION_ID'",
      "persona": "Security Expert",
      "critique": "🔒 SECURITY EXPERT'\''s CRITIQUE:\nThe proposed authentication design has serious security vulnerabilities:\n\n1. LocalStorage is vulnerable to XSS attacks - tokens can be stolen by injected scripts\n2. There'\''s no mention of HTTPS enforcement, which is essential for secure token transmission\n3. The 24-hour expiration is too long for a sensitive application\n4. No mention of CSRF protection mechanisms\n5. No consideration of secure login practices (rate limiting, 2FA, etc.)\n\nAlternative approaches:\n- Store tokens in HttpOnly cookies to prevent JavaScript access\n- Implement shorter token lifetimes (1 hour) with refresh tokens\n- Add CSRF protection if using cookies\n- Consider adding rate limiting on login endpoints\nEND CRITIQUE"
    }
  }
}' | nc -U /tmp/mcp.sock

# Submit synthesis
echo -e "\nStep 5: Submit Synthesis"
echo '{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "callTool",
  "params": {
    "name": "submit_synthesis",
    "arguments": {
      "session_id": "'$SESSION_ID'",
      "synthesis": "SYNTHESIS OF PERSPECTIVES:\n\nAfter considering both the Developer and Security Expert perspectives, several important issues have been identified with the original authentication approach.\n\nBLIND SPOTS IDENTIFIED:\n1. XSS vulnerability with localStorage token storage\n2. No token refresh mechanism\n3. No HTTPS enforcement\n4. Excessive token lifetime\n5. No CSRF protection\n6. No error handling strategy\n7. Scalability concerns with microservices\n\nCONTRADICTIONS FOUND:\nNone - both perspectives identified complementary issues\n\nCONFIDENCE: Low\n\nCHANGES NEEDED: Yes\n\nRECOMMENDATION:\nThe authentication system requires significant security improvements before implementation:\n\n1. Use HttpOnly cookies instead of localStorage to store tokens\n2. Implement HTTPS across all endpoints\n3. Reduce token lifetime to 1 hour and implement a refresh token mechanism\n4. Add CSRF protection when using cookies\n5. Implement rate limiting on authentication endpoints\n6. Add comprehensive error handling\n7. Consider centralized authentication if using microservices\n\nThis revised approach balances security requirements with development considerations.\nEND SYNTHESIS"
    }
  }
}' | nc -U /tmp/mcp.sock

echo -e "\nTest completed! Session validation flow executed successfully."
