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
    
    for query, expected_domain in test_cases:
        detected_domain = tool._determine_domain(query)
        print(f"Query: '{query}'")
        print(f"Expected domain: {expected_domain}")
        print(f"Detected domain: {detected_domain}")
        print(f"Match: {'✅' if detected_domain == expected_domain else '❌'}")
        print("-" * 50)
        
    # Test persona selection for each domain
    for domain in tool.persona_pairs.keys():
        personas = tool._select_persona_pair(domain)
        print(f"Domain: {domain}")
        print(f"Selected personas: {personas[0]} vs {personas[1]}")
        print("-" * 50)
    
    # Test example templates
    templates = tool.get_example_templates()
    print("Example Templates:")
    for template_name, template_data in templates.items():
        print(f"Template: {template_name}")
        print(f"Query: {template_data['query']}")
        print(f"Personas: {' vs '.join(template_data['personas'])}")
        print("-" * 50)

if __name__ == "__main__":
    test_domain_detection()
