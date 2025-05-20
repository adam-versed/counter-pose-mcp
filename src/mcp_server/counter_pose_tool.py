"""Counter-Pose Tool for validating LLM reasoning through perspective transition."""

from datetime import datetime
import json
import re
from typing import Dict, List, Tuple, Optional, Any


class ResponseCache:
    """Cache for counter-pose responses to avoid redundant processing."""
    
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, reasoning: str, domain: str) -> Optional[Dict]:
        """Get a cached response if available."""
        # Use a hash of the reasoning as the key to avoid overly long keys
        cache_key = f"{hash(reasoning)}|{domain}"
        return self.cache.get(cache_key)
    
    def set(self, reasoning: str, domain: str, response: Dict) -> None:
        """Cache a response for future use."""
        cache_key = f"{hash(reasoning)}|{domain}"
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[cache_key] = response


class UsageLogger:
    """Logger for counter-pose tool usage and statistics."""
    
    def __init__(self, log_file="counter_pose_usage.log"):
        self.log_file = log_file
    
    def log_usage(self, domain: str, persona_pair: Tuple[str, str], reasoning_length: int, 
                  blind_spots_found: int, contradictions_found: int) -> None:
        """Log usage of the counter-pose reasoning validator."""
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp},{domain},{persona_pair[0]},{persona_pair[1]},"
                   f"{reasoning_length},{blind_spots_found},{contradictions_found}\n")


class CounterPoseTool:
    """Implementation of the RPT (Reasoning-through-Perspective-Transition) technique
    for validating LLM reasoning."""
    
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
    
    def _determine_domain(self, text: str) -> str:
        """Determine the domain of the reasoning based on keyword matching."""
        # Count matches for each domain
        matches = {domain: 0 for domain in self.domain_keywords}
        for domain, domain_keywords in self.domain_keywords.items():
            for keyword in domain_keywords:
                if keyword.lower() in text.lower():
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
    
    def _extract_query_from_reasoning(self, reasoning: str) -> str:
        """Extract the original query from the reasoning text.
        
        This is a simple implementation that looks for question marks or keywords.
        In a real implementation, this would use more sophisticated NLP.
        """
        # Look for sentences ending with question marks
        questions = re.findall(r'([^.!?]*\?)', reasoning)
        if questions:
            return questions[0].strip()
        
        # Look for sentences with query keywords
        query_keywords = ["ask", "query", "question", "wondering", "requested"]
        sentences = re.split(r'[.!?]', reasoning)
        for sentence in sentences:
            for keyword in query_keywords:
                if keyword in sentence.lower():
                    return sentence.strip()
        
        # Default to first 100 characters if we can't identify a clear query
        return reasoning[:100].strip() + "..."
    
    def _analyze_reasoning_structure(self, reasoning: str) -> Dict:
        """Analyze the structure of the reasoning.
        
        This identifies key components like claims, evidence, and logical steps.
        In a real implementation, this would use more sophisticated NLP.
        """
        # Simple structure analysis (placeholder)
        sentences = re.split(r'[.!?]', reasoning)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Identify potential claims (sentences with assertive language)
        claim_keywords = ["is", "are", "should", "must", "need", "conclude", "therefore", "thus"]
        claims = []
        for sentence in sentences:
            for keyword in claim_keywords:
                if f" {keyword} " in f" {sentence.lower()} ":
                    claims.append(sentence)
                    break
        
        # Identify potential evidence (sentences with supporting language)
        evidence_keywords = ["because", "since", "as", "evidence", "research", "study", "data", "example"]
        evidence = []
        for sentence in sentences:
            for keyword in evidence_keywords:
                if f" {keyword} " in f" {sentence.lower()} ":
                    evidence.append(sentence)
                    break
        
        # Identify potential assumptions (sentences with qualifying language)
        assumption_keywords = ["assume", "if", "may", "might", "could", "possibly", "perhaps", "likely"]
        assumptions = []
        for sentence in sentences:
            for keyword in assumption_keywords:
                if f" {keyword} " in f" {sentence.lower()} ":
                    assumptions.append(sentence)
                    break
        
        return {
            "total_sentences": len(sentences),
            "claims": claims,
            "evidence": evidence,
            "assumptions": assumptions
        }
    
    def _identify_blind_spots(self, reasoning: str, persona: str, domain: str) -> List[Dict]:
        """Identify blind spots in the reasoning from a particular persona's perspective.
        
        Note: In a real implementation, this would call an LLM with an appropriate prompt.
        """
        # This is a placeholder - in a real implementation, this would call an LLM
        # Pre-defined blind spots for each domain/persona combination
        common_blind_spots = {
            "software_development": {
                "Developer": ["scalability considerations", "technical debt implications"],
                "Security Expert": ["potential security vulnerabilities", "data privacy concerns"]
            },
            "digital_marketing": {
                "Creative Director": ["brand consistency issues", "emotional response factors"],
                "Analytics Specialist": ["conversion attribution", "statistical significance of data"]
            },
            "visual_design": {
                "UI Minimalist": ["information density trade-offs", "cognitive load"],
                "Feature-Rich Designer": ["discoverability issues", "feature prioritization"]
            },
            "product_strategy": {
                "Customer Advocate": ["user pain points", "accessibility considerations"],
                "Business Strategist": ["monetization challenges", "competitive positioning"]
            }
        }
        
        # Get relevant blind spots for the domain/persona
        relevant_blind_spots = []
        if domain in common_blind_spots and persona in common_blind_spots[domain]:
            potential_blind_spots = common_blind_spots[domain][persona]
            
            # Check if these blind spots are addressed in the reasoning
            for blind_spot in potential_blind_spots:
                if blind_spot.lower() not in reasoning.lower():
                    relevant_blind_spots.append({
                        "topic": blind_spot,
                        "explanation": f"The reasoning doesn't address {blind_spot}, which is important from a {persona}'s perspective."
                    })
        
        return relevant_blind_spots
    
    def _identify_contradictions(self, reasoning: str) -> List[Dict]:
        """Identify potential contradictions in the reasoning.
        
        Note: In a real implementation, this would use more sophisticated NLP or call an LLM.
        """
        # This is a placeholder - in a real implementation, this would use NLP techniques or call an LLM
        
        # Look for potential contradiction markers
        contradiction_markers = [
            "but",
            "however",
            "on the other hand",
            "conversely",
            "in contrast",
            "although",
            "nonetheless",
            "despite",
            "while",
            "yet"
        ]
        
        potential_contradictions = []
        sentences = re.split(r'[.!?]', reasoning)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        for i, sentence in enumerate(sentences):
            for marker in contradiction_markers:
                if f" {marker} " in f" {sentence.lower()} ":
                    # Found a potential contradiction marker
                    context = " ".join(sentences[max(0, i-1):min(len(sentences), i+2)])
                    potential_contradictions.append({
                        "marker": marker,
                        "context": context,
                        "explanation": f"Potential logical tension around '{marker}' statement"
                    })
                    break
        
        return potential_contradictions
    
    def _generate_critique(self, reasoning: str, structure_analysis: Dict, 
                          blind_spots: List[Dict], contradictions: List[Dict], 
                          persona: str) -> str:
        """Generate a critique of the reasoning from a specific persona's perspective.
        
        Note: In a real implementation, this would call an LLM with the appropriate prompt.
        """
        # This is a placeholder - in a real implementation, this would call an LLM
        
        critique_parts = []
        
        # Add introduction
        critique_parts.append(f"As a {persona}, I've analyzed the provided reasoning and identified several key points:")
        
        # Comment on reasoning structure
        if structure_analysis["claims"]:
            critique_parts.append("\nMain claims identified:")
            for i, claim in enumerate(structure_analysis["claims"][:3], 1):
                critique_parts.append(f"  {i}. \"{claim}\"")
        
        if blind_spots:
            critique_parts.append("\nPotential blind spots:")
            for i, spot in enumerate(blind_spots, 1):
                critique_parts.append(f"  {i}. {spot['explanation']}")
        
        if contradictions:
            critique_parts.append("\nPotential contradictions or tensions:")
            for i, contradiction in enumerate(contradictions, 1):
                critique_parts.append(f"  {i}. {contradiction['explanation']}")
        
        # Add a perspective-specific evaluation
        persona_perspectives = {
            "Developer": "technical implementation feasibility",
            "Security Expert": "security implications",
            "Creative Director": "brand alignment and creative impact",
            "Analytics Specialist": "measurable outcomes and data-driven insights",
            "UI Minimalist": "simplicity and usability",
            "Feature-Rich Designer": "functionality and feature completeness",
            "Customer Advocate": "user needs and pain points",
            "Business Strategist": "strategic alignment and business impact"
        }
        
        perspective = persona_perspectives.get(persona, "overall approach")
        critique_parts.append(f"\nFrom a {perspective} perspective, this reasoning is {self._generate_quality_assessment()}.")
        
        return "\n".join(critique_parts)
    
    def _generate_quality_assessment(self) -> str:
        """Generate a qualitative assessment of reasoning quality.
        This is a placeholder function that would be replaced with actual analysis in a real implementation.
        """
        import random
        assessments = [
            "generally sound but could be strengthened in specific areas",
            "missing some important considerations",
            "well-structured but contains some questionable assumptions",
            "strong in its logical flow but lacks supporting evidence in key areas",
            "focused on the right issues but may not have explored all implications"
        ]
        return random.choice(assessments)
    
    def _assess_confidence(self, blind_spots: List[Dict], contradictions: List[Dict]) -> str:
        """Assess confidence in the reasoning based on blind spots and contradictions."""
        total_issues = len(blind_spots) + len(contradictions)
        
        if total_issues == 0:
            return "High"
        elif total_issues <= 2:
            return "Medium"
        else:
            return "Low"
    
    def _synthesize_feedback(self, reasoning: str, query: str, 
                           critique1: str, critique2: str, 
                           blind_spots1: List[Dict], blind_spots2: List[Dict],
                           contradictions: List[Dict]) -> Dict:
        """Synthesize feedback on the reasoning from multiple perspectives.
        
        Note: In a real implementation, this would call an LLM with the appropriate prompt.
        """
        # Combine all blind spots and contradictions
        all_blind_spots = blind_spots1 + blind_spots2
        
        # Assess confidence
        confidence = self._assess_confidence(all_blind_spots, contradictions)
        
        # Determine if changes are needed
        changes_needed = confidence != "High"
        
        # Create recommendation
        if changes_needed:
            recommendation = "Consider revising your reasoning to address the identified blind spots and potential contradictions."
        else:
            recommendation = "Your reasoning appears sound from multiple perspectives. You may proceed with your current approach."
        
        # Detailed feedback
        feedback_points = []
        
        if all_blind_spots:
            feedback_points.append("Key blind spots to address:")
            for spot in all_blind_spots:
                feedback_points.append(f"- {spot['explanation']}")
        
        if contradictions:
            feedback_points.append("Potential contradictions to resolve:")
            for contradiction in contradictions:
                feedback_points.append(f"- {contradiction['explanation']}")
        
        if not feedback_points:
            feedback_points.append("No significant issues were identified with your reasoning.")
            
        return {
            "query": query,
            "confidence": confidence,
            "changes_needed": changes_needed,
            "recommendation": recommendation,
            "detailed_feedback": "\n".join(feedback_points),
            "blind_spots_count": len(all_blind_spots),
            "contradictions_count": len(contradictions)
        }
    
    def validate_reasoning(self, reasoning: str) -> Dict:
        """Validate a reasoning process using the Counter-Pose technique."""
        # Extract query from reasoning
        query = self._extract_query_from_reasoning(reasoning)
        
        # Determine domain
        domain = self._determine_domain(reasoning)
        
        # Check cache first
        cached_response = self.cache.get(reasoning, domain)
        if cached_response:
            return cached_response
        
        # Select appropriate persona pair for the domain
        persona_pair = self._select_persona_pair(domain)
        
        # Analyze reasoning structure
        structure_analysis = self._analyze_reasoning_structure(reasoning)
        
        # Identify blind spots from each persona's perspective
        blind_spots1 = self._identify_blind_spots(reasoning, persona_pair[0], domain)
        blind_spots2 = self._identify_blind_spots(reasoning, persona_pair[1], domain)
        
        # Identify contradictions
        contradictions = self._identify_contradictions(reasoning)
        
        # Generate critiques from each persona's perspective
        critique1 = self._generate_critique(
            reasoning, structure_analysis, blind_spots1, contradictions, persona_pair[0]
        )
        critique2 = self._generate_critique(
            reasoning, structure_analysis, blind_spots2, contradictions, persona_pair[1]
        )
        
        # Synthesize feedback
        synthesis = self._synthesize_feedback(
            reasoning, query, critique1, critique2, 
            blind_spots1, blind_spots2, contradictions
        )
        
        # Prepare response
        result = {
            "domain": domain,
            "personas": persona_pair,
            "first_critique": self._format_response(persona_pair[0], critique1),
            "second_critique": self._format_response(persona_pair[1], critique2),
            "synthesis": synthesis
        }
        
        # Log usage
        self.logger.log_usage(
            domain, 
            persona_pair, 
            len(reasoning),
            len(blind_spots1) + len(blind_spots2),
            len(contradictions)
        )
        
        # Cache the result
        self.cache.set(reasoning, domain, result)
        
        return result

    def get_example_templates(self) -> Dict[str, Dict]:
        """Return example templates for common reasoning validation scenarios."""
        return {
            "api_design_reasoning": {
                "reasoning": "I'm designing a REST API for an e-commerce app. I think we should use a standard CRUD approach with endpoints for products, orders, and users. We'll use JWT for authentication because it's stateless and scalable. I'll implement rate limiting to prevent abuse.",
                "example_output": "Your reasoning correctly addresses API design patterns and authentication, but misses security considerations like input validation and HTTPS enforcement. A Security Expert would recommend addressing these blind spots before proceeding."
            },
            "marketing_campaign_reasoning": {
                "reasoning": "For our new product launch email campaign, I'm planning a sequence of teasers followed by the main announcement. We'll segment users by past purchase behavior and send at optimal times. Content will focus on unique features and benefits.",
                "example_output": "Your campaign structure is solid from a Brand Strategist view, but an Analytics Specialist notes that you haven't specified success metrics or A/B testing strategy. Consider adding these elements before proceeding."
            },
            "ui_redesign_reasoning": {
                "reasoning": "For our mobile app redesign, I'm focusing on a minimalist approach with lots of whitespace, simplified navigation, and reduced cognitive load. We'll use a monochromatic color scheme with accent colors for key actions.",
                "example_output": "While your minimalist UI approach improves clarity, a Feature-Rich Designer would point out you haven't addressed how users will discover advanced functionality. Consider adding a progressive disclosure mechanism."
            },
            "product_roadmap_reasoning": {
                "reasoning": "For our Q3 roadmap, I'm prioritizing features based on engineering effort and technical dependencies. We should tackle the payment system upgrade first, then the reporting dashboard, and finally the mobile app enhancements.",
                "example_output": "Your technical sequencing makes sense, but a Customer Advocate would note you haven't mentioned how these priorities align with user needs. Consider incorporating user feedback and impact metrics into your prioritization approach."
            }
        }
