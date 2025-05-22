"""Counter-Pose Tool for RPT (Reasoning-through-Perspective-Transition) prompted reasoning."""

from datetime import datetime
from typing import Dict, List, Optional, Tuple


class UsageLogger:
    """Logger for counter-pose tool usage and statistics."""

    def __init__(self, log_file: str = "/tmp/counter_pose_usage.log") -> None:
        self.log_file = log_file

    def log_usage(
        self, session_id: str, domain: str, persona: str, step: str, reasoning_length: int
    ) -> None:
        """Log usage of the counter-pose reasoning validator."""
        timestamp = datetime.now().isoformat()
        try:
            with open(self.log_file, "a") as f:
                f.write(f"{timestamp},{session_id},{domain},{persona},{step},{reasoning_length}\n")
        except OSError:
            pass  # Optionally, print a warning or log to console


class CounterPoseSession:
    """Represents an ongoing Counter-Pose RPT reasoning session."""

    def __init__(self, session_id: str, domain: Optional[str] = None) -> None:
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
            "changes_needed": self.changes_needed,
        }


class CounterPoseTool:
    """Implementation of the RPT (Reasoning-through-Perspective-Transition) technique
    for structured reasoning validation."""

    def __init__(self) -> None:
        self.sessions = {}
        self.domain_keywords = self._generate_domain_keywords()
        self.persona_pairs = self._load_persona_pairs()
        self.persona_keywords = self._generate_persona_keywords()
        self.logger = UsageLogger()
        self.persona_icons = {
            "developer": "👨‍💻",
            "security expert": "🔒",
            "frontend engineer": "🎨",
            "ux designer": "🧑‍🎨",
            "backend engineer": "⚙️",
            "devops engineer": "🔧",
            "performance engineer": "⚡",
            "maintainability advocate": "🧹",
            "creative director": "🎭",
            "analytics specialist": "📊",
            "social media expert": "📱",
            "growth hacker": "📈",
            "brand strategist": "🎯",
            "conversion optimizer": "💰",
            "content creator": "✍️",
            "performance marketer": "🎪",
            "b2b marketer": "🏢",
            "b2c marketer": "👥",
            "landing page expert": "🖥️",
            "seo specialist": "🔍",
            "ui minimalist": "⚪",
            "feature-rich designer": "🧩",
            "brand identity expert": "🏷️",
            "user-centered designer": "👤",
            "print design specialist": "📄",
            "digital-first designer": "💻",
            "artistic creative": "🎨",
            "data-driven designer": "📊",
            "accessibility expert": "♿",
            "visual artist": "🖼️",
            "customer advocate": "👥",
            "business strategist": "📈",
            "innovative disruptor": "💡",
            "market researcher": "📊",
            "mvp champion": "🚀",
            "quality perfectionist": "✨",
            "long-term strategist": "🔭",
            "quick-to-market tactician": "⚡",
            "technical pm": "⚙️",
            "business pm": "💼",
        }

    def _load_persona_pairs(self) -> Dict[str, List[Tuple[str, str]]]:
        """Load predefined persona pairs for each domain."""
        return {
            "software_development": [
                ("Developer", "Security Expert"),
                ("Frontend Engineer", "UX Designer"),
                ("Backend Engineer", "DevOps Engineer"),
                ("Performance Engineer", "Maintainability Advocate"),
            ],
            "digital_marketing": [
                ("Creative Director", "Analytics Specialist"),
                ("Brand Strategist", "Conversion Optimizer"),
                ("Social Media Expert", "Growth Hacker"),
                ("Content Creator", "Performance Marketer"),
                ("B2B Marketer", "B2C Marketer"),
                ("Landing Page Expert", "SEO Specialist"),
            ],
            "visual_design": [
                ("UI Minimalist", "Feature-Rich Designer"),
                ("Brand Identity Expert", "User-Centered Designer"),
                ("Print Design Specialist", "Digital-First Designer"),
                ("Artistic Creative", "Data-Driven Designer"),
                ("Accessibility Expert", "Visual Artist"),
            ],
            "product_strategy": [
                ("Customer Advocate", "Business Strategist"),
                ("Innovative Disruptor", "Market Researcher"),
                ("MVP Champion", "Quality Perfectionist"),
                ("Long-term Strategist", "Quick-to-Market Tactician"),
                ("Technical PM", "Business PM"),
            ],
        }

    def _generate_persona_keywords(self) -> Dict[str, Dict[str, List[str]]]:
        """Generate keywords for intelligent persona pair selection within domains."""
        return {
            "software_development": {
                "Developer,Security Expert": [
                    "security",
                    "vulnerability",
                    "auth",
                    "encryption",
                    "breach",
                    "privacy",
                    "compliance",
                ],
                "Frontend Engineer,UX Designer": [
                    "ui",
                    "interface",
                    "user experience",
                    "frontend",
                    "design",
                    "usability",
                    "accessibility",
                ],
                "Backend Engineer,DevOps Engineer": [
                    "infrastructure",
                    "deployment",
                    "server",
                    "database",
                    "scaling",
                    "devops",
                    "backend",
                ],
                "Performance Engineer,Maintainability Advocate": [
                    "performance",
                    "optimization",
                    "speed",
                    "maintainability",
                    "refactor",
                    "clean code",
                    "technical debt",
                ],
            },
            "digital_marketing": {
                "Social Media Expert,Growth Hacker": [
                    "social media",
                    "followers",
                    "engagement",
                    "platform",
                    "twitter",
                    "x.com",
                    "instagram",
                    "growth",
                ],
                "Creative Director,Analytics Specialist": [
                    "brand",
                    "creative",
                    "storytelling",
                    "analytics",
                    "metrics",
                    "campaign",
                    "creative direction",
                ],
                "Brand Strategist,Conversion Optimizer": [
                    "brand strategy",
                    "positioning",
                    "conversion",
                    "funnel",
                    "optimization",
                    "cro",
                ],
                "Content Creator,Performance Marketer": [
                    "content",
                    "organic",
                    "paid",
                    "advertising",
                    "content marketing",
                    "performance",
                ],
                "B2B Marketer,B2C Marketer": [
                    "b2b",
                    "b2c",
                    "enterprise",
                    "consumer",
                    "business",
                    "audience",
                ],
                "Landing Page Expert,SEO Specialist": [
                    "landing page",
                    "seo",
                    "search",
                    "website",
                    "page optimization",
                    "organic traffic",
                ],
            },
            "visual_design": {
                "UI Minimalist,Feature-Rich Designer": [
                    "minimalist",
                    "simple",
                    "clean",
                    "complex",
                    "feature-rich",
                    "functionality",
                ],
                "Brand Identity Expert,User-Centered Designer": [
                    "brand identity",
                    "logo",
                    "user-centered",
                    "user research",
                    "branding",
                ],
                "Print Design Specialist,Digital-First Designer": [
                    "print",
                    "digital",
                    "web",
                    "traditional",
                    "digital-first",
                ],
                "Artistic Creative,Data-Driven Designer": [
                    "artistic",
                    "creative",
                    "data-driven",
                    "analytics",
                    "metrics",
                    "testing",
                ],
                "Accessibility Expert,Visual Artist": [
                    "accessibility",
                    "a11y",
                    "visual",
                    "aesthetics",
                    "artistic",
                    "inclusive design",
                ],
            },
            "product_strategy": {
                "Customer Advocate,Business Strategist": [
                    "customer",
                    "user needs",
                    "business strategy",
                    "monetization",
                    "revenue",
                ],
                "Innovative Disruptor,Market Researcher": [
                    "innovation",
                    "disrupt",
                    "market research",
                    "validation",
                    "competitive analysis",
                ],
                "MVP Champion,Quality Perfectionist": [
                    "mvp",
                    "minimum viable",
                    "quality",
                    "perfectionist",
                    "launch",
                    "iteration",
                ],
                "Long-term Strategist,Quick-to-Market Tactician": [
                    "long-term",
                    "strategy",
                    "quick",
                    "tactical",
                    "roadmap",
                    "timeline",
                ],
                "Technical PM,Business PM": [
                    "technical",
                    "engineering",
                    "business",
                    "stakeholder",
                    "requirements",
                    "technical debt",
                ],
            },
        }

    def _generate_domain_keywords(self) -> Dict[str, List[str]]:
        """Generate keywords for domain detection."""
        return {
            "software_development": [
                "code",
                "programming",
                "develop",
                "software",
                "bug",
                "feature",
                "app",
                "application",
                "engineer",
                "function",
                "class",
                "library",
                "API",
                "interface",
                "database",
                "algorithm",
                "architecture",
                "server",
                "client",
                "testing",
                "deployment",
                "DevOps",
                "git",
                "GitHub",
                "authentication",
                "JWT",
                "tokens",
                "encryption",
                "security",
                "vulnerability",
                "auth",
                "login",
                "session",
                "oauth",
                "API key",
                "SSL",
                "TLS",
                "HTTPS",
                "implement",
                "privacy",
                "compliance",
            ],
            "digital_marketing": [
                "marketing",
                "campaign",
                "audience",
                "conversion",
                "social media",
                "SEO",
                "PPC",
                "content",
                "email",
                "analytics",
                "ROI",
                "CPC",
                "CPA",
                "funnel",
                "leads",
                "engagement",
                "traffic",
                "CTR",
                "advertising",
                "brand",
                "competitors",
                "strategy",
                "targeting",
                "segmentation",
            ],
            "visual_design": [
                "design",
                "layout",
                "visual",
                "color",
                "typography",
                "UI",
                "UX",
                "user interface",
                "user experience",
                "wireframe",
                "prototype",
                "mockup",
                "branding",
                "logo",
                "illustration",
                "graphic",
                "aesthetic",
                "responsive",
                "mobile",
                "desktop",
                "theme",
                "style guide",
                "grid",
                "material design",
                "design system",
                "custom design",
                "design patterns",
                "component library",
                "design tokens",
            ],
            "product_strategy": [
                "product",
                "market",
                "strategy",
                "roadmap",
                "customer",
                "MVP",
                "feature",
                "release",
                "launch",
                "pricing",
                "competitive",
                "analysis",
                "persona",
                "user story",
                "agile",
                "scrum",
                "sprint",
                "backlog",
                "stakeholder",
                "KPI",
                "metrics",
                "validation",
                "feedback",
                "iteration",
            ],
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

    def _rank_persona_pairs(
        self, domain: str, text: str
    ) -> List[Tuple[Tuple[str, str], float, str]]:
        """Rank persona pairs within a domain based on keyword matching."""
        pairs_with_scores = []
        domain_pairs = self.persona_keywords.get(domain, {})

        for pair_key, keywords in domain_pairs.items():
            persona_pair = tuple(pair_key.split(","))
            score = 0
            matched_keywords = []

            for keyword in keywords:
                if keyword.lower() in text.lower():
                    score += 1
                    matched_keywords.append(keyword)

            reason = (
                f"Matched keywords: {', '.join(matched_keywords)}"
                if matched_keywords
                else "General domain fit"
            )
            pairs_with_scores.append((persona_pair, score, reason))

        # Sort by score (highest first), then by pair order in original list
        pairs_with_scores.sort(key=lambda x: (-x[1], self.persona_pairs[domain].index(x[0])))
        return pairs_with_scores

    def init_session(self, session_id: str, initial_reasoning: str) -> Dict:
        """Initialize a new Counter-Pose session with persona options."""
        # Determine domain from initial reasoning
        domain = self.determine_domain(initial_reasoning)

        # Rank persona pairs for this domain and reasoning
        ranked_pairs = self._rank_persona_pairs(domain, initial_reasoning)

        # Create new session
        session = CounterPoseSession(session_id, domain)
        self.sessions[session_id] = session

        # Log usage
        self.logger.log_usage(
            session_id=session_id,
            domain=domain,
            persona="system",
            step="init",
            reasoning_length=len(initial_reasoning),
        )

        # Return session info with persona options
        return {
            "session_id": session_id,
            "domain": domain,
            "persona_options": [
                {"personas": list(pair), "score": score, "reason": reason, "recommended": i == 0}
                for i, (pair, score, reason) in enumerate(ranked_pairs)
            ],
            "next_step": "select_personas",
            "instructions": (
                "Choose a persona pair from the options above, or specify your own "
                "custom pair for this domain."
            ),
        }

    def select_personas(self, session_id: str, persona_pair: List[str]) -> Dict:
        """Select personas for the session and start the critique process."""
        # Get session
        session = self.sessions.get(session_id)
        if not session:
            return {"error": f"Session {session_id} not found"}

        # Validate persona pair
        if len(persona_pair) != 2:
            return {"error": "Persona pair must contain exactly 2 personas"}

        # Set personas for session
        session.personas = persona_pair
        session.current_persona_index = -1

        # Log usage
        self.logger.log_usage(
            session_id=session_id,
            domain=session.domain,
            persona="system",
            step="select_personas",
            reasoning_length=len(str(persona_pair)),
        )

        # Return first critique instructions
        return {
            "session_id": session_id,
            "domain": session.domain,
            "selected_personas": persona_pair,
            "next_persona": persona_pair[0],
            "next_step": "critique",
            "format": self._get_critique_format(persona_pair[0]),
            "total_steps": 3,  # Two critiques + synthesis
        }

    def _get_critique_format(self, persona: str) -> str:
        """Get formatting guidance for a specific persona's critique."""
        icon = self.get_persona_icon(persona)

        # Provide guidance based on persona type
        persona_guidance = {
            "developer": (
                "Focus on implementation feasibility, component design, and technical debt"
            ),
            "security expert": (
                "Focus on security vulnerabilities, data privacy, and regulatory compliance"
            ),
            "frontend engineer": (
                "Focus on frontend architecture, component design, "
                "and user interface implementation"
            ),
            "ux designer": "Focus on user experience, accessibility, and usability",
            "creative director": (
                "Focus on brand consistency, emotional impact, and creative storytelling"
            ),
            "analytics specialist": (
                "Focus on measurable outcomes, data validation, and statistical rigor"
            ),
            "ui minimalist": "Focus on simplicity, clarity, and cognitive load reduction",
            "feature-rich designer": (
                "Focus on functionality completeness, discoverability, and feature organization"
            ),
            "customer advocate": "Focus on user needs, pain points, and accessibility",
            "business strategist": (
                "Focus on strategic alignment, competitive positioning, and monetization"
            ),
        }

        guidance = persona_guidance.get(
            persona.lower(), "Consider the perspective's unique expertise"
        )

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
        session.steps.append(
            {
                "type": "critique",
                "persona": persona,
                "content": critique,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Update current persona index
        session.current_persona_index = session.personas.index(persona)

        # Log usage
        self.logger.log_usage(
            session_id=session_id,
            domain=session.domain,
            persona=persona,
            step="critique",
            reasoning_length=len(critique),
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
                "total_steps": len(session.personas) + 1,  # All critiques + synthesis
            }
        else:
            # All critiques done, move to synthesis
            return {
                "session_id": session_id,
                "domain": session.domain,
                "current_step": critiques_count,
                "next_step": "synthesis",
                "format": self._get_synthesis_format(session),
                "total_steps": len(session.personas) + 1,  # All critiques + synthesis
            }

    def _get_synthesis_format(self, session: CounterPoseSession) -> str:
        """Get formatting guidance for the synthesis step."""
        personas_list = " and ".join(session.personas)
        return f"""
            SYNTHESIS OF PERSPECTIVES:

            After considering the critiques from {personas_list}, 
            synthesize a balanced recommendation.

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
        session.steps.append(
            {"type": "synthesis", "content": synthesis, "timestamp": datetime.now().isoformat()}
        )

        # Log usage
        self.logger.log_usage(
            session_id=session_id,
            domain=session.domain,
            persona="synthesizer",
            step="synthesis",
            reasoning_length=len(synthesis),
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
            "session_summary": session.to_dict(),
        }
