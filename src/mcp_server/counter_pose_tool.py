"""Counter-Pose Tool for RPT (Reasoning-through-Perspective-Transition) prompted reasoning."""

from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional, Any


class UsageLogger:
    """Logger for counter-pose tool usage and statistics."""
    
    def __init__(self, log_file="/tmp/counter_pose_usage.log"):
        self.log_file = log_file
    
    def log_usage(self, session_id: str, domain: str, persona: str, 
                 step: str, reasoning_length: int) -> None:
        """Log usage of the counter-pose reasoning validator."""
        timestamp = datetime.now().isoformat()
        try:
            with open(self.log_file, "a") as f:
                f.write(f"{timestamp},{session_id},{domain},{persona},{step},{reasoning_length}\n")
        except OSError:
            pass  # Optionally, print a warning or log to console


class CounterPoseSession:
    """Represents an ongoing Counter-Pose RPT reasoning session."""
    
    def __init__(self, session_id: str, domain: str = None):
        self.session_id = session_id
        self.domain = domain
        self.personas = []
        self.current_persona_index = -1
        self.steps = []
        self.started_at = datetime.now().isoformat()
        self.domain_keywords = {}
        self.available_personas = {}
        self.confidence = None
        self.changes_needed = None
        self.blind_spots = []
        self.contradictions = []
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "domain": self.domain,
            "personas": self.personas,
            "current_persona_index": self.current_persona_index,
            "steps": self.steps,
            "started_at": self.started_at,
            "completed_steps": len(self.steps),
            "blind_spots": self.blind_spots,
            "contradictions": self.contradictions,
            "confidence": self.confidence,
            "changes_needed": self.changes_needed
        }


class CounterPoseTool:
    """Implementation of the RPT (Reasoning-through-Perspective-Transition) technique
    for structured reasoning validation."""
    
    def __init__(self):
        self.sessions = {}
        self.domain_keywords = self._generate_domain_keywords()
        self.persona_pairs = self._load_persona_pairs()
        self.logger = UsageLogger()
        self.persona_icons = {
            "developer": "👨‍💻",
            "security expert": "🔒",
            "frontend engineer": "🎨",
            "ux designer": "🧑‍🎨",
            "creative director": "🎭",
            "analytics specialist": "📊",
            "ui minimalist": "🔍",
            "feature-rich designer": "🧩",
            "customer advocate": "👥",
            "business strategist": "📈",
            "innovative disruptor": "💡",
            "market researcher": "📊",
            "mvp champion": "🚀",
            "quality perfectionist": "✨",
            "long-term strategist": "🔭",
            "quick-to-market tactician": "⚡"
        }
    
    def _load_persona_pairs(self) -> Dict[str, List[Tuple[str, str]]]:
        """Load predefined persona pairs for each domain."""
        return {
            "software_development": [
                ("Developer", "Solution Architect"),
                ("Frontend Engineer", "UX Designer"),
                ("Solution Architect", "Security Expert"),
                ("Performance Optimizer", "Maintainability Advocate"),
                ("Solution Architect", "Startup CTO")
            ],
            "digital_marketing": [
                ("Creative Director", "Analytics Specialist"),
                ("Brand Strategist", "Conversion Optimizer"),
                ("Social Media Expert", "Growth Hacker"),
                ("Landing Page Expert", "SEO Specialist")
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
    
    def get_persona_icon(self, persona: str) -> str:
        """Get an icon for the persona."""
        return self.persona_icons.get(persona.lower(), "👤")
    
    def determine_domain(self, text: str) -> str:
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
    
    def select_persona_pair(self, domain: str) -> Tuple[str, str]:
        """Select an appropriate persona pair for the domain."""
        # For now, just select the first pair
        return self.persona_pairs[domain][0]
    
    def init_session(self, session_id: str, initial_reasoning: str) -> Dict:
        """Initialize a new Counter-Pose session."""
        # Determine domain from initial reasoning
        domain = self.determine_domain(initial_reasoning)
        
        # Create new session
        session = CounterPoseSession(session_id, domain)
        
        # Select persona pair for this domain
        persona_pair = self.select_persona_pair(domain)
        session.personas = list(persona_pair)
        
        # Store session
        self.sessions[session_id] = session
        
        # Log usage
        self.logger.log_usage(
            session_id=session_id,
            domain=domain,
            persona="system",
            step="init",
            reasoning_length=len(initial_reasoning)
        )
        
        # Return session info
        return {
            "session_id": session_id,
            "domain": domain,
            "personas": persona_pair,
            "next_persona": persona_pair[0],
            "next_step": "first_critique",
            "format": self._get_critique_format(persona_pair[0]),
            "total_steps": 3  # Initial critique, counter critique, synthesis
        }
    
    def _get_critique_format(self, persona: str) -> str:
        """Get formatting guidance for a specific persona's critique."""
        icon = self.get_persona_icon(persona)
        
        # Provide guidance based on persona type
        persona_guidance = {
            "developer": "Focus on implementation feasibility, component design, and technical debt",
            "security expert": "Focus on security vulnerabilities, data privacy, and regulatory compliance",
            "frontend engineer": "Focus on frontend architecture, component design, and user interface implementation",
            "ux designer": "Focus on user experience, accessibility, and usability",
            "creative director": "Focus on brand consistency, emotional impact, and creative storytelling",
            "analytics specialist": "Focus on measurable outcomes, data validation, and statistical rigor",
            "ui minimalist": "Focus on simplicity, clarity, and cognitive load reduction",
            "feature-rich designer": "Focus on functionality completeness, discoverability, and feature organization",
            "customer advocate": "Focus on user needs, pain points, and accessibility",
            "business strategist": "Focus on strategic alignment, competitive positioning, and monetization"
        }
        
        guidance = persona_guidance.get(persona.lower(), "Consider the perspective's unique expertise")
        
        return f"""
            As {persona}, critique the reasoning from your specific perspective.

            {guidance}

            Identify:
            1. Key claims that need examination
            2. Potential blind spots or unconsidered factors
            3. Logical contradictions or tensions
            4. Alternative approaches worth considering

            Format your critique as:

            {icon} {persona.upper()}'s CRITIQUE:
            <Your critique here>

            END CRITIQUE
            """
    
    def submit_critique(self, session_id: str, persona: str, critique: str) -> Dict:
        """Submit a critique from a specific persona."""
        # Get session
        session = self.sessions.get(session_id)
        if not session:
            return {"error": f"Session {session_id} not found"}
        
        # Validate persona
        if persona not in session.personas:
            return {"error": f"Persona {persona} not part of this session"}
        
        # Add step to session history
        session.steps.append({
            "type": "critique",
            "persona": persona,
            "content": critique,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update current persona index
        session.current_persona_index = session.personas.index(persona)
        
        # Log usage
        self.logger.log_usage(
            session_id=session_id,
            domain=session.domain,
            persona=persona,
            step="critique",
            reasoning_length=len(critique)
        )
        
        # Determine next step
        critiques_count = len([s for s in session.steps if s["type"] == "critique"])
        
        if critiques_count < len(session.personas):
            # More personas need to critique
            next_persona_index = (session.current_persona_index + 1) % len(session.personas)
            next_persona = session.personas[next_persona_index]
            
            return {
                "session_id": session_id,
                "domain": session.domain,
                "current_step": critiques_count,
                "next_persona": next_persona,
                "next_step": "critique",
                "format": self._get_critique_format(next_persona),
                "total_steps": len(session.personas) + 1  # All critiques + synthesis
            }
        else:
            # All critiques done, move to synthesis
            return {
                "session_id": session_id,
                "domain": session.domain,
                "current_step": critiques_count,
                "next_step": "synthesis",
                "format": self._get_synthesis_format(session),
                "total_steps": len(session.personas) + 1  # All critiques + synthesis
            }
    
    def _get_synthesis_format(self, session: CounterPoseSession) -> str:
        """Get formatting guidance for the synthesis step."""
        return f"""
            SYNTHESIS OF PERSPECTIVES:

            After considering the critiques from {" and ".join(session.personas)}, synthesize a balanced recommendation.

            Your synthesis should:
            1. Identify key blind spots raised by each perspective
            2. Note any contradictions between perspectives
            3. Provide a confidence assessment (High/Medium/Low)
            4. Recommend whether changes are needed to the original reasoning
            5. Offer specific recommendations for improvement

            Format your synthesis as:

            BLIND SPOTS IDENTIFIED:
            <List of blind spots>

            CONTRADICTIONS FOUND:
            <List of contradictions>

            CONFIDENCE: <High/Medium/Low>

            CHANGES NEEDED: <Yes/No>

            RECOMMENDATION:
            <Your synthesized recommendation>

            END SYNTHESIS
            """
    
    def submit_synthesis(self, session_id: str, synthesis: str) -> Dict:
        """Submit the final synthesis for a session."""
        # Get session
        session = self.sessions.get(session_id)
        if not session:
            return {"error": f"Session {session_id} not found"}
        
        # Add synthesis to session history
        session.steps.append({
            "type": "synthesis",
            "content": synthesis,
            "timestamp": datetime.now().isoformat()
        })
        
        # Log usage
        self.logger.log_usage(
            session_id=session_id,
            domain=session.domain,
            persona="synthesizer",
            step="synthesis",
            reasoning_length=len(synthesis)
        )
        
        # Extract metadata (this would normally be done by the calling LLM,
        # but we'll do simple extraction for testing purposes)
        
        # Extract confidence
        if "CONFIDENCE: High" in synthesis:
            session.confidence = "High"
        elif "CONFIDENCE: Medium" in synthesis:
            session.confidence = "Medium"
        else:
            session.confidence = "Low"
            
        # Extract changes needed
        session.changes_needed = "CHANGES NEEDED: Yes" in synthesis
        
        # Return session summary
        return {
            "session_id": session_id,
            "domain": session.domain,
            "personas": session.personas,
            "steps_completed": len(session.steps),
            "complete": True,
            "confidence": session.confidence,
            "changes_needed": session.changes_needed,
            "session_summary": session.to_dict()
        }
    
    def get_session(self, session_id: str) -> Dict:
        """Get information about a session."""
        session = self.sessions.get(session_id)
        if not session:
            return {"error": f"Session {session_id} not found"}
        
        return session.to_dict()
    
    def get_example_templates(self) -> Dict[str, Dict]:
        """Return example templates for common reasoning validation scenarios."""
        return {
            "api_design_reasoning": {
                "initial_reasoning": "I'm designing a REST API for an e-commerce app. I think we should use a standard CRUD approach with endpoints for products, orders, and users. We'll use JWT for authentication because it's stateless and scalable. I'll implement rate limiting to prevent abuse.",
                "domain": "software_development",
                "personas": ["Developer", "Security Expert"],
                "example_critiques": {
                    "Developer": "From a development perspective, the proposed API design lacks consideration for versioning and scalability. While the CRUD approach is solid, we should consider using GraphQL for complex queries to reduce over-fetching. The JWT implementation needs more specifics about token management and refresh mechanisms.",
                    "Security Expert": "The security considerations are insufficient. Storing JWTs in local storage exposes them to XSS attacks. We should use httpOnly cookies. Additionally, no mention of input validation, HTTPS enforcement, or OWASP top 10 mitigations. Rate limiting is good but needs IP-based limits to prevent distributed attacks."
                }
            },
            "marketing_campaign_reasoning": {
                "initial_reasoning": "For our new product launch email campaign, I'm planning a sequence of teasers followed by the main announcement. We'll segment users by past purchase behavior and send at optimal times. Content will focus on unique features and benefits.",
                "domain": "digital_marketing",
                "personas": ["Creative Director", "Analytics Specialist"],
                "example_critiques": {
                    "Creative Director": "The campaign lacks a unified creative vision and emotional hook. While feature-focused content is important, we need a compelling story that connects with our audience on an emotional level. The brand voice isn't addressed at all, and there's no mention of visual consistency across touchpoints.",
                    "Analytics Specialist": "The measurement strategy is missing entirely. What KPIs will determine success? How will we attribute conversions across the email sequence? The segmentation approach is vague—we need specific criteria and control groups to validate effectiveness. A/B testing plan should be included for subject lines and CTAs."
                }
            }
        }
        
    def get_domains(self) -> Dict[str, List[str]]:
        """Get available domains and their keywords."""
        return self.domain_keywords
    
    def get_personas(self) -> Dict[str, List[Tuple[str, str]]]:
        """Get available persona pairs for each domain."""
        return self.persona_pairs
