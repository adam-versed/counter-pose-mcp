"""Additional tests for Counter-Pose Tool."""
import sys
from src.mcp_server.counter_pose_tool import CounterPoseTool

def test_domain_detection():
    """Test domain detection for different queries."""
    tool = CounterPoseTool()
    
    # Test various queries and their expected domains
    test_cases = [
        ("How do I optimize my Python code for better performance?", "software_development"),
        ("What's the best way to increase my website's conversion rate?", "digital_marketing"),
        ("Should I use Material Design or develop a custom design system?", "visual_design"),
        ("How should I prioritize my product roadmap for the next quarter?", "product_strategy"),
        ("What's the best color scheme for my mobile app?", "visual_design"),
        ("How can I improve my SEO ranking?", "digital_marketing"),
        ("What architecture should I use for my microservices?", "software_development"),
        ("Should I launch an MVP or wait for a more polished product?", "product_strategy")
    ]
    
    print("TESTING DOMAIN DETECTION")
    print("=" * 40)
    
    all_passed = True
    for query, expected_domain in test_cases:
        detected_domain = tool.determine_domain(query)
        match = detected_domain == expected_domain
        if not match:
            all_passed = False
            
        print(f"Query: '{query[:50]}...'")
        print(f"Expected: {expected_domain}")
        print(f"Detected: {detected_domain}")
        print(f"Match: {'✅' if match else '❌'}")
        print("-" * 50)
    
    # Test persona pair availability for each domain
    print("\nTESTING PERSONA PAIRS AVAILABILITY")
    print("=" * 40)
    
    for domain in tool.persona_pairs.keys():
        pairs = tool.persona_pairs[domain]
        print(f"Domain: {domain}")
        print(f"Available pairs ({len(pairs)}):")
        for i, (persona1, persona2) in enumerate(pairs, 1):
            print(f"  {i}. {persona1} vs {persona2}")
        print("-" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = test_domain_detection()
    if success:
        print("\n✅ All domain detection tests passed!")
    else:
        print("\n❌ Some domain detection tests failed!")
        sys.exit(1)
