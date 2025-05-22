"""Test the refactored session-based Counter-Pose MCP Server."""

import sys
import uuid
from src.mcp_server.counter_pose_tool import CounterPoseTool

def test_counter_pose_session_flow():
    """Test the complete flow of a Counter-Pose session."""
    # Initialize tool
    tool = CounterPoseTool()
    
    # Generate a test session ID
    session_id = str(uuid.uuid4())
    
    # Sample reasoning for a software development problem
    initial_reasoning = """
    I'm designing an authentication system for our web application. I plan to use JWT tokens 
    stored in localStorage with a 24-hour expiration. The authentication flow will be:
    1. User enters credentials
    2. Server validates and returns JWT
    3. Frontend stores token in localStorage
    4. Token is included in Authorization header for API calls
    
    This approach is simple to implement and works well with our React frontend.
    """
    
    print("\n" + "=" * 80)
    print("TESTING COUNTER-POSE SESSION FLOW")
    print("=" * 80)
    
    # Step 1: Initialize session
    print("\nStep 1: Initialize Session")
    print("-" * 40)
    
    init_result = tool.init_session(session_id, initial_reasoning)
    print(f"Session ID: {init_result['session_id']}")
    print(f"Detected Domain: {init_result['domain']}")
    print(f"Next Step: {init_result['next_step']}")
    
    # Display persona options
    print("\nPersona Options:")
    for i, option in enumerate(init_result['persona_options'], 1):
        rec = " (RECOMMENDED)" if option['recommended'] else ""
        print(f"  {i}. {option['personas'][0]} vs {option['personas'][1]}{rec}")
        print(f"     Score: {option['score']}, Reason: {option['reason']}")
    
    # Step 2: Select personas (use the recommended pair)
    print("\nStep 2: Select Personas")
    print("-" * 40)
    
    recommended_pair = next(opt['personas'] for opt in init_result['persona_options'] if opt['recommended'])
    select_result = tool.select_personas(session_id, recommended_pair)
    
    print(f"Selected Personas: {', '.join(select_result['selected_personas'])}")
    print(f"Next Step: {select_result['next_step']} by {select_result['next_persona']}")
    
    # Step 3: Submit first critique (Developer)
    print("\nStep 3: Submit First Critique (Developer)")
    print("-" * 40)
    
    developer_critique = """
    👨‍💻 DEVELOPER's CRITIQUE:
    The authentication approach covers the basic flow, but has several technical limitations:
    
    1. Storing JWTs in localStorage is accessible to JavaScript, making it vulnerable to XSS attacks
    2. There's no mention of token refresh strategy - what happens when tokens expire?
    3. Error handling isn't addressed - how will authentication failures be managed?
    4. The implementation doesn't consider scalability with multiple services or microservices
    5. There's no consideration of performance impact of including tokens in every request
    
    Alternative approaches worth considering:
    - Using HTTP-only cookies for token storage to mitigate XSS risks
    - Implementing a token refresh mechanism
    - Considering a centralized auth service if using microservices
    END CRITIQUE
    """
    
    critique1_result = tool.submit_critique(session_id, select_result['selected_personas'][0], developer_critique)
    print(f"Current Step: {critique1_result['current_step']}")
    print(f"Next Step: {critique1_result['next_step']} by {critique1_result.get('next_persona', 'N/A')}")
    
    # Step 4: Submit second critique (Security Expert)
    print("\nStep 4: Submit Second Critique (Security Expert)")
    print("-" * 40)
    
    security_critique = """
    🔒 SECURITY EXPERT's CRITIQUE:
    The proposed authentication design has serious security vulnerabilities:
    
    1. LocalStorage is vulnerable to XSS attacks - tokens can be stolen by injected scripts
    2. There's no mention of HTTPS enforcement, which is essential for secure token transmission
    3. The 24-hour expiration is too long for a sensitive application
    4. No mention of CSRF protection mechanisms
    5. No consideration of secure login practices (rate limiting, 2FA, etc.)
    
    Alternative approaches:
    - Store tokens in HttpOnly cookies to prevent JavaScript access
    - Implement shorter token lifetimes (1 hour) with refresh tokens
    - Add CSRF protection if using cookies
    - Consider adding rate limiting on login endpoints
    END CRITIQUE
    """
    
    critique2_result = tool.submit_critique(session_id, select_result['selected_personas'][1], security_critique)
    print(f"Current Step: {critique2_result['current_step']}")
    print(f"Next Step: {critique2_result['next_step']}")
    
    # Step 5: Submit synthesis
    print("\nStep 5: Submit Synthesis")
    print("-" * 40)
    
    synthesis = """
    SYNTHESIS OF PERSPECTIVES:
    
    After considering both the Developer and Security Expert perspectives, several important issues have been identified with the original authentication approach.
    
    BLIND SPOTS IDENTIFIED:
    1. XSS vulnerability with localStorage token storage
    2. No token refresh mechanism
    3. No HTTPS enforcement
    4. Excessive token lifetime
    5. No CSRF protection
    6. No error handling strategy
    7. Scalability concerns with microservices
    
    CONTRADICTIONS FOUND:
    None - both perspectives identified complementary issues
    
    CONFIDENCE: Low
    
    CHANGES NEEDED: Yes
    
    RECOMMENDATION:
    The authentication system requires significant security improvements before implementation:
    
    1. Use HttpOnly cookies instead of localStorage to store tokens
    2. Implement HTTPS across all endpoints
    3. Reduce token lifetime to 1 hour and implement a refresh token mechanism
    4. Add CSRF protection when using cookies
    5. Implement rate limiting on authentication endpoints
    6. Add comprehensive error handling
    7. Consider centralized authentication if using microservices
    
    This revised approach balances security requirements with development considerations.
    END SYNTHESIS
    """
    
    synthesis_result = tool.submit_synthesis(session_id, synthesis)
    print(f"Session completed: {synthesis_result['complete']}")
    print(f"Confidence: {synthesis_result['confidence']}")
    print(f"Changes needed: {synthesis_result['changes_needed']}")
    
    print("\nStep 6: Validation Complete")
    print("-" * 40)
    print(f"Domain: {synthesis_result['domain']}")
    print(f"Personas: {', '.join(synthesis_result['personas'])}")
    print(f"Steps completed: {synthesis_result['steps_completed']}")
    
    print("\n✅ Test completed successfully!")
    return True


def test_multi_domain_detection():
    """Test domain detection across multiple domains."""
    # Initialize tool
    tool = CounterPoseTool()
    
    # Test cases for each domain
    test_cases = {
        "software_development": "I'm building a React application with a Node.js backend. The database will be MongoDB.",
        "digital_marketing": "Our email campaign needs better segmentation and a stronger call to action. The conversion rate is too low.",
        "visual_design": "The UI design uses too many colors and inconsistent typography. We need a more cohesive visual system.",
        "product_strategy": "We should prioritize the features that align with our target market and provide competitive differentiation."
    }
    
    print("\n" + "=" * 80)
    print("TESTING DOMAIN DETECTION")
    print("=" * 80)
    
    all_passed = True
    for expected_domain, text in test_cases.items():
        detected_domain = tool.determine_domain(text)
        match = detected_domain == expected_domain
        if not match:
            all_passed = False
            
        print(f"\nText: {text[:50]}...")
        print(f"Expected domain: {expected_domain}")
        print(f"Detected domain: {detected_domain}")
        print(f"Match: {'✅' if match else '❌'}")
    
    if all_passed:
        print("\n✅ All domain detection tests passed!")
    else:
        print("\n❌ Some domain detection tests failed!")
    
    return all_passed


if __name__ == "__main__":
    test1_success = test_counter_pose_session_flow()
    test2_success = test_multi_domain_detection()
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)
