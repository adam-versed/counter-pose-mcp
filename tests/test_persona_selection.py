"""Test the intelligent persona selection and ranking system."""

import sys
import uuid
from src.mcp_server.counter_pose_tool import CounterPoseTool

def test_persona_ranking_accuracy():
    """Test that persona ranking correctly identifies the most relevant pairs."""
    tool = CounterPoseTool()
    
    print("TESTING INTELLIGENT PERSONA RANKING")
    print("=" * 50)
    
    # Test cases with expected top persona pairs
    test_cases = [
        {
            "name": "Social Media Growth",
            "reasoning": "I want to grow my X.com account from 0 to 10,000 followers using engagement strategies and social media best practices.",
            "expected_domain": "digital_marketing",
            "expected_top_pair": ("Social Media Expert", "Growth Hacker"),
            "should_contain_keywords": ["social media", "followers", "engagement"]
        },
        {
            "name": "Security Authentication",
            "reasoning": "I need to implement secure authentication with JWT tokens, considering encryption, vulnerability protection and privacy compliance.",
            "expected_domain": "software_development", 
            "expected_top_pair": ("Developer", "Security Expert"),
            "should_contain_keywords": ["security", "auth", "vulnerability"]
        },
        {
            "name": "Performance Optimization",
            "reasoning": "My application has performance issues. I need to optimize speed and efficiency while maintaining clean, maintainable code.",
            "expected_domain": "software_development",
            "expected_top_pair": ("Performance Engineer", "Maintainability Advocate"), 
            "should_contain_keywords": ["performance", "optimization", "speed"]
        },
        {
            "name": "B2B Marketing Strategy",
            "reasoning": "We need a marketing strategy targeting enterprise businesses rather than individual consumers for our B2B SaaS product.",
            "expected_domain": "digital_marketing",
            "expected_top_pair": ("B2B Marketer", "B2C Marketer"),
            "should_contain_keywords": ["b2b", "enterprise", "business"]
        },
        {
            "name": "Accessibility Design",
            "reasoning": "Our design needs to be more accessible for users with disabilities while maintaining visual appeal and artistic elements.",
            "expected_domain": "visual_design",
            "expected_top_pair": ("Accessibility Expert", "Visual Artist"),
            "should_contain_keywords": ["accessibility", "visual", "artistic"]
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\nTest Case: {test_case['name']}")
        print("-" * 30)
        
        reasoning = test_case["reasoning"]
        expected_domain = test_case["expected_domain"]
        expected_top_pair = test_case["expected_top_pair"]
        
        # Test domain detection
        detected_domain = tool.determine_domain(reasoning)
        domain_correct = detected_domain == expected_domain
        
        print(f"Domain: {detected_domain} (expected: {expected_domain}) {'✅' if domain_correct else '❌'}")
        
        if not domain_correct:
            all_passed = False
            continue
        
        # Test persona ranking
        ranked_pairs = tool._rank_persona_pairs(detected_domain, reasoning)
        
        if not ranked_pairs:
            print("❌ No ranked pairs returned")
            all_passed = False
            continue
            
        top_pair = ranked_pairs[0][0]  # (pair, score, reason)
        top_score = ranked_pairs[0][1]
        top_reason = ranked_pairs[0][2]
        
        pair_correct = top_pair == expected_top_pair
        score_meaningful = top_score > 0
        
        print(f"Top pair: {top_pair[0]} vs {top_pair[1]} (score: {top_score}) {'✅' if pair_correct else '❌'}")
        print(f"Reason: {top_reason}")
        print(f"Score > 0: {'✅' if score_meaningful else '❌'}")
        
        if not pair_correct:
            print(f"  Expected: {expected_top_pair[0]} vs {expected_top_pair[1]}")
            all_passed = False
        
        if not score_meaningful:
            print("  Expected score > 0 for keyword matches")
            all_passed = False
    
    return all_passed


def test_submit_reasoning_persona_options():
    """Test that submit_reasoning returns properly formatted persona options."""
    tool = CounterPoseTool()
    
    print("\n" + "=" * 50)
    print("TESTING SUBMIT_REASONING PERSONA OPTIONS")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    reasoning = "I need to optimize my social media content strategy to increase engagement and grow my X.com followers."
    
    result = tool.submit_reasoning(session_id, reasoning)
    
    print(f"Session ID: {result['session_id']}")
    print(f"Domain: {result['domain']}")
    print(f"Next step: {result['next_step']}")
    
    # Test structure
    required_keys = ['session_id', 'domain', 'persona_options', 'next_step', 'instructions']
    structure_valid = all(key in result for key in required_keys)
    print(f"Structure valid: {'✅' if structure_valid else '❌'}")
    
    # Test persona options format
    options = result['persona_options']
    options_valid = True
    
    if not isinstance(options, list) or len(options) == 0:
        print("❌ Persona options should be a non-empty list")
        options_valid = False
    else:
        print(f"Number of options: {len(options)}")
        
        # Check that exactly one option is recommended
        recommended_count = sum(1 for opt in options if opt.get('recommended', False))
        if recommended_count != 1:
            print(f"❌ Expected exactly 1 recommended option, got {recommended_count}")
            options_valid = False
        else:
            print("✅ Exactly one option marked as recommended")
        
        # Check format of each option
        for i, option in enumerate(options):
            required_option_keys = ['personas', 'score', 'reason', 'recommended']
            if not all(key in option for key in required_option_keys):
                print(f"❌ Option {i+1} missing required keys")
                options_valid = False
                continue
                
            personas = option['personas']
            if not isinstance(personas, list) or len(personas) != 2:
                print(f"❌ Option {i+1} personas should be list of 2 strings")
                options_valid = False
            
            if not isinstance(option['score'], (int, float)):
                print(f"❌ Option {i+1} score should be numeric")
                options_valid = False
    
    print(f"Options format valid: {'✅' if options_valid else '❌'}")
    
    # Display all options
    print("\nPersona Options:")
    for i, option in enumerate(options, 1):
        rec = " (RECOMMENDED)" if option.get('recommended', False) else ""
        print(f"  {i}. {option['personas'][0]} vs {option['personas'][1]}{rec}")
        print(f"     Score: {option['score']}, Reason: {option['reason']}")
    
    return structure_valid and options_valid


def test_get_persona_guidance_validation():
    """Test persona selection validation and flow."""
    tool = CounterPoseTool()
    
    print("\n" + "=" * 50)
    print("TESTING GET_PERSONA_GUIDANCE VALIDATION")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    reasoning = "I need help with my software architecture design and security considerations."
    
    # Initialize session
    init_result = tool.submit_reasoning(session_id, reasoning)
    print(f"Initialized session for domain: {init_result['domain']}")
    
    # Test valid persona selection
    print("\nTesting valid persona selection:")
    valid_pair = ["Developer", "Security Expert"]
    select_result = tool.get_persona_guidance(session_id, valid_pair)
    
    valid_selection = (
        'error' not in select_result and
        select_result.get('selected_personas') == valid_pair and
        'next_step' in select_result and
        'format' in select_result
    )
    
    print(f"Valid selection: {'✅' if valid_selection else '❌'}")
    if valid_selection:
        print(f"  Selected: {', '.join(select_result['selected_personas'])}")
        print(f"  Next step: {select_result['next_step']}")
    
    # Test invalid persona selection (wrong number)
    print("\nTesting invalid persona selection (wrong count):")
    invalid_result = tool.get_persona_guidance(session_id, ["Only One Persona"])
    invalid_handled = 'error' in invalid_result
    print(f"Error handled: {'✅' if invalid_handled else '❌'}")
    if invalid_handled:
        print(f"  Error: {invalid_result['error']}")
    
    # Test invalid session ID
    print("\nTesting invalid session ID:")
    fake_session = str(uuid.uuid4())
    session_error_result = tool.get_persona_guidance(fake_session, valid_pair)
    session_error_handled = 'error' in session_error_result
    print(f"Session error handled: {'✅' if session_error_handled else '❌'}")
    if session_error_handled:
        print(f"  Error: {session_error_result['error']}")
    
    return valid_selection and invalid_handled and session_error_handled


def test_new_critique_flow():
    """Test the new 3-step submit_critique flow."""
    tool = CounterPoseTool()
    
    print("\n" + "=" * 50)
    print("TESTING NEW 3-STEP CRITIQUE FLOW")
    print("=" * 50)
    
    session_id = str(uuid.uuid4())
    reasoning = "I need help with my social media growth strategy and content creation."
    
    # Initialize session
    init_result = tool.submit_reasoning(session_id, reasoning)
    print(f"Domain: {init_result['domain']}")
    
    # Get recommended personas from the session
    recommended_option = next(opt for opt in init_result['persona_options'] if opt['recommended'])
    personas = recommended_option['personas']
    
    # Select personas
    select_result = tool.get_persona_guidance(session_id, personas)
    print(f"Selected personas: {', '.join(select_result['selected_personas'])}")
    
    # Test complete critique submission (both personas)
    print(f"\nSubmitting critiques from both {personas[0]} and {personas[1]}:")
    first_critique = f"This is a test critique from {personas[0]}."
    second_critique = f"This is a test critique from {personas[1]}."
    result1 = tool.submit_critique(session_id, personas[0], first_critique, personas[1], second_critique)
    
    complete_flow = (
        'error' not in result1 and
        result1.get('critiques_complete') == True and
        result1.get('next_step') == 'synthesis' and
        result1.get('steps_completed') == 3 and
        result1.get('total_steps') == 3 and
        'format' in result1
    )
    
    print(f"Critique submission completes flow: {'✅' if complete_flow else '❌'}")
    if complete_flow:
        print(f"  Critiques complete: {result1['critiques_complete']}")
        print(f"  Next step: {result1['next_step']}")
        print(f"  Steps completed: {result1['steps_completed']}/{result1['total_steps']}")
    
    # Test multiple critiques at once (new feature)
    print(f"\nTesting multiple critiques submission:")
    session_id2 = str(uuid.uuid4())
    tool.submit_reasoning(session_id2, reasoning)
    tool.get_persona_guidance(session_id2, personas)
    
    multiple_critiques = {
        personas[0]: f"Multi-critique from {personas[0]}",
        personas[1]: f"Multi-critique from {personas[1]}"
    }
    
    multi_result = tool.submit_critique(session_id2, personas[0], multiple_critiques[personas[0]], personas[1], multiple_critiques[personas[1]])
    
    multi_flow = (
        'error' not in multi_result and
        multi_result.get('critiques_complete') == True and
        multi_result.get('next_step') == 'synthesis' and
        multi_result.get('steps_completed') == 3
    )
    
    print(f"Multiple critiques at once: {'✅' if multi_flow else '❌'}")
    
    return complete_flow and multi_flow


if __name__ == "__main__":
    test1_success = test_persona_ranking_accuracy()
    test2_success = test_submit_reasoning_persona_options()
    test3_success = test_get_persona_guidance_validation()
    test4_success = test_new_critique_flow()
    
    print("\n" + "=" * 50)
    print("PERSONA SELECTION TEST SUMMARY")
    print("=" * 50)
    
    if test1_success and test2_success and test3_success and test4_success:
        print("🎉 All persona selection tests passed!")
        sys.exit(0)
    else:
        print("💥 Some persona selection tests failed!")
        print(f"  Ranking accuracy: {'✅' if test1_success else '❌'}")
        print(f"  Submit reasoning format: {'✅' if test2_success else '❌'}")
        print(f"  Guidance validation: {'✅' if test3_success else '❌'}")
        print(f"  New critique flow: {'✅' if test4_success else '❌'}")
        sys.exit(1) 