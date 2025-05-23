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
    
    init_result = tool.submit_reasoning(session_id, initial_reasoning)
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
    select_result = tool.get_persona_guidance(session_id, recommended_pair)
    
    print(f"Selected Personas: {', '.join(select_result['selected_personas'])}")
    print(f"Next Step: {select_result['next_step']}")
    print(f"Format keys: {list(select_result['format'].keys())}")
    
    # Step 3: Submit both critiques
    print("\nStep 3: Submit Both Critiques")
    print("-" * 40)
    
    persona1_critique = """
    👨‍💻 FRONTEND ENGINEER's CRITIQUE:
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
    
    persona2_critique = """
    🧑‍🎨 UX DESIGNER's CRITIQUE:
    From a user experience perspective, this authentication system needs consideration:
    
    1. No mention of user feedback during authentication process
    2. 24-hour expiration might frustrate users who need to re-login frequently
    3. No consideration of different user types or permission levels
    4. Missing accessibility considerations for authentication forms
    5. No plan for handling authentication errors gracefully
    
    UX improvements to consider:
    - Clear loading states during authentication
    - Helpful error messages for failed logins
    - Remember me functionality
    - Password strength indicators
    END CRITIQUE
    """
    
    critique_result = tool.submit_critique(session_id, select_result['selected_personas'][0], persona1_critique, select_result['selected_personas'][1], persona2_critique)
    print(f"Critiques Complete: {critique_result.get('critiques_complete', False)}")
    print(f"Next Step: {critique_result['next_step']}")
    print(f"Steps Completed: {critique_result.get('steps_completed', 0)}/{critique_result.get('total_steps', 0)}")
    
    # Step 4: Display synthesis format (critiques are now complete)
    print("\nStep 4: Ready for Synthesis")
    print("-" * 40)
    
    if critique_result.get('critiques_complete'):
        print("✅ All critiques completed!")
        print(f"Domain: {critique_result['domain']}")
        print(f"Personas: {', '.join(critique_result['personas'])}")
        print(f"Total steps completed: {critique_result['steps_completed']}")
        print("\nSynthesis format provided:")
        print(critique_result.get('format', 'No format provided'))
    else:
        print("❌ Critiques not complete")
    
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
