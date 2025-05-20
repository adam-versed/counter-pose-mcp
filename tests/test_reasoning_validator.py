"""Test the Counter-Pose reasoning validator functionality."""
import sys
from src.mcp_server.counter_pose_tool import CounterPoseTool

def test_reasoning_validator():
    """Test the basic functionality of the reasoning validator."""
    tool = CounterPoseTool()
    
    # Test examples across different domains
    test_cases = [
        # Software Development
        {
            "domain": "software_development",
            "reasoning": """
                I'm trying to decide on the best architecture for our new microservices. 
                I think we should use a REST-based approach with each service responsible for its own data.
                We'll use API gateways to handle authentication and routing. This will give us good scalability
                and allow teams to work independently. The services will communicate asynchronously using a
                message queue to reduce coupling.
            """
        },
        # Digital Marketing
        {
            "domain": "digital_marketing",
            "reasoning": """
                For our holiday campaign, I'm planning to focus primarily on email marketing and social media.
                We'll create a sequence of emails starting with teasers 2 weeks before the sale, then 
                announcements, then last-chance reminders. For social, we'll create shareable holiday-themed
                content that subtly promotes our products. I think this will maximize our existing audience
                engagement without requiring much additional ad spend.
            """
        },
        # Visual Design
        {
            "domain": "visual_design",
            "reasoning": """
                For our mobile app redesign, I'm considering a minimalist approach with a focus on typography
                and whitespace. We'll use a monochromatic color scheme with accent colors only for calls to action.
                The navigation will be simplified to just 3 main tabs with secondary actions in a hidden menu.
                This should reduce cognitive load and make the app feel more modern and clean.
            """
        },
        # Product Strategy
        {
            "domain": "product_strategy",
            "reasoning": """
                Looking at our product roadmap, I think we need to prioritize the reporting features over
                the collaboration tools. Our user research shows that customers are primarily using our product
                for data analysis, and the competition is catching up in this area. We can launch a basic
                version in Q2 and then iterate based on feedback. This approach minimizes risk while addressing
                our most pressing market threat.
            """
        }
    ]
    
    print("TESTING REASONING VALIDATOR ACROSS DOMAINS")
    print("==========================================")
    
    for test_case in test_cases:
        expected_domain = test_case["domain"]
        reasoning = test_case["reasoning"]
        
        # Detect domain
        detected_domain = tool._determine_domain(reasoning)
        print(f"\nDomain test - Expected: {expected_domain}, Detected: {detected_domain}")
        print(f"Match: {'✅' if detected_domain == expected_domain else '❌'}")
        
        # Run validation
        result = tool.validate_reasoning(reasoning)
        
        # Display key validation results
        print(f"\nValidating {detected_domain} reasoning:")
        print(f"Selected personas: {result['personas'][0]} vs {result['personas'][1]}")
        print(f"Confidence: {result['synthesis']['confidence']}")
        print(f"Changes needed: {result['synthesis']['changes_needed']}")
        print(f"Blind spots found: {result['synthesis']['blind_spots_count']}")
        print(f"Contradictions found: {result['synthesis']['contradictions_count']}")
        print(f"\nRecommendation: {result['synthesis']['recommendation']}")
        print(f"\nDetailed feedback: {result['synthesis']['detailed_feedback']}")
        print("\n" + "-" * 50)
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_reasoning_validator()
