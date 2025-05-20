"""Counter-Pose Tool for RPT (Reasoning-through-Perspective-Transition) prompting."""

from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional, Any


class ResponseCache:
    """Cache for counter-pose responses to avoid redundant processing."""
    
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, query: str, domain: str, show_full_process: bool) -> Optional[Dict]:
        """Get a cached response if available."""
        cache_key = f"{query}|{domain}|{show_full_process}"
        return self.cache.get(cache_key)
    
    def set(self, query: str, domain: str, show_full_process: bool, response: Dict) -> None:
        """Cache a response for future use."""
        cache_key = f"{query}|{domain}|{show_full_process}"
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[cache_key] = response


class UsageLogger:
    """Logger for counter-pose tool usage and statistics."""
    
    def __init__(self, log_file="counter_pose_usage.log"):
        self.log_file = log_file
    
    def log_usage(self, domain: str, persona_pair: Tuple[str, str], query_length: int, contradictions_found: int) -> None:
        """Log usage of the counter-pose tool."""
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp},{domain},{persona_pair[0]},{persona_pair[1]},{query_length},{contradictions_found}\n")


class CounterPoseTool:
    """Implementation of the RPT (Reasoning-through-Perspective-Transition) technique."""
    
    def __init__(self):
        self.persona_pairs = self._load_persona_pairs()
        self.domain_keywords = self._generate_domain_keywords()
        self.cache = ResponseCache()
        self.logger = UsageLogger()
        
    def _load_persona_pairs(self) -> Dict[str, List[Tuple[str, str]]]:
        """Load predefined persona pairs for each domain."""
        return {
            "software_development": [
                ("Developer", "Security Expert"),
                ("Frontend Engineer", "UX Designer"),
                ("Performance Optimizer", "Maintainability Advocate"),
                ("Startup CTO", "Enterprise Architect")
            ],
            "digital_marketing": [
                ("Creative Director", "Analytics Specialist"),
                ("Brand Strategist", "Conversion Optimizer"),
                ("Social Media Expert", "SEO Specialist"),
                ("Traditional Marketer", "Growth Hacker")
            ],
            "visual_design": [
                ("UI Minimalist", "Feature-Rich Designer"),
                ("Brand Identity Expert", "User-Centered Designer"),
                ("Print Design Specialist", "Digital-First Designer"),
                ("Artistic Creative", "Data-Driven Designer")
            ],
            "product_strategy": [
                ("Customer Advocate", "Business Strategist"),
                ("Innovative Disruptor", "Market Researcher"),
                ("MVP Champion", "Quality Perfectionist"),
                ("Long-term Strategist", "Quick-to-Market Tactician")
            ]
        }
    
    def _generate_domain_keywords(self) -> Dict[str, List[str]]:
        """Generate keywords for domain detection."""
        return {
            "software_development": [
                "code", "programming", "develop", "software", "bug", "feature", 
                "app", "application", "engineer", "function", "class", "library",
                "API", "interface", "database", "algorithm", "architecture", "server",
                "client", "testing", "deployment", "DevOps", "git", "GitHub"
            ],
            "digital_marketing": [
                "marketing", "campaign", "audience", "conversion", "social media",
                "SEO", "PPC", "content", "email", "analytics", "ROI", "CPC", "CPA",
                "funnel", "leads", "engagement", "traffic", "CTR", "advertising",
                "brand", "competitors", "strategy", "targeting", "segmentation"
            ],
            "visual_design": [
                "design", "layout", "visual", "color", "typography", "UI", "UX",
                "user interface", "user experience", "wireframe", "prototype",
                "mockup", "branding", "logo", "illustration", "graphic", "aesthetic",
                "responsive", "mobile", "desktop", "theme", "style guide", "grid"
            ],
            "product_strategy": [
                "product", "market", "strategy", "roadmap", "customer", "MVP",
                "feature", "release", "launch", "pricing", "competitive", "analysis",
                "persona", "user story", "agile", "scrum", "sprint", "backlog",
                "stakeholder", "KPI", "metrics", "validation", "feedback", "iteration"
            ]
        }
    
    def _determine_domain(self, query: str) -> str:
        """Determine the domain of the query based on keyword matching."""
        # Count matches for each domain
        matches = {domain: 0 for domain in self.domain_keywords}
        for domain, domain_keywords in self.domain_keywords.items():
            for keyword in domain_keywords:
                if keyword.lower() in query.lower():
                    matches[domain] += 1
        
        # Return domain with most matches, default to product_strategy if no matches
        best_match = max(matches.items(), key=lambda x: x[1])
        return best_match[0] if best_match[1] > 0 else "product_strategy"
    
    def _select_persona_pair(self, domain: str) -> Tuple[str, str]:
        """Select an appropriate persona pair for the domain."""
        # For now, just select the first pair; this could be enhanced later
        return self.persona_pairs[domain][0]
    
    def _get_persona_icon(self, persona: str) -> str:
        """Get an icon for the persona."""
        persona_icons = {
            "developer": "👨‍💻",
            "security expert": "🔒",
            "frontend engineer": "🎨",
            "ux designer": "🧑‍🎨",
            "creative director": "🎭",
            "analytics specialist": "📊",
            "customer advocate": "👥",
            "business strategist": "📈",
        }
        
        # Default icon if not found
        return persona_icons.get(persona.lower(), "👤")
    
    def _format_response(self, persona: str, content: str) -> str:
        """Format the response with visual indicators based on persona type."""
        icon = self._get_persona_icon(persona)
        
        return f"\n{icon} {persona.upper()}'s Perspective:\n{'-' * 40}\n{content}\n{'-' * 40}\n"
    
    def _generate_perspective(self, query: str, persona: str) -> str:
        """Generate a response from the first persona's perspective.
        
        Note: In a real implementation, this would call an LLM with the appropriate prompt.
        """
        # This is a placeholder - in a real implementation, this would call an LLM
        return f"As {persona}, I recommend the following approach to your question about '{query}'..."
    
    def _generate_critique(self, query: str, first_perspective: str, persona: str) -> str:
        """Generate a critique from the second persona's perspective.
        
        Note: In a real implementation, this would call an LLM with the appropriate prompt.
        """
        # This is a placeholder - in a real implementation, this would call an LLM
        return f"As {persona}, I would challenge the previous perspective with these considerations..."
    
    def _identify_contradictions(self, first_perspective: str, critique: str) -> List[Dict]:
        """Identify key contradictions between perspectives.
        
        Note: In a real implementation, this would use more sophisticated analysis.
        """
        # Placeholder - in a real implementation, this would use NLP techniques
        return [
            {"point": "Some contradictory point", "perspective1": "View 1", "perspective2": "View 2"},
            {"point": "Another contradictory point", "perspective1": "View 1", "perspective2": "View 2"}
        ]
    
    def _resolve_contradiction(self, contradiction: Dict) -> Dict:
        """Resolve a contradiction between perspectives.
        
        Note: In a real implementation, this would call an LLM with the appropriate prompt.
        """
        # Placeholder - in a real implementation, this would call an LLM
        return {
            "point": contradiction["point"],
            "resolution": "A balanced view that addresses both perspectives",
            "rationale": "Explanation of why this resolution makes sense"
        }
    
    def _assess_confidence(self, resolutions: List[Dict]) -> str:
        """Assess confidence in the synthesized answer based on contradiction resolutions."""
        # Simple placeholder logic
        if len(resolutions) == 0:
            return "High"  # No contradictions to resolve
        elif len(resolutions) <= 2:
            return "Medium"  # Few contradictions
        else:
            return "Low"  # Many contradictions
    
    def _synthesize_answer(self, query: str, first_perspective: str, critique: str) -> Dict:
        """Synthesize a final answer from multiple perspectives.
        
        Note: In a real implementation, this would call an LLM with the appropriate prompt.
        """
        # Identify key contradictions
        contradictions = self._identify_contradictions(first_perspective, critique)
        
        # Resolve each contradiction
        resolutions = []
        for contradiction in contradictions:
            resolution = self._resolve_contradiction(contradiction)
            resolutions.append(resolution)
        
        # Generate synthesis with confidence assessment
        confidence = self._assess_confidence(resolutions)
        
        # In a real implementation, this would call an LLM to generate the synthesis
        synthesis = {
            "answer": f"After considering multiple perspectives on '{query}', the recommended approach is...",
            "confidence": confidence,
            "resolved_contradictions": resolutions if len(resolutions) > 0 else None
        }
        
        return synthesis
    
    def process_query(self, query: str, show_full_process: bool = False) -> Dict:
        """Process a query using the Counter-Pose technique."""
        # Check cache first
        domain = self._determine_domain(query)
        cached_response = self.cache.get(query, domain, show_full_process)
        if cached_response:
            return cached_response
        
        # Select appropriate persona pair for the domain
        persona_pair = self._select_persona_pair(domain)
        
        # Generate first perspective
        first_perspective = self._generate_perspective(query, persona_pair[0])
        
        # Generate critique from second perspective
        critique = self._generate_critique(query, first_perspective, persona_pair[1])
        
        # Synthesize final answer with confidence assessment
        synthesis = self._synthesize_answer(query, first_perspective, critique)
        
        # Log usage
        contradictions_found = len(synthesis.get("resolved_contradictions", []))
        self.logger.log_usage(domain, persona_pair, len(query), contradictions_found)
        
        # Prepare response
        result = {}
        if show_full_process:
            result = {
                "domain": domain,
                "personas": persona_pair,
                "first_perspective": self._format_response(persona_pair[0], first_perspective),
                "critique": self._format_response(persona_pair[1], critique),
                "synthesis": synthesis
            }
        else:
            result = {"synthesis": synthesis}
        
        # Cache the result
        self.cache.set(query, domain, show_full_process, result)
        
        return result

    def get_example_templates(self) -> Dict[str, Dict]:
        """Return example templates for common use cases."""
        return {
            "api_design": {
                "query": "What's the best way to design a REST API for my e-commerce app?",
                "personas": ["Backend Developer", "API Security Specialist"],
                "example_output": "After considering the Backend Developer's focus on flexibility and the API Security Specialist's emphasis on protection mechanisms, it's recommended to implement a REST API using OAuth 2.0 authentication, rate limiting, and comprehensive input validation while maintaining a logical resource hierarchy..."
            },
            "marketing_campaign": {
                "query": "How should I structure my email campaign for a new product launch?",
                "personas": ["Brand Strategist", "Conversion Optimizer"],
                "example_output": "A balanced approach would include a story-driven sequence that establishes brand values (per the Brand Strategist) while implementing clear CTAs and segmentation (per the Conversion Optimizer). Start with 3 teaser emails followed by a launch announcement and 2 follow-ups..."
            },
            "ui_redesign": {
                "query": "How should I approach redesigning our mobile app UI?",
                "personas": ["UI Minimalist", "Feature-Rich Designer"],
                "example_output": "The recommended approach is to start with a minimalist foundation that prioritizes core user flows, then strategically integrate additional features based on user research. This balances clean design principles with ensuring all valuable functionality remains accessible..."
            },
            "product_roadmap": {
                "query": "How should I prioritize features for our Q3 roadmap?",
                "personas": ["Customer Advocate", "Business Strategist"],
                "example_output": "Implement a weighted scoring model that assigns 40% to customer impact (addressing the Customer Advocate's concerns) and 60% to business metrics including revenue potential and strategic alignment (addressing the Business Strategist's perspective). This balanced approach ensures both user needs and business objectives drive priorities..."
            }
        }
