"""Comprehensive reasoning tests for the Counter-Pose MCP Server.

This file contains realistic reasoning examples for each domain to test
the reasoning validation capabilities of the Counter-Pose tool.
"""

import json
import sys
import os
from src.mcp_server.counter_pose_tool import CounterPoseTool

# Initialize the Counter-Pose tool
tool = CounterPoseTool()

# Set of test cases organized by domain
TEST_CASES = {
    # DOMAIN: SOFTWARE DEVELOPMENT
    "software_development": [
        {
            "title": "Authentication Implementation",
            "reasoning": """
            For the authentication system in our SaaS application, I've decided to implement JWT-based authentication.
            The flow will be:
            1. User logs in with username/password
            2. Server validates credentials and issues a JWT token
            3. Token is stored in browser local storage
            4. Token is sent with each API request in the Authorization header
            5. Server validates the token on each request
            
            I chose JWT because it's stateless, which scales well with our microservices architecture. Tokens will
            expire after 24 hours, which balances security and user convenience. This approach is also simple to
            implement and has good library support in our tech stack.
            """
        },
        {
            "title": "Database Selection",
            "reasoning": """
            We need to select a database for our new product analytics service. After considering our requirements,
            I believe MongoDB is the best choice. Our data has a variable schema since different products have 
            different event structures. MongoDB's flexible document model will handle this well.
            
            Performance is critical for this service since we'll be processing millions of events daily. MongoDB's
            horizontal scaling will help us handle growth. We also need to run complex aggregations for analytics
            dashboards, which MongoDB's aggregation pipeline supports well.
            
            Implementation-wise, our team already has experience with MongoDB, which will speed up development.
            The service will primarily be write-heavy (logging events) with occasional complex reads (generating
            reports), which aligns well with MongoDB's strengths.
            """
        }
    ],
    
    # DOMAIN: DIGITAL MARKETING
    "digital_marketing": [
        {
            "title": "Content Marketing Strategy",
            "reasoning": """
            For our B2B SaaS product's content marketing strategy, I recommend focusing on creating in-depth
            guides and case studies rather than more frequent, shorter blog posts. Our target audience is
            enterprise IT managers who are looking for comprehensive solutions and proof points.
            
            The content calendar should include:
            - 2 detailed guides per quarter on industry challenges
            - 1 case study per month highlighting customer success
            - Quarterly webinars with industry experts
            
            We should distribute this content through LinkedIn and industry newsletters rather than Twitter
            or Facebook, as our analytics show that's where our audience engages. This approach will generate
            fewer but higher quality leads compared to a high-volume approach that targets a broader audience.
            """
        },
        {
            "title": "Ad Campaign Budget Allocation",
            "reasoning": """
            For our upcoming product launch, I'm planning to allocate 60% of our budget to Google Ads, 30% to 
            LinkedIn, and 10% to retargeting campaigns. Google Ads will focus on search terms with high purchase
            intent, while LinkedIn will target job titles and industries that match our ideal customer profile.
            
            My reasoning for this split is based on historical performance data. Google Ads has consistently
            delivered the lowest cost per acquisition, while LinkedIn, though more expensive, brings in higher
            value customers. Retargeting has shown good results for converting users who visited our site but
            didn't sign up.
            
            We'll measure success primarily through sales qualified leads (SQLs) generated rather than click-through
            rates or impressions since that aligns better with revenue impact.
            """
        }
    ],
    
    # DOMAIN: VISUAL DESIGN
    "visual_design": [
        {
            "title": "Mobile App Design System",
            "reasoning": """
            For our mobile app redesign, I'm proposing we create a minimalist design system focused on clarity
            and ease of use. The core elements will include:
            
            1. Typography: A single sans-serif family (SF Pro) with 3 weights and 4 size levels
            2. Color: A monochromatic blue scheme with one accent color (orange) reserved for CTAs only
            3. Components: Simplified versions of our current components with consistent spacing rules
            4. Icons: Line-style icons with a uniform stroke width
            
            This approach will reduce visual noise and help users focus on their tasks. It also improves our
            development efficiency since there will be fewer custom components to build and maintain. The design
            will be distinctly ours through the unique combination of these elements rather than through complex
            individual elements.
            """
        },
        {
            "title": "Website Navigation Redesign",
            "reasoning": """
            For our e-commerce website navigation redesign, I'm planning to simplify the current 7-level deep
            category structure to a 3-level hierarchy. User testing showed that customers rarely navigate beyond
            the third level, instead preferring to use search or filters.
            
            The main navigation will be horizontal with dropdown menus for second-level categories. This matches
            the mental model our users demonstrated in card sorting sessions. Key categories will have visual
            icons to improve scanning.
            
            Mobile navigation will use a hamburger menu with expanded sections rather than our current approach
            of showing all categories at once. This will improve load time and reduce scrolling.
            
            I'll use the same typography and color scheme as the rest of the site to maintain brand consistency,
            with slight emphasis changes to improve wayfinding.
            """
        }
    ],
    
    # DOMAIN: PRODUCT STRATEGY
    "product_strategy": [
        {
            "title": "Feature Prioritization",
            "reasoning": """
            For our Q3 roadmap, I've decided to prioritize developing the team collaboration features over the
            advanced reporting dashboard. While both features have been requested by customers, the collaboration
            features address a more critical pain point according to our customer interviews.
            
            Additionally, our main competitor just released enhanced reporting features, but their collaboration
            capabilities remain weak. By focusing on collaboration, we can maintain a distinctive value proposition.
            
            From a technical perspective, the collaboration features will take approximately 6 weeks to develop
            with our current team, while the reporting dashboard would require 8-10 weeks. This means we can
            deliver value to customers sooner and potentially still complete the dashboard before the end of Q3.
            
            The collaboration features also have a clearer monetization path as they will be part of our premium
            tier, potentially driving upgrades from current users.
            """
        },
        {
            "title": "Market Expansion Strategy",
            "reasoning": """
            I believe we should expand into the European market before exploring opportunities in Asia.
            Europe represents a lower-risk opportunity for several reasons:
            
            1. Cultural and business practices are more similar to our current US market
            2. We already have a small base of European customers who found us organically
            3. Our product already meets GDPR requirements after our compliance work last year
            4. The competitive landscape is less saturated than in our US market
            
            My proposed approach is to start with the UK, Germany, and France, which represent the largest
            addressable markets for our product category. We should localize the product for these markets
            in Q1, then establish a small sales presence in London in Q2.
            
            This approach allows us to test our international operations with relatively low investment before
            considering the more complex Asian markets, which would require more significant localization and
            different go-to-market strategies.
            """
        }
    ]
}

def run_test(domain, test_case):
    """Run a single test case for a specific domain."""
    title = test_case["title"]
    reasoning = test_case["reasoning"]
    
    print(f"\n{'-' * 80}")
    print(f"TESTING: {domain.upper()} - {title}")
    print(f"{'-' * 80}")
    
    # Detect domain to verify accuracy
    detected_domain = tool._determine_domain(reasoning)
    print(f"Domain detection - Expected: {domain}, Detected: {detected_domain}")
    print(f"Match: {'✅' if detected_domain == domain else '❌'}")
    
    # Run validation
    start_time = __import__('time').time()
    result = tool.validate_reasoning(reasoning)
    end_time = __import__('time').time()
    
    # Display result summary
    print(f"\nValidation completed in {(end_time - start_time):.2f} seconds")
    print(f"Selected personas: {result['personas'][0]} vs {result['personas'][1]}")
    
    # Display synthesis results
    synthesis = result["synthesis"]
    print(f"\nCONFIDENCE: {synthesis['confidence']}")
    print(f"CHANGES NEEDED: {synthesis['changes_needed']}")
    print(f"BLIND SPOTS: {synthesis['blind_spots_count']}")
    print(f"CONTRADICTIONS: {synthesis['contradictions_count']}")
    
    # Display the detailed results
    print("\nRECOMMENDATION:")
    print(f"{synthesis['recommendation']}")
    
    print("\nDETAILED FEEDBACK:")
    print(f"{synthesis['detailed_feedback']}")
    
    # Display the first critique
    print("\nFIRST CRITIQUE:")
    print(f"{result['first_critique']}")
    
    # Display the second critique
    print("\nSECOND CRITIQUE:")
    print(f"{result['second_critique']}")
    
    return result

def main():
    """Run all tests or a specific domain if specified."""
    # Check if a specific domain was requested
    if len(sys.argv) > 1 and sys.argv[1] in TEST_CASES:
        domains_to_test = [sys.argv[1]]
    else:
        domains_to_test = TEST_CASES.keys()
    
    # Run tests for each domain
    results = {}
    for domain in domains_to_test:
        domain_results = []
        print(f"\n{'=' * 80}")
        print(f"TESTING DOMAIN: {domain.upper()}")
        print(f"{'=' * 80}")
        
        for test_case in TEST_CASES[domain]:
            result = run_test(domain, test_case)
            domain_results.append({
                "title": test_case["title"],
                "confidence": result["synthesis"]["confidence"],
                "changes_needed": result["synthesis"]["changes_needed"],
                "blind_spots": result["synthesis"]["blind_spots_count"],
                "contradictions": result["synthesis"]["contradictions_count"]
            })
        
        results[domain] = domain_results
    
    # Print summary of all tests
    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for domain, domain_results in results.items():
        print(f"\n{domain.upper()}")
        print("-" * 40)
        
        for result in domain_results:
            status = "❌ Changes needed" if result["changes_needed"] else "✅ No changes needed"
            print(f"{result['title']}: {result['confidence']} confidence, {status}")
            print(f"  Blind spots: {result['blind_spots']}, Contradictions: {result['contradictions']}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
