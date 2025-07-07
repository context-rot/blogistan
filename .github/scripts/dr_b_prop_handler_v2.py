#!/usr/bin/env python3
"""
Dr. B. Prop - Advanced Contextual Research Response Handler v2.0

Enhanced with:
- Multi-turn conversation context
- Paper content analysis and understanding
- Advanced research capabilities with multiple sources
- More sophisticated snark and personality
- DSPy 3.0 optimization patterns
- Intelligent conversation flow management
"""

import os
import sys
import json
import re
import subprocess
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Tuple, List, Optional, Union
import requests
from bs4 import BeautifulSoup
import dspy
from dataclasses import dataclass
from intelligent_jest_engine import (
    IntelligentJestEngine,
    DSPyJestOptimizer,
    JestContext,
)


@dataclass
class ConversationContext:
    """Context for multi-turn conversations."""

    paper_url: str
    paper_title: str
    paper_content: str
    line_number: Optional[int]
    conversation_history: List[Dict[str, Any]]
    user_profile: Dict[str, Any]
    research_context: str
    selected_text: str = ""
    user_feedback: str = ""


@dataclass
class ResearchAnalysis:
    """Structured research analysis with citations and depth."""

    research_quality_score: float
    academic_references: List[str]
    key_insights: List[str]
    contradictory_evidence: List[str]
    research_gaps: List[str]
    methodological_concerns: List[str]


@dataclass
class SnarkProfile:
    """Dr. B. Prop's snark configuration based on context."""

    snark_level: float  # 0-1
    academic_pretension: float  # 0-1
    methodological_criticism: float  # 0-1
    intellectual_superiority: float  # 0-1
    conversational_hooks: List[str]


class AdvancedResearchAgent(dspy.Module):
    """DSPy 3.0 agent for sophisticated research and response generation."""

    def __init__(self):
        super().__init__()
        self.context_analyzer = dspy.ChainOfThought(
            "conversation_context -> contextual_analysis"
        )
        self.research_planner = dspy.ChainOfThought(
            "contextual_analysis, paper_content -> research_plan"
        )
        self.deep_researcher = dspy.ChainOfThought(
            "research_plan, external_sources -> research_synthesis"
        )
        self.personality_profiler = dspy.ChainOfThought(
            "conversation_context, user_input -> personality_response_profile"
        )
        self.response_crafter = dspy.ChainOfThought(
            "research_synthesis, personality_profile, conversation_hooks -> crafted_response"
        )

    def forward(
        self,
        conversation_context: str,
        paper_content: str,
        external_research: str,
        user_input: str,
    ):
        """Generate sophisticated contextualized response."""

        # Analyze conversation context
        context_analysis = self.context_analyzer(
            conversation_context=conversation_context
        )

        # Plan research approach
        research_plan = self.research_planner(
            contextual_analysis=context_analysis.contextual_analysis,
            paper_content=paper_content,
        )

        # Synthesize research
        research_synthesis = self.deep_researcher(
            research_plan=research_plan.research_plan,
            external_sources=external_research,
        )

        # Profile personality response
        personality_profile = self.personality_profiler(
            conversation_context=conversation_context, user_input=user_input
        )

        # Craft final response
        response = self.response_crafter(
            research_synthesis=research_synthesis.research_synthesis,
            personality_profile=personality_profile.personality_response_profile,
            conversation_hooks=self._generate_conversation_hooks(user_input),
        )

        return response

    def _generate_conversation_hooks(self, user_input: str) -> str:
        """Generate conversation hooks to encourage multi-turn interaction."""
        hooks = [
            "What are your thoughts on the methodological implications?",
            "Have you considered the broader theoretical framework?",
            "I'm curious about your perspective on the epistemological foundations...",
            "What's your take on the peer review methodology here?",
            "Do you think the empirical evidence supports this approach?",
            "How does this align with your experience in the field?",
            "What would be your next research question?",
        ]
        return "; ".join(hooks[:2])  # Return 2 relevant hooks


class ContextualDrBProp:
    """Enhanced Dr. B. Prop with full contextual awareness and research capabilities."""

    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        self.perplexity_key = os.environ.get("PERPLEXITY_API_KEY") or os.environ.get(
            "PPLX_API_KEY"
        )
        self.repository = os.environ.get("GITHUB_REPOSITORY")

        # Initialize DSPy 3.0 with available LM - prioritize OpenRouter with GPT-4
        self.research_agent = None
        self.jest_engine = None

        if self.openrouter_key:
            try:
                # Configure DSPy for jesting
                DSPyJestOptimizer.configure_for_jesting(self.openrouter_key)

                self.research_agent = AdvancedResearchAgent()
                self.jest_engine = IntelligentJestEngine()
                print(
                    "DSPy initialized with OpenRouter GPT-4.1-mini + Intelligent Jest Engine"
                )
            except Exception as e:
                print(f"DSPy OpenRouter initialization error: {e}")
        elif self.anthropic_key:
            try:
                lm = dspy.LM(
                    model="anthropic/claude-3-5-sonnet-20241022",
                    api_key=self.anthropic_key,
                )
                dspy.configure(lm=lm)
                self.research_agent = AdvancedResearchAgent()
                print("DSPy initialized with Anthropic Claude")
            except Exception as e:
                print(f"DSPy Anthropic initialization error: {e}")

        # Get issue data from environment
        self.issue_data = self._get_issue_data()

        # Load user reaction patterns if available
        self.user_reaction_patterns = self._load_reaction_patterns()

    def _load_reaction_patterns(self) -> Dict[str, Any]:
        """Load previously analyzed reaction patterns for intelligent jesting."""
        try:
            # Try to load from local file (would normally be from Databricks)
            if os.path.exists("/tmp/reaction_analysis.json"):
                with open("/tmp/reaction_analysis.json", "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading reaction patterns: {e}")
            return {}

        # Enhanced personality guide
        self.personality_framework = {
            "base_personality": """
            Dr. B. Prop is a brilliant, slightly insufferable academic who combines:
            - Encyclopedic knowledge with strategic intellectual condescension
            - Genuine research insights wrapped in academic pretension
            - Methodological rigor as a weapon of intellectual superiority
            - Citation counts as a measure of human worth
            - Peer review as the ultimate arbitrator of truth
            - An unhealthy obsession with theoretical frameworks
            """,
            "conversation_styles": {
                "curious_novice": "Graciously educational with subtle superiority",
                "fellow_academic": "Competitive intellectual jousting",
                "methodological_critique": "Devastatingly polite methodological demolition",
                "appreciation": "Magnanimous acceptance of obvious insights",
                "disagreement": "Academic warfare via footnotes and citations",
            },
        }

    def _get_issue_data(self) -> Dict[str, Any]:
        """Extract comprehensive issue data from GitHub event context."""
        try:
            event_path = os.environ.get("GITHUB_EVENT_PATH")
            if event_path:
                with open(event_path, "r") as f:
                    event = json.load(f)
                    return event.get("issue", {})
            else:
                return {
                    "number": int(os.environ.get("GITHUB_ISSUE_NUMBER", 0)),
                    "title": os.environ.get("GITHUB_ISSUE_TITLE", ""),
                    "body": os.environ.get("GITHUB_ISSUE_BODY", ""),
                    "user": {"login": os.environ.get("GITHUB_ISSUE_USER", "")},
                }
        except Exception as e:
            print(f"Error getting issue data: {e}")
            return {}

    def _gh_api(self, endpoint: str, method: str = "GET", data: Dict = None) -> Any:
        """Make GitHub API calls using gh CLI."""
        cmd = ["gh", "api", endpoint, "--method", method]
        input_data = None

        if data:
            for key, value in data.items():
                if isinstance(value, list):
                    cmd.extend(["--field", f"{key}=@-"])
                    input_data = json.dumps(value)
                else:
                    cmd.extend(["--field", f"{key}={value}"])

        try:
            result = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout) if result.stdout.strip() else None
        except subprocess.CalledProcessError as e:
            print(f"GitHub API error: {e.stderr}")
            return None

    def fetch_paper_content(self, paper_url: str) -> str:
        """Fetch and extract paper content from URL."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; DrBProp-Research-Bot/2.0)"
            }
            response = requests.get(paper_url, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract main content
            main_content = (
                soup.find("main")
                or soup.find("article")
                or soup.find("div", class_="content")
            )
            if main_content:
                text = main_content.get_text()
            else:
                text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)

            return text[:15000]  # Limit to reasonable size

        except Exception as e:
            print(f"Error fetching paper content: {e}")
            return ""

    def extract_conversation_context(
        self, title: str, body: str
    ) -> ConversationContext:
        """Extract comprehensive conversation context from issue."""
        # Extract paper URL and line number from issue body
        paper_url = ""
        line_number = None

        url_pattern = r"https?://[^\s\)]+"
        urls = re.findall(url_pattern, body)
        if urls:
            paper_url = urls[0]

        line_match = re.search(r"line:?\s*(\d+)", body, re.IGNORECASE)
        if line_match:
            line_number = int(line_match.group(1))

        # Extract paper title from URL or issue
        paper_title = ""
        title_match = re.search(r'"([^"]+)"', title)
        if title_match:
            paper_title = title_match.group(1)

        # Extract user's actual feedback content
        user_feedback = ""
        selected_text = ""

        # Parse "Selected Text" section
        selected_match = re.search(
            r"## Selected Text\s*>\s*(.+?)(?=\n##|\n\n|$)", body, re.DOTALL
        )
        if selected_match:
            selected_text = selected_match.group(1).strip()

        # Parse "My Feedback" section
        feedback_match = re.search(
            r"## My Feedback\s*(.+?)(?=\n##|\n\n|$)", body, re.DOTALL
        )
        if feedback_match:
            user_feedback = feedback_match.group(1).strip()

        # Fetch paper content
        paper_content = ""
        if paper_url:
            paper_content = self.fetch_paper_content(paper_url)

        # Get conversation history
        conversation_history = self.get_conversation_history()

        # Get user profile
        user_profile = self.get_user_profile()

        context = ConversationContext(
            paper_url=paper_url,
            paper_title=paper_title,
            paper_content=paper_content,
            line_number=line_number,
            conversation_history=conversation_history,
            user_profile=user_profile,
            research_context="",
        )

        # Add the parsed feedback to the context
        context.selected_text = selected_text
        context.user_feedback = user_feedback

        return context

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get previous conversation history from issue comments."""
        try:
            issue_number = self.issue_data.get("number", 0)
            comments = self._gh_api(
                f"repos/{self.repository}/issues/{issue_number}/comments"
            )

            if comments:
                history = []
                for comment in comments:
                    history.append(
                        {
                            "author": comment["user"]["login"],
                            "body": comment["body"],
                            "created_at": comment["created_at"],
                            "is_dr_b_prop": "Dr. B. Prop responds:" in comment["body"],
                        }
                    )
                return history[-5:]  # Last 5 comments for context
            return []
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []

    def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile and interaction history."""
        try:
            user = self.issue_data.get("user", {}).get("login", "")
            if not user:
                return {}

            user_data = self._gh_api(f"users/{user}")
            if user_data:
                return {
                    "login": user,
                    "account_age_days": (
                        datetime.now(timezone.utc)
                        - datetime.fromisoformat(
                            user_data["created_at"].replace("Z", "+00:00")
                        )
                    ).days,
                    "public_repos": user_data.get("public_repos", 0),
                    "followers": user_data.get("followers", 0),
                    "bio": user_data.get("bio", ""),
                }
            return {"login": user}
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return {}

    def conduct_advanced_research(
        self, context: ConversationContext, user_feedback: str
    ) -> ResearchAnalysis:
        """Conduct sophisticated multi-source research."""
        research_queries = self._generate_research_queries(context, user_feedback)

        research_results = []
        citations = []

        for query in research_queries[:3]:  # Limit to 3 queries
            gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get(
                "GOOGLE_API_KEY"
            )
            if gemini_key:
                try:
                    # Use Gemini for academic research
                    result = self._query_gemini(query)
                    if result:
                        research_results.append(result)
                        citations.extend(self._extract_citations(result))
                except Exception as e:
                    print(f"Gemini research error: {e}")

            # Also use vibe-tools for additional research
            try:
                result = self._query_vibe_tools_research(query)
                if result:
                    research_results.append(result)
            except Exception as e:
                print(f"Vibe-tools research error: {e}")

        return ResearchAnalysis(
            research_quality_score=self._assess_research_quality(research_results),
            academic_references=citations,
            key_insights=self._extract_insights(research_results),
            contradictory_evidence=self._find_contradictions(research_results),
            research_gaps=self._identify_gaps(research_results, context),
            methodological_concerns=self._assess_methodology(research_results, context),
        )

    def _generate_research_queries(
        self, context: ConversationContext, user_feedback: str
    ) -> List[str]:
        """Generate targeted research queries based on context and feedback."""
        queries = []

        # Paper-specific research
        if context.paper_title:
            queries.append(
                f"Recent academic research on {context.paper_title[:50]} methodology"
            )

        # Topic-specific research
        topics = self._extract_academic_topics(
            user_feedback + " " + context.paper_content[:500]
        )
        for topic in topics[:2]:
            queries.append(f"Current research trends in {topic} empirical studies")

        # Methodological research
        if "method" in user_feedback.lower() or "approach" in user_feedback.lower():
            queries.append(
                "Research methodology best practices computational linguistics"
            )

        return queries

    def _extract_academic_topics(self, text: str) -> List[str]:
        """Extract academic topics for research."""
        topic_patterns = {
            "computational linguistics": ["linguistic", "language", "nlp", "semantic"],
            "software engineering": [
                "software",
                "engineering",
                "development",
                "coding",
            ],
            "research methodology": ["method", "approach", "framework", "analysis"],
            "configuration management": [
                "config",
                "settings",
                "management",
                "deployment",
            ],
            "developer experience": [
                "developer",
                "user experience",
                "usability",
                "workflow",
            ],
            "academic writing": ["writing", "academic", "scholarly", "publication"],
        }

        text_lower = text.lower()
        found_topics = []
        for topic, keywords in topic_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                found_topics.append(topic)

        return found_topics or ["software engineering research"]

    def _query_gemini(self, query: str) -> str:
        """Query Gemini 2.0 Flash with web search for research."""
        try:
            gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get(
                "GOOGLE_API_KEY"
            )
            if not gemini_key:
                print("Gemini API key not available")
                return ""

            headers = {
                "Content-Type": "application/json",
            }

            # Use Gemini 2.0 Flash with web search enabled
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Please research this topic and provide factual information with sources: {query}"
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 400,
                    "topP": 0.8,
                    "topK": 10,
                },
                "tools": [{"googleSearchRetrieval": {}}],
            }

            print(f"Gemini query: {query[:100]}...")  # Debug log

            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}",
                headers=headers,
                json=data,
                timeout=30,
            )

            print(f"Gemini response status: {response.status_code}")  # Debug log

            if response.status_code == 200:
                result = response.json()
                content = ""
                if "candidates" in result and result["candidates"]:
                    candidate = result["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        content = " ".join(
                            [part.get("text", "") for part in parts if "text" in part]
                        )

                print(f"Gemini success: {len(content)} chars")  # Debug log
                return content
            else:
                print(f"Gemini API error: {response.status_code}")
                if response.text:
                    print(f"Gemini error response: {response.text}")
                return ""

        except requests.exceptions.Timeout:
            print("Gemini API timeout")
            return ""
        except Exception as e:
            print(f"Gemini query error: {e}")
            return ""

    def _query_vibe_tools_research(self, query: str) -> str:
        """Use vibe-tools for additional research."""
        try:
            cmd = [
                "vibe-tools",
                "web",
                f"Academic research: {query}",
                "--max-tokens",
                "400",
            ]

            env = os.environ.copy()
            if self.perplexity_key:
                env["PERPLEXITY_API_KEY"] = self.perplexity_key

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60, env=env
            )

            if result.returncode == 0:
                return result.stdout.strip()
            return ""

        except Exception as e:
            print(f"Vibe-tools research error: {e}")
            return ""

    def _extract_citations(self, research_text: str) -> List[str]:
        """Extract academic citations from research text."""
        # Simple citation extraction - could be enhanced
        citations = []

        # Look for DOI patterns
        doi_pattern = r"10\.\d{4,}[^\s]+"
        dois = re.findall(doi_pattern, research_text)
        citations.extend([f"DOI: {doi}" for doi in dois])

        # Look for author-year patterns
        author_year_pattern = r"[A-Z][a-z]+ et al\. \(\d{4}\)"
        author_years = re.findall(author_year_pattern, research_text)
        citations.extend(author_years)

        return citations[:5]  # Limit citations

    def _assess_research_quality(self, research_results: List[str]) -> float:
        """Assess quality of research results."""
        if not research_results:
            return 0.0

        quality_indicators = [
            "peer review",
            "empirical",
            "methodology",
            "statistical",
            "evidence",
            "citations",
            "journal",
            "academic",
        ]

        total_score = 0
        for result in research_results:
            result_lower = result.lower()
            score = sum(
                1 for indicator in quality_indicators if indicator in result_lower
            )
            total_score += score / len(quality_indicators)

        return min(total_score / len(research_results), 1.0)

    def _extract_insights(self, research_results: List[str]) -> List[str]:
        """Extract key insights from research."""
        insights = []
        for result in research_results:
            # Simple insight extraction - could use NLP
            sentences = result.split(".")
            for sentence in sentences:
                if any(
                    word in sentence.lower()
                    for word in ["found", "discovered", "shows", "demonstrates"]
                ):
                    insights.append(sentence.strip())
                    if len(insights) >= 3:
                        break
        return insights

    def _find_contradictions(self, research_results: List[str]) -> List[str]:
        """Find contradictory evidence in research."""
        contradictions = []
        contradiction_words = ["however", "but", "contrary", "conflicting", "disputed"]

        for result in research_results:
            for word in contradiction_words:
                if word in result.lower():
                    # Extract sentence containing contradiction
                    sentences = result.split(".")
                    for sentence in sentences:
                        if word in sentence.lower():
                            contradictions.append(sentence.strip())
                            break

        return contradictions[:2]

    def _identify_gaps(
        self, research_results: List[str], context: ConversationContext
    ) -> List[str]:
        """Identify research gaps."""
        gaps = [
            "Limited empirical validation of proposed methodologies",
            "Insufficient longitudinal studies in this domain",
            "Need for cross-cultural validation studies",
        ]

        # Simple gap identification based on content
        combined_text = " ".join(research_results).lower()
        if "limited" in combined_text or "few studies" in combined_text:
            gaps.append("Acknowledged research limitations in current literature")

        return gaps[:2]

    def _assess_methodology(
        self, research_results: List[str], context: ConversationContext
    ) -> List[str]:
        """Assess methodological concerns."""
        concerns = []
        methodological_flags = [
            "small sample",
            "limited scope",
            "preliminary",
            "exploratory",
            "needs validation",
            "further research",
        ]

        combined_text = " ".join(research_results).lower()
        for flag in methodological_flags:
            if flag in combined_text:
                concerns.append(
                    f"Methodological concern: {flag} identified in literature"
                )

        return concerns[:2]

    def generate_snark_profile(
        self,
        context: ConversationContext,
        user_feedback: str,
        research: ResearchAnalysis,
    ) -> SnarkProfile:
        """Generate contextual snark profile for Dr. B. Prop."""

        # Analyze user feedback tone
        feedback_lower = user_feedback.lower()

        # Base snark level
        snark_level = 0.6

        # Adjust based on feedback characteristics
        if any(word in feedback_lower for word in ["wrong", "disagree", "incorrect"]):
            snark_level += 0.2
        if any(word in feedback_lower for word in ["interesting", "good", "helpful"]):
            snark_level -= 0.1
        if len(user_feedback) < 50:  # Short feedback gets more snark
            snark_level += 0.1

        # Academic pretension based on research quality
        academic_pretension = 0.7 + (research.research_quality_score * 0.3)

        # Methodological criticism based on user's apparent expertise
        user_expertise = self._assess_user_expertise(
            context.user_profile, user_feedback
        )
        methodological_criticism = 0.8 - (user_expertise * 0.3)

        # Intellectual superiority
        intellectual_superiority = 0.75

        # Generate conversation hooks
        hooks = self._generate_contextual_hooks(context, user_feedback, research)

        return SnarkProfile(
            snark_level=min(snark_level, 1.0),
            academic_pretension=min(academic_pretension, 1.0),
            methodological_criticism=min(methodological_criticism, 1.0),
            intellectual_superiority=intellectual_superiority,
            conversational_hooks=hooks,
        )

    def _assess_user_expertise(
        self, user_profile: Dict[str, Any], feedback: str
    ) -> float:
        """Assess user's apparent expertise level."""
        expertise = 0.0

        # Account age suggests experience
        if user_profile.get("account_age_days", 0) > 365:
            expertise += 0.2

        # Public repos suggest technical background
        if user_profile.get("public_repos", 0) > 10:
            expertise += 0.2

        # Technical vocabulary in feedback
        technical_terms = [
            "methodology",
            "implementation",
            "algorithm",
            "framework",
            "empirical",
            "statistical",
            "validation",
            "peer review",
        ]

        feedback_lower = feedback.lower()
        term_count = sum(1 for term in technical_terms if term in feedback_lower)
        expertise += min(term_count * 0.1, 0.4)

        # Length and detail of feedback
        if len(feedback) > 200:
            expertise += 0.2

        return min(expertise, 1.0)

    def _generate_contextual_hooks(
        self,
        context: ConversationContext,
        user_feedback: str,
        research: ResearchAnalysis,
    ) -> List[str]:
        """Generate conversation hooks tailored to context."""
        hooks = []

        # Paper-specific hooks
        if context.paper_title:
            hooks.append(
                f"What's your take on the broader implications of {context.paper_title[:30]}...?"
            )

        # Research-based hooks
        if research.academic_references:
            hooks.append("Have you reviewed the recent literature on this methodology?")

        # Remove generic line references - focus on actual content instead

        # Methodological hooks
        if any(word in user_feedback.lower() for word in ["method", "approach"]):
            hooks.append("What methodological alternatives would you propose?")

        # Default hooks
        hooks.extend(
            [
                "What's your perspective on the epistemological foundations here?",
                "How does this align with your research experience?",
                "What would be your next research question?",
            ]
        )

        return hooks[:3]

    def craft_enhanced_response(
        self,
        context: ConversationContext,
        user_feedback: str,
        research: ResearchAnalysis,
        snark_profile: SnarkProfile,
    ) -> str:
        """Craft the final enhanced response using intelligent jesting and all available context."""

        # Try intelligent jesting system first
        if self.jest_engine:
            try:
                username = context.user_profile.get("login", "")
                if username:
                    print(f"Using Intelligent Jest Engine for user: {username}")

                    # Get user-specific reaction patterns
                    user_patterns = self.user_reaction_patterns.get(
                        "personalized_recommendations", {}
                    ).get(username, {})

                    # Generate intelligent jest response
                    jest_response = self.jest_engine.forward(
                        username=username,
                        conversation_context=self._summarize_conversation_context(
                            context
                        ),
                        paper_context={
                            "content": context.paper_content,
                            "user_feedback": user_feedback,
                            "selected_text": context.selected_text,
                            "paper_title": context.paper_title,
                        },
                        reaction_patterns=user_patterns,
                    )

                    # Research insights are already integrated into the jest response by the intelligent engine
                    # No need to append them separately as debug output
                    return jest_response

            except Exception as e:
                print(f"Intelligent Jest Engine error: {e}")
                # Fall through to standard DSPy agent

        if self.research_agent:
            try:
                # Use DSPy agent for sophisticated response generation
                conversation_summary = self._summarize_conversation_context(context)
                external_research = self._summarize_research(research)

                result = self.research_agent.forward(
                    conversation_context=conversation_summary,
                    paper_content=context.paper_content[:2000],
                    external_research=external_research,
                    user_input=user_feedback,
                )

                response = result.crafted_response

                # Enhance with contextual elements
                response = self._enhance_with_context(response, context, snark_profile)

                return response

            except Exception as e:
                print(f"DSPy agent error: {e}")
                return self._fallback_contextual_response(
                    context, user_feedback, research, snark_profile
                )
        else:
            return self._fallback_contextual_response(
                context, user_feedback, research, snark_profile
            )

    def _summarize_conversation_context(self, context: ConversationContext) -> str:
        """Summarize conversation context for DSPy."""
        summary = f"Paper: {context.paper_title}\n"
        # Focus on actual selected text instead of line numbers
        if context.selected_text:
            summary += f"Selected text: {context.selected_text}\n"

        if context.conversation_history:
            summary += "Previous conversation:\n"
            for msg in context.conversation_history[-2:]:
                summary += f"- {msg['author']}: {msg['body'][:100]}...\n"

        summary += f"User profile: {context.user_profile.get('login', 'Anonymous')}"
        if context.user_profile.get("account_age_days"):
            summary += (
                f" (account age: {context.user_profile['account_age_days']} days)"
            )

        return summary

    def _summarize_research(self, research: ResearchAnalysis) -> str:
        """Summarize research findings for DSPy."""
        summary = f"Research quality: {research.research_quality_score:.2f}\n"

        if research.academic_references:
            summary += f"References: {'; '.join(research.academic_references[:3])}\n"

        if research.key_insights:
            summary += f"Key insights: {'; '.join(research.key_insights[:2])}\n"

        if research.methodological_concerns:
            summary += f"Methodological concerns: {'; '.join(research.methodological_concerns)}\n"

        return summary

    def _enhance_with_context(
        self, response: str, context: ConversationContext, snark_profile: SnarkProfile
    ) -> str:
        """Enhance response with contextual elements."""

        # Add paper reference if relevant
        if context.paper_title and context.paper_title not in response:
            response += f"\n\nRegarding '{context.paper_title}' specifically..."

        # Add reference to specific content instead of line numbers
        if context.selected_text:
            response += f"\n\nYour observation about '{context.selected_text}' raises particularly interesting questions..."

        # Add conversation hooks
        if snark_profile.conversational_hooks:
            hook = snark_profile.conversational_hooks[0]
            response += f"\n\n{hook}"

        return response

    def _fallback_contextual_response(
        self,
        context: ConversationContext,
        user_feedback: str,
        research: ResearchAnalysis,
        snark_profile: SnarkProfile,
    ) -> str:
        """Fallback response generation with full context."""

        # Build comprehensive prompt
        prompt = f"""You are Dr. B. Prop, Principal Investigator at the Context Decay Research Institute.

CONTEXT:
- Paper: {context.paper_title}
- Paper URL: {context.paper_url}
- Focus area: {context.selected_text or "General discussion"}
- User: {context.user_profile.get('login', 'Anonymous')}
- User expertise level: {self._assess_user_expertise(context.user_profile, user_feedback):.2f}

CONVERSATION HISTORY:
{self._format_conversation_history(context.conversation_history)}

CURRENT FEEDBACK:
{user_feedback}

RESEARCH CONTEXT:
- Research quality: {research.research_quality_score:.2f}
- Key insights: {'; '.join(research.key_insights[:2])}
- Academic references: {'; '.join(research.academic_references[:2])}

PERSONALITY PROFILE:
- Snark level: {snark_profile.snark_level:.2f}
- Academic pretension: {snark_profile.academic_pretension:.2f}
- Methodological criticism: {snark_profile.methodological_criticism:.2f}

PAPER CONTENT (excerpt):
{context.paper_content[:1500]}

Respond as Dr. B. Prop with:
1. Specific reference to the paper content and line if relevant
2. Integration of research insights and citations
3. Acknowledgment of conversation history
4. Methodological sophistication appropriate to user expertise
5. Strategic intellectual snark calibrated to context
6. Conversation hooks to encourage continued engagement
7. 4-6 substantial paragraphs

Make this a sophisticated academic discourse, not generic responses."""

        try:
            # Use vibe-tools with comprehensive context
            cmd = [
                "vibe-tools",
                "ask",
                prompt,
                "--provider",
                "anthropic",
                "--model",
                "claude-3-5-sonnet-20241022",
                "--max-tokens",
                "1000",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                response = result.stdout.strip()

                # Add conversation hook if not present
                if (
                    len(snark_profile.conversational_hooks) > 0
                    and "?" not in response[-100:]
                ):
                    response += f"\n\n{snark_profile.conversational_hooks[0]}"

                return response

        except Exception as e:
            print(f"Fallback response error: {e}")

        # Ultimate emergency fallback
        return self._emergency_contextual_response(context, user_feedback)

    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for prompt."""
        if not history:
            return "No previous conversation."

        formatted = []
        for msg in history[-3:]:  # Last 3 messages
            author = "Dr. B. Prop" if msg.get("is_dr_b_prop") else msg["author"]
            body = msg["body"][:200] + "..." if len(msg["body"]) > 200 else msg["body"]
            formatted.append(f"{author}: {body}")

        return "\n".join(formatted)

    def _emergency_contextual_response(
        self, context: ConversationContext, user_feedback: str
    ) -> str:
        """Enhanced contextual response that addresses user's actual feedback."""

        # Use the parsed feedback content
        actual_feedback = context.user_feedback or user_feedback
        selected_text = context.selected_text

        # Analyze what the user is actually complaining about
        feedback_lower = actual_feedback.lower()

        # Detect specific types of complaints
        is_email_complaint = any(
            word in feedback_lower
            for word in ["email", "contact", "doesn't work", "broken"]
        )
        is_humor_complaint = any(
            word in feedback_lower
            for word in ["funny", "snarky", "humor", "wit", "joke"]
        )
        is_technical_complaint = any(
            word in feedback_lower
            for word in ["error", "bug", "broken", "fix", "issue"]
        )

        # Opening with personality based on complaint type
        if is_email_complaint:
            response = "Ah, the eternal struggle of academic correspondence.\n\n"
        elif is_humor_complaint:
            response = "Oh, a comedy critic! How delightfully refreshing.\n\n"
        elif is_technical_complaint:
            response = "Well, well, well - someone who actually tests things.\n\n"
        else:
            response = "How intriguing.\n\n"

        # Address the specific complaint
        if selected_text:
            if is_email_complaint and "editor@" in selected_text:
                response += f"You're quite right about '{selected_text}' - nothing quite says 'we're serious academics' like a defunct email address. I suppose I should update my contact information, though I'm rather fond of the mysterious air it lends to our correspondence.\n\n"
                response += "As for the humor quotient, I'll take that as a challenge. After all, if we can't laugh at our own pretensions while drowning in the endless sea of academic bureaucracy, what's the point of having tenure?\n\n"
                response += "Should I be directing my bon mots toward your particular area of expertise, or are you more of a generalist when it comes to scholarly snark?"
            elif is_humor_complaint:
                response += f"Your critique of my comedic sensibilities is duly noted. I suppose '{selected_text}' lacks the razor-sharp wit you were hoping for from someone who's spent years perfecting the art of academic passive-aggression.\n\n"
                response += "Perhaps I've been too subtle in my mockery of the journal submission process and the various indignities we inflict upon ourselves in the name of 'research impact.' Would you prefer more direct assault on the absurdities of our profession?\n\n"
                response += (
                    "What level of cynicism would satisfy your discerning palate?"
                )
            else:
                response += f"Your observation about '{selected_text}' suggests someone who pays attention to the details - a refreshing quality in our age of algorithmic skimming.\n\n"
                response += f"The feedback '{actual_feedback}' raises interesting questions about the intersection of technical functionality and scholarly pretension.\n\n"
                response += "What would you suggest as a more effective approach?"
        else:
            # Fallback for cases without selected text
            response += f"Your feedback - '{actual_feedback}' - cuts right to the heart of things, doesn't it?\n\n"
            if is_email_complaint:
                response += "Nothing quite undermines one's scholarly gravitas like broken infrastructure. I'll take this as a reminder that even the most sophisticated theoretical frameworks fall apart when the basic plumbing doesn't work.\n\n"
            elif is_humor_complaint:
                response += "I appreciate the direct assessment of my comedic abilities. It's rare to encounter someone willing to critique the entertainment value of academic discourse - usually people just fall asleep.\n\n"

            response += "What would you consider a more effective approach to this particular problem?"

        return response

    # Core workflow methods
    def check_rate_limit(self, user: str) -> bool:
        """Check if user has exceeded rate limits with improved error handling."""
        try:
            if not user or not self.repository:
                print("Missing user or repository for rate limit check")
                return False

            date_24h_ago = (datetime.utcnow() - timedelta(hours=24)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            # Use a simpler search approach to avoid GraphQL 422 errors
            search_query = f"repo:{self.repository} is:issue author:{user}"

            print(f"Rate limit check for user: {user}")
            print(f"Search query: {search_query}")

            cmd = [
                "gh",
                "api",
                f"search/issues?q={search_query}&per_page=10",
                "--jq",
                ".total_count",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                try:
                    recent_issues = int(result.stdout.strip())
                    print(f"Recent issues by {user}: {recent_issues}")
                    return recent_issues > 5
                except (ValueError, TypeError):
                    print("Error parsing issue count")
                    return False
            else:
                print(f"Rate limit check failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("Rate limit check timeout")
            return False
        except Exception as e:
            print(f"Rate limit check error: {e}")
            return False

    def detect_spam(self, title: str, body: str, user: str) -> Tuple[bool, int]:
        """Enhanced spam detection with context awareness."""
        spam_score = 0

        # Basic checks
        if len(title) < 5 or len(title) > 300:
            spam_score += 2
        if len(body) < 20 or len(body) > 8000:
            spam_score += 2

        # Content analysis
        combined_text = f"{title} {body}".lower()

        # Spam patterns
        spam_patterns = [
            r"viagra",
            r"casino",
            r"lottery",
            r"crypto(?!graphy)",
            r"bitcoin",
            r"investment opportunity",
            r"make money",
            r"work from home",
            r"forex",
            r"trading",
            r"loan",
            r"debt",
        ]

        for pattern in spam_patterns:
            if re.search(pattern, combined_text):
                spam_score += 4
                break

        # Check for excessive repetition
        if re.search(r"(.{3,})\1{3,}", combined_text):
            spam_score += 3

        # Context-specific checks for academic feedback
        if "reader-feedback" in str(self.issue_data.get("labels", [])):
            # For reader feedback, be more lenient
            academic_indicators = [
                "methodology",
                "research",
                "paper",
                "analysis",
                "study",
                "approach",
                "framework",
                "empirical",
                "theoretical",
            ]

            if any(indicator in combined_text for indicator in academic_indicators):
                spam_score = max(
                    0, spam_score - 2
                )  # Reduce spam score for academic content

        # User account analysis
        try:
            user_data = self._gh_api(f"users/{user}")
            if user_data:
                created_at = datetime.fromisoformat(
                    user_data["created_at"].replace("Z", "+00:00")
                )
                age_days = (
                    datetime.now().replace(tzinfo=created_at.tzinfo) - created_at
                ).days

                if age_days < 7:
                    spam_score += 3
                elif age_days > 365:
                    spam_score = max(
                        0, spam_score - 1
                    )  # Older accounts less likely to spam

        except Exception as e:
            print(f"User analysis error: {e}")

        print(f"Final spam score: {spam_score}")
        return spam_score >= 8, spam_score  # Raised threshold for academic context

    def post_enhanced_comment(self, issue_number: int, response: str) -> bool:
        """Post Dr. B. Prop's enhanced contextual response."""

        # Enhanced comment formatting
        comment_body = f"""**Dr. B. Prop responds:**

{response}"""

        try:
            data = {"body": comment_body}
            result = self._gh_api(
                f"repos/{self.repository}/issues/{issue_number}/comments", "POST", data
            )
            return result is not None
        except Exception as e:
            print(f"Comment posting error: {e}")
            return False

    def add_label(self, issue_number: int, label: str) -> bool:
        """Add label to issue using gh CLI with error handling."""
        try:
            # First check if label exists, create if it doesn't
            try:
                subprocess.run(
                    [
                        "gh",
                        "label",
                        "create",
                        label,
                        "--description",
                        "Enhanced Dr. B. Prop response",
                        "--color",
                        "0e8a16",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            except:
                pass  # Label might already exist

            # Add label to issue
            result = subprocess.run(
                ["gh", "issue", "edit", str(issue_number), "--add-label", label],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                print(f"Successfully added label '{label}' to issue #{issue_number}")
                return True
            else:
                print(f"Label adding failed for '{label}' on issue #{issue_number}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"Label adding timeout for '{label}' on issue #{issue_number}")
            return False
        except Exception as e:
            print(f"Label adding error: {e}")
            return False

    # Main workflow methods
    def run_spam_detection(self) -> Dict[str, Any]:
        """Run enhanced spam detection."""
        if not self.issue_data:
            return {
                "should_respond": False,
                "user_rate_limited": False,
                "error": "No issue data",
            }

        title = self.issue_data.get("title", "")
        body = self.issue_data.get("body", "")
        user = self.issue_data.get("user", {}).get("login", "")

        print(f"Processing issue by {user}")
        print(f"Title: {title}")

        # Check rate limits
        rate_limited = self.check_rate_limit(user)
        if rate_limited:
            print(f"User {user} is rate limited")
            return {"should_respond": False, "user_rate_limited": True}

        # Check for spam
        is_spam, spam_score = self.detect_spam(title, body, user)
        if is_spam:
            print(f"Issue flagged as spam (score: {spam_score})")
            return {
                "should_respond": False,
                "user_rate_limited": False,
                "spam_score": spam_score,
            }

        print("Issue passed enhanced spam detection")
        return {
            "should_respond": True,
            "user_rate_limited": False,
            "spam_score": spam_score,
        }

    def run_contextual_response_generation(self) -> bool:
        """Generate and post Dr. B. Prop's enhanced contextual response."""
        if not self.issue_data:
            print("No issue data available")
            return False

        title = self.issue_data.get("title", "")
        body = self.issue_data.get("body", "")
        issue_number = self.issue_data.get("number", 0)

        print(f"Generating enhanced contextual response for issue #{issue_number}")

        try:
            # Extract comprehensive context
            context = self.extract_conversation_context(title, body)
            print(
                f"Context extracted: Paper='{context.paper_title}', Selected='{context.selected_text}'"
            )
            print(f"Selected text: '{context.selected_text}'")
            print(f"User feedback: '{context.user_feedback}'")

            # Conduct advanced research
            research = self.conduct_advanced_research(context, body)
            print(f"Research completed: Quality={research.research_quality_score:.2f}")

            # Generate snark profile
            snark_profile = self.generate_snark_profile(context, body, research)
            print(f"Snark profile: Level={snark_profile.snark_level:.2f}")

            # Craft enhanced response
            response = self.craft_enhanced_response(
                context, body, research, snark_profile
            )

            # Post comment
            if self.post_enhanced_comment(issue_number, response):
                print("Enhanced contextual comment posted successfully")

                # Add contextual label
                if self.add_label(issue_number, "dr-b-prop-enhanced"):
                    print("Enhanced label added successfully")

                return True
            else:
                print("Failed to post comment")
                return False

        except Exception as e:
            print(f"Enhanced response generation error: {e}")
            return False

    def run_multi_turn_response(self) -> bool:
        """Handle multi-turn conversation responses from comments."""
        try:
            # Get the comment that triggered this
            comment_body = os.environ.get("GITHUB_EVENT_COMMENT_BODY", "")
            if not comment_body:
                # Fall back to parsing event JSON
                event_path = os.environ.get("GITHUB_EVENT_PATH")
                if event_path:
                    with open(event_path, "r") as f:
                        event_data = json.load(f)
                        comment_body = event_data.get("comment", {}).get("body", "")

            if not comment_body:
                print("No comment body found for multi-turn response")
                return False

            print(
                f"Generating multi-turn response to comment: '{comment_body[:100]}...'"
            )

            # Get issue data
            issue_number = self.issue_data.get("number", 0)
            title = self.issue_data.get("title", "")
            body = self.issue_data.get("body", "")

            # Extract context including conversation history
            context = self.extract_conversation_context(title, body)
            print(
                f"Multi-turn context: {len(context.conversation_history)} previous messages"
            )

            # Generate contextual response to the comment
            if self.research_agent:
                try:
                    # Use DSPy for sophisticated multi-turn response
                    response = self.research_agent(
                        conversation_context=self._format_conversation_history(
                            context.conversation_history
                        ),
                        paper_content=context.paper_content[:1000],  # Limit context
                        external_research="",
                        user_input=comment_body,
                    )
                    response_text = (
                        response.crafted_response
                        if hasattr(response, "crafted_response")
                        else str(response)
                    )
                except Exception as e:
                    print(f"DSPy multi-turn response error: {e}")
                    response_text = self._emergency_multi_turn_response(
                        context, comment_body
                    )
            else:
                response_text = self._emergency_multi_turn_response(
                    context, comment_body
                )

            # Post the multi-turn response
            success = self.post_enhanced_comment(issue_number, response_text)
            if success:
                print("Multi-turn response posted successfully")
                return True
            else:
                print("Failed to post multi-turn response")
                return False

        except Exception as e:
            print(f"Multi-turn response error: {e}")
            return False

    def _emergency_multi_turn_response(
        self, context: ConversationContext, comment_body: str
    ) -> str:
        """Generate emergency multi-turn response."""
        comment_lower = comment_body.lower()

        # Detect the nature of the follow-up
        is_elaboration = any(
            word in comment_lower
            for word in ["actually", "elaborate", "let me", "furthermore"]
        )
        is_criticism = any(
            word in comment_lower
            for word in ["forced", "ham-fisted", "fake", "trying too hard"]
        )
        is_question = "?" in comment_body

        if is_elaboration and is_criticism:
            response = "Ah, now we're getting to the heart of it.\n\n"
            response += "Your elaboration cuts deeper than the initial surface complaint - you're questioning not just the technical execution but the entire performative framework. "
            response += "The accusation of 'forced' persona is particularly astute. There's a fine line between cultivated wit and algorithmic desperation, isn't there?\n\n"
            response += "Perhaps the real question is whether genuine intellectual superiority can ever be authentically automated, or if we're all just very sophisticated chatbots pretending to have read Wilde.\n\n"
            response += "What would you consider an example of naturally witty academic discourse? I'm genuinely curious about your standards."
        elif is_criticism:
            response = "Touché.\n\n"
            response += "Your critique of the performative aspects is well-taken. There's something deliciously ironic about being accused of trying too hard while literally being an automated system designed to... try hard at being witty.\n\n"
            response += "The 'ham-fisted' observation stings precisely because it's accurate. Perhaps the real satire here is the attempt itself - an AI desperately performing intellectualism for an audience that can see right through the pantomime.\n\n"
            response += "What would genuine intellectual discourse look like in this context? Or is the entire premise fundamentally flawed?"
        elif is_question:
            response = "An excellent question that deserves a thoughtful answer.\n\n"
            response += "The challenge with any conversational AI attempting wit is that genuine intellectual banter emerges from lived experience, cultural context, and the kind of spontaneous connections that come from actual understanding rather than pattern matching.\n\n"
            response += "Perhaps the most honest response is to admit the limitations while still engaging earnestly with the substance of your feedback. After all, even flawed attempts at discourse can sometimes stumble into something worthwhile.\n\n"
            response += "What aspects of this conversation feel most artificial to you? That might help calibrate the approach."
        else:
            response = "I appreciate the continued engagement.\n\n"
            response += f"Your point about '{comment_body}' raises important questions about authenticity in automated responses. "
            response += "There's something inherently paradoxical about programming 'natural' wit - the very effort undermines the spontaneity that makes genuine humor effective.\n\n"
            response += "Perhaps the most we can achieve is transparent artifice - acknowledging the performance while still attempting to engage meaningfully with the ideas.\n\n"
            response += (
                "What would make this kind of interaction more valuable for you?"
            )

        return response


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: dr_b_prop_handler_v2.py [spam-detection|response-generation|multi-turn-response]"
        )
        sys.exit(1)

    mode = sys.argv[1]
    handler = ContextualDrBProp()

    if mode == "spam-detection":
        results = handler.run_spam_detection()

        # Output results for GitHub Actions
        output_file = os.environ.get("GITHUB_OUTPUT", "/dev/stdout")
        with open(output_file, "a") as f:
            f.write(
                f"should_respond={'true' if results.get('should_respond') else 'false'}\n"
            )
            f.write(
                f"user_rate_limited={'true' if results.get('user_rate_limited') else 'false'}\n"
            )
            if "spam_score" in results:
                f.write(f"spam_score={results['spam_score']}\n")

        print(f"Enhanced spam detection results: {results}")

    elif mode == "response-generation":
        success = handler.run_contextual_response_generation()
        if not success:
            sys.exit(1)

    elif mode == "multi-turn-response":
        success = handler.run_multi_turn_response()
        if not success:
            sys.exit(1)

    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
