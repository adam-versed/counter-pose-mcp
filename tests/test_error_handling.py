"""Test error handling and edge cases for the Counter-Pose tool."""

import sys
import uuid
from src.mcp_server.counter_pose_tool import CounterPoseTool

def test_invalid_session_handling():
    """Test handling of invalid session IDs across all methods."""
    tool = CounterPoseTool()
    
    print("TESTING INVALID SESSION HANDLING")
    print("=" * 40)
    
    fake_session_id = str(uuid.uuid4())
    all_passed = True
    
    # Test select_personas with invalid session
    print("\nTesting select_personas with invalid session:")
    result = tool.select_personas(fake_session_id, ["Developer", "Security Expert"])
    if 'error' in result and 'not found' in result['error']:
        print("✅ select_personas correctly handles invalid session")
    else:
        print("❌ select_personas should return error for invalid session")
        all_passed = False
    
    # Test submit_critique with invalid session
    print("\nTesting submit_critique with invalid session:")
    result = tool.submit_critique(fake_session_id, "Developer", "Some critique")
    if 'error' in result and 'not found' in result['error']:
        print("✅ submit_critique correctly handles invalid session")
    else:
        print("❌ submit_critique should return error for invalid session")
        all_passed = False
    
    # Test submit_synthesis with invalid session
    print("\nTesting submit_synthesis with invalid session:")
    result = tool.submit_synthesis(fake_session_id, "Some synthesis")
    if 'error' in result and 'not found' in result['error']:
        print("✅ submit_synthesis correctly handles invalid session")
    else:
        print("❌ submit_synthesis should return error for invalid session")
        all_passed = False
    
    return all_passed


def test_invalid_persona_validation():
    """Test validation of persona inputs."""
    tool = CounterPoseTool()
    
    print("\n" + "=" * 40)
    print("TESTING INVALID PERSONA VALIDATION")
    print("=" * 40)
    
    # Initialize a valid session
    session_id = str(uuid.uuid4())
    tool.init_session(session_id, "Test reasoning for validation")
    
    all_passed = True
    
    # Test with wrong number of personas
    print("\nTesting wrong number of personas:")
    test_cases = [
        [],  # Empty list
        ["Only One"],  # Too few
        ["One", "Two", "Three"],  # Too many
    ]
    
    for i, personas in enumerate(test_cases):
        result = tool.select_personas(session_id, personas)
        if 'error' in result:
            print(f"✅ Case {i+1}: Correctly rejected {len(personas)} personas")
        else:
            print(f"❌ Case {i+1}: Should reject {len(personas)} personas")
            all_passed = False
    
    # Set up valid personas for critique testing
    tool.select_personas(session_id, ["Developer", "Security Expert"])
    
    # Test submit_critique with invalid persona
    print("\nTesting submit_critique with invalid persona:")
    result = tool.submit_critique(session_id, "NonExistentPersona", "Some critique")
    if 'error' in result and 'not part of this session' in result['error']:
        print("✅ submit_critique correctly rejects invalid persona")
    else:
        print("❌ submit_critique should reject invalid persona")
        all_passed = False
    
    return all_passed


def test_empty_and_edge_case_inputs():
    """Test handling of empty strings and edge case inputs."""
    tool = CounterPoseTool()
    
    print("\n" + "=" * 40)
    print("TESTING EMPTY AND EDGE CASE INPUTS")
    print("=" * 40)
    
    all_passed = True
    
    # Test empty reasoning string
    print("\nTesting empty reasoning string:")
    session_id = str(uuid.uuid4())
    try:
        result = tool.init_session(session_id, "")
        # Should not crash, should default to product_strategy domain
        if result.get('domain') == 'product_strategy':
            print("✅ Empty reasoning defaults to product_strategy domain")
        else:
            print(f"❌ Empty reasoning gave domain: {result.get('domain')}")
            all_passed = False
    except Exception as e:
        print(f"❌ Empty reasoning caused exception: {e}")
        all_passed = False
    
    # Test very short reasoning
    print("\nTesting very short reasoning:")
    try:
        result = tool.init_session(str(uuid.uuid4()), "a")
        if 'domain' in result:
            print("✅ Very short reasoning handled without crash")
        else:
            print("❌ Very short reasoning failed")
            all_passed = False
    except Exception as e:
        print(f"❌ Very short reasoning caused exception: {e}")
        all_passed = False
    
    # Test very long reasoning
    print("\nTesting very long reasoning:")
    long_reasoning = "software development " * 1000  # Very long string
    try:
        result = tool.init_session(str(uuid.uuid4()), long_reasoning)
        if result.get('domain') == 'software_development':
            print("✅ Very long reasoning handled correctly")
        else:
            print(f"❌ Very long reasoning gave unexpected domain: {result.get('domain')}")
            all_passed = False
    except Exception as e:
        print(f"❌ Very long reasoning caused exception: {e}")
        all_passed = False
    
    # Test special characters
    print("\nTesting special characters:")
    special_reasoning = "software 💻 development with émojis and ñoñ-ASCII çhars"
    try:
        result = tool.init_session(str(uuid.uuid4()), special_reasoning)
        if 'domain' in result:
            print("✅ Special characters handled without crash")
        else:
            print("❌ Special characters failed")
            all_passed = False
    except Exception as e:
        print(f"❌ Special characters caused exception: {e}")
        all_passed = False
    
    return all_passed


def test_session_state_consistency():
    """Test that session state remains consistent through the flow."""
    tool = CounterPoseTool()
    
    print("\n" + "=" * 40)
    print("TESTING SESSION STATE CONSISTENCY")
    print("=" * 40)
    
    session_id = str(uuid.uuid4())
    all_passed = True
    
    # Initialize session
    init_result = tool.init_session(session_id, "I need help with software security and development")
    print(f"Initialized session with domain: {init_result['domain']}")
    
    # Select personas
    selected_personas = ["Developer", "Security Expert"]
    select_result = tool.select_personas(session_id, selected_personas)
    
    # Verify session state
    session = tool.sessions.get(session_id)
    if not session:
        print("❌ Session not found in sessions dict")
        return False
    
    state_checks = [
        (session.personas == selected_personas, "Personas stored correctly"),
        (session.domain == init_result['domain'], "Domain preserved"),
        (session.session_id == session_id, "Session ID matches"),
        (len(session.steps) == 0, "Steps list initially empty"),
    ]
    
    for check_result, description in state_checks:
        if check_result:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_passed = False
    
    # Submit first critique and check state
    critique_result = tool.submit_critique(session_id, "Developer", "Test critique")
    
    # Check that step was recorded
    if len(session.steps) == 1:
        print("✅ Critique step recorded")
        step = session.steps[0]
        if (step['type'] == 'critique' and 
            step['persona'] == 'Developer' and 
            'timestamp' in step):
            print("✅ Critique step has correct structure")
        else:
            print("❌ Critique step structure incorrect")
            all_passed = False
    else:
        print(f"❌ Expected 1 step, found {len(session.steps)}")
        all_passed = False
    
    return all_passed


def test_concurrent_sessions():
    """Test that multiple sessions can run independently."""
    tool = CounterPoseTool()
    
    print("\n" + "=" * 40)
    print("TESTING CONCURRENT SESSIONS")
    print("=" * 40)
    
    # Create multiple sessions
    sessions = []
    for i in range(3):
        session_id = str(uuid.uuid4())
        domain_texts = [
            "I need help with software development",
            "I need help with digital marketing campaigns", 
            "I need help with visual design decisions"
        ]
        expected_domains = ["software_development", "digital_marketing", "visual_design"]
        
        result = tool.init_session(session_id, domain_texts[i])
        sessions.append({
            'id': session_id,
            'expected_domain': expected_domains[i],
            'actual_domain': result['domain']
        })
    
    all_passed = True
    
    # Verify all sessions exist and are independent
    print(f"\nCreated {len(sessions)} concurrent sessions:")
    for i, session_info in enumerate(sessions):
        session_obj = tool.sessions.get(session_info['id'])
        if session_obj:
            domain_correct = session_info['actual_domain'] == session_info['expected_domain']
            print(f"✅ Session {i+1}: Domain {session_info['actual_domain']} {'✅' if domain_correct else '❌'}")
            if not domain_correct:
                all_passed = False
        else:
            print(f"❌ Session {i+1}: Not found in sessions dict")
            all_passed = False
    
    # Verify sessions don't interfere with each other
    session1_id = sessions[0]['id']
    session2_id = sessions[1]['id']
    
    # Select different personas for each
    tool.select_personas(session1_id, ["Developer", "Security Expert"])
    tool.select_personas(session2_id, ["Creative Director", "Analytics Specialist"])
    
    session1 = tool.sessions[session1_id]
    session2 = tool.sessions[session2_id]
    
    if (session1.personas != session2.personas and
        session1.domain != session2.domain):
        print("✅ Sessions remain independent")
    else:
        print("❌ Session state interference detected")
        all_passed = False
    
    return all_passed


if __name__ == "__main__":
    test1_success = test_invalid_session_handling()
    test2_success = test_invalid_persona_validation()
    test3_success = test_empty_and_edge_case_inputs()
    test4_success = test_session_state_consistency()
    test5_success = test_concurrent_sessions()
    
    print("\n" + "=" * 40)
    print("ERROR HANDLING TEST SUMMARY")
    print("=" * 40)
    
    tests = [
        ("Invalid session handling", test1_success),
        ("Invalid persona validation", test2_success),
        ("Empty/edge case inputs", test3_success),
        ("Session state consistency", test4_success),
        ("Concurrent sessions", test5_success),
    ]
    
    all_passed = all(success for _, success in tests)
    
    for test_name, success in tests:
        print(f"  {test_name}: {'✅' if success else '❌'}")
    
    if all_passed:
        print("\n🎉 All error handling tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some error handling tests failed!")
        sys.exit(1) 