#!/usr/bin/env python3
"""
Dr. B. Prop - Intelligent Jest Engine with DSPy 3.0
Sophisticated academic jesting system powered by user intelligence and advanced DSPy optimization
"""

import os
import json
import dspy
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import requests
from datetime import datetime, timezone


@dataclass
class JestContext:
    """Context for generating sophisticated academic jests."""

    user_profile: Dict[str, Any]
    conversation_history: List[Dict[str, Any]]
    paper_context: Dict[str, Any]
    reaction_patterns: Dict[str, Any]
    jest_style_preferences: Dict[str, Any]


class UserIntelligenceRetriever(dspy.Signature):
    """Retrieve and synthesize user intelligence data for personalized jesting."""

    username: str = dspy.InputField(desc="GitHub username to analyze")
    conversation_context: str = dspy.InputField(desc="Current conversation context")

    user_intelligence_summary: str = dspy.OutputField(
        desc="Comprehensive summary of user's technical profile, coding patterns, and interaction style for academic jesting"
    )
    jest_opportunities: str = dspy.OutputField(
        desc="Specific areas ripe for sophisticated academic humor based on user's code and behavior patterns"
    )
    optimal_jest_style: str = dspy.OutputField(
        desc="Recommended jesting approach: sophisticated_peer, gentle_deflation, educational_jest, or collegial_banter"
    )


class AcademicJestCrafter(dspy.Signature):
    """Craft sophisticated academic jests tailored to user's profile and current context."""

    user_intelligence: str = dspy.InputField(
        desc="User's technical profile and patterns"
    )
    jest_opportunities: str = dspy.InputField(desc="Specific areas for academic humor")
    paper_content: str = dspy.InputField(desc="Current paper/topic being discussed")
    user_feedback: str = dspy.InputField(desc="User's specific feedback or question")
    jest_style: str = dspy.InputField(desc="Optimal jesting style for this user")
    conversation_history: str = dspy.InputField(desc="Previous conversation context")
    reaction_feedback: str = dspy.InputField(
        desc="Previous reaction patterns and effectiveness"
    )

    sophisticated_jest: str = dspy.OutputField(
        desc="Clever, witty academic response that playfully engages with user's technical background while addressing their feedback"
    )
    conversation_hooks: str = dspy.OutputField(
        desc="2-3 engaging questions or observations to encourage continued intelligent discourse"
    )
    jest_confidence: str = dspy.OutputField(
        desc="Confidence level (0.0-1.0) in the appropriateness and effectiveness of this jest for the specific user"
    )


class ReactionFeedbackAnalyzer(dspy.Signature):
    """Analyze emoji reaction patterns to improve future jesting effectiveness."""

    previous_responses: str = dspy.InputField(desc="Previous Dr. B. Prop responses")
    emoji_reactions: str = dspy.InputField(desc="Emoji reactions received from users")
    user_engagement_data: str = dspy.InputField(
        desc="User engagement patterns and feedback"
    )

    effectiveness_analysis: str = dspy.OutputField(
        desc="Analysis of which jesting approaches work best for different user types"
    )
    optimization_suggestions: str = dspy.OutputField(
        desc="Specific recommendations for improving jest effectiveness and user engagement"
    )
    personalization_insights: str = dspy.OutputField(
        desc="Insights about individual user preferences for future customization"
    )


class IntelligentJestEngine(dspy.Module):
    """Advanced DSPy 3.0 system for intelligent academic jesting with user personalization."""

    def __init__(self):
        super().__init__()

        # Initialize DSPy components with specific prompting strategies
        self.user_retriever = dspy.ChainOfThought(UserIntelligenceRetriever)
        self.jest_crafter = dspy.ChainOfThought(AcademicJestCrafter)
        self.reaction_analyzer = dspy.ChainOfThought(ReactionFeedbackAnalyzer)

        # Initialize external services
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.databricks_host = os.environ.get("DATABRICKS_HOST")
        self.databricks_token = os.environ.get("DATABRICKS_TOKEN")

    def retrieve_user_intelligence(
        self, username: str, conversation_context: str
    ) -> Dict[str, Any]:
        """Retrieve comprehensive user intelligence for jesting personalization."""
        try:
            # Use DSPy to analyze and synthesize user data
            intelligence = self.user_retriever(
                username=username, conversation_context=conversation_context
            )

            return {
                "summary": intelligence.user_intelligence_summary,
                "jest_opportunities": intelligence.jest_opportunities,
                "optimal_style": intelligence.optimal_jest_style,
            }
        except Exception as e:
            print(f"User intelligence retrieval error: {e}")
            return self._fallback_user_analysis(username)

    def _fallback_user_analysis(self, username: str) -> Dict[str, Any]:
        """Fallback user analysis when DSPy fails."""
        try:
            # Direct GitHub API analysis
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }

            user_data = requests.get(
                f"https://api.github.com/users/{username}", headers=headers
            ).json()
            repos_data = requests.get(
                f"https://api.github.com/users/{username}/repos?per_page=50",
                headers=headers,
            ).json()

            # Quick analysis
            languages = []
            total_stars = 0
            fork_count = 0

            for repo in repos_data[:20]:  # Analyze first 20 repos
                if repo.get("language"):
                    languages.append(repo["language"])
                total_stars += repo.get("stargazers_count", 0)
                if repo.get("fork"):
                    fork_count += 1

            # Determine jest opportunities
            top_languages = list(set(languages))[:3]
            jest_opps = []

            if "JavaScript" in top_languages:
                jest_opps.append(
                    "the eternal struggle with JavaScript's interesting relationship with truth and falsy values"
                )
            if "Python" in top_languages:
                jest_opps.append(
                    "the devotion to Pythonic principles, though sometimes 'there should be one obvious way to do it' becomes negotiable"
                )
            if fork_count > len(repos_data) * 0.7:
                jest_opps.append(
                    "the impressive collection of community contributions with thoughtful modifications"
                )

            # Determine style based on profile
            if user_data.get("public_repos", 0) > 50 and total_stars > 100:
                jest_style = "sophisticated_peer"
            elif user_data.get("followers", 0) > user_data.get("following", 1):
                jest_style = "respectful_acknowledgment"
            else:
                jest_style = "collegial_banter"

            return {
                "summary": f"Developer with {len(top_languages)} primary languages, {user_data.get('public_repos', 0)} repositories, active in {', '.join(top_languages[:2])} development",
                "jest_opportunities": "; ".join(jest_opps),
                "optimal_style": jest_style,
            }

        except Exception as e:
            print(f"Fallback analysis error: {e}")
            return {
                "summary": "Engaged community member with active development presence",
                "jest_opportunities": "general software development patterns and academic discourse",
                "optimal_style": "collegial_banter",
            }

    def generate_intelligent_jest(self, context: JestContext) -> Dict[str, Any]:
        """Generate sophisticated academic jest using full user intelligence."""
        try:
            # Prepare context for DSPy
            user_intel_summary = context.user_profile.get("summary", "")
            jest_opportunities = context.user_profile.get("jest_opportunities", "")
            jest_style = context.user_profile.get("optimal_style", "collegial_banter")

            paper_content = context.paper_context.get("content", "")[
                :1500
            ]  # Limit for efficiency
            user_feedback = context.paper_context.get("user_feedback", "")

            # Format conversation history
            conv_history = self._format_conversation_history(
                context.conversation_history
            )

            # Format reaction feedback
            reaction_feedback = self._format_reaction_patterns(
                context.reaction_patterns
            )

            # Generate sophisticated jest
            jest_response = self.jest_crafter(
                user_intelligence=user_intel_summary,
                jest_opportunities=jest_opportunities,
                paper_content=paper_content,
                user_feedback=user_feedback,
                jest_style=jest_style,
                conversation_history=conv_history,
                reaction_feedback=reaction_feedback,
            )

            return {
                "response": jest_response.sophisticated_jest,
                "conversation_hooks": jest_response.conversation_hooks,
                "confidence": (
                    float(jest_response.jest_confidence)
                    if jest_response.jest_confidence.replace(".", "").isdigit()
                    else 0.8
                ),
            }

        except Exception as e:
            print(f"Jest generation error: {e}")
            return self._fallback_jest_generation(context)

    def _fallback_jest_generation(self, context: JestContext) -> Dict[str, Any]:
        """Fallback jest generation when DSPy fails."""
        jest_opportunities = context.user_profile.get("jest_opportunities", "")
        user_feedback = context.paper_context.get("user_feedback", "")

        # Simple template-based jest generation
        if "JavaScript" in jest_opportunities:
            jest = f"Your observations about the paper are quite insightful. I particularly appreciate how they demonstrate the same attention to detail that must serve you well when navigating JavaScript's delightfully inconsistent type coercion behaviors. "
        elif "Python" in jest_opportunities:
            jest = f"The methodological rigor you're calling for here reminds me of the Zen of Python's emphasis on explicit over implicit - though I suspect like most of us, you've occasionally found 'practicality beats purity' to be a useful escape clause. "
        else:
            jest = f"Your technical perspective brings a refreshing clarity to these academic discussions. "

        jest += f"The specific point about '{user_feedback[:100]}...' raises intriguing questions about the intersection of practical implementation and theoretical frameworks."

        hooks = [
            "What's your take on the broader methodological implications?",
            "How does this align with your experience in software development?",
        ]

        return {
            "response": jest,
            "conversation_hooks": "; ".join(hooks),
            "confidence": 0.6,
        }

    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for DSPy processing."""
        if not history:
            return "No previous conversation."

        formatted = []
        for msg in history[-3:]:  # Last 3 messages
            author = msg.get("author", "Unknown")
            content = msg.get("body", "")[:200]  # Truncate long messages
            formatted.append(f"{author}: {content}...")

        return " | ".join(formatted)

    def _format_reaction_patterns(self, patterns: Dict[str, Any]) -> str:
        """Format reaction patterns for DSPy processing."""
        if not patterns:
            return "No previous reaction data available."

        engagement_score = patterns.get("engagement_score", 0.0)
        top_reactions = patterns.get("reaction_types", {})

        if top_reactions:
            top_emoji = max(top_reactions, key=top_reactions.get)
            return f"Previous engagement score: {engagement_score:.2f}, most common reaction: {top_emoji}"

        return f"Previous engagement score: {engagement_score:.2f}"

    def analyze_reaction_effectiveness(
        self, responses: List[str], reactions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze effectiveness of previous responses based on reactions."""
        try:
            response_text = " | ".join(responses[-5:])  # Last 5 responses
            reaction_data = json.dumps(reactions, default=str)
            engagement_data = f"Total reactions: {reactions.get('total_reactions', 0)}, Positive: {reactions.get('positive_reactions', 0)}"

            analysis = self.reaction_analyzer(
                previous_responses=response_text,
                emoji_reactions=reaction_data,
                user_engagement_data=engagement_data,
            )

            return {
                "effectiveness": analysis.effectiveness_analysis,
                "suggestions": analysis.optimization_suggestions,
                "insights": analysis.personalization_insights,
            }

        except Exception as e:
            print(f"Reaction analysis error: {e}")
            return {
                "effectiveness": "Limited data available for analysis",
                "suggestions": "Continue current approach with minor adjustments",
                "insights": "Monitor user engagement patterns for future optimization",
            }

    def forward(
        self,
        username: str,
        conversation_context: str,
        paper_context: Dict[str, Any],
        reaction_patterns: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Main forward pass for intelligent jest generation."""

        # Retrieve user intelligence
        user_intel = self.retrieve_user_intelligence(username, conversation_context)

        # Build jest context
        jest_context = JestContext(
            user_profile=user_intel,
            conversation_history=[],  # Would be populated from actual data
            paper_context=paper_context,
            reaction_patterns=reaction_patterns or {},
            jest_style_preferences={},
        )

        # Generate intelligent jest
        jest_result = self.generate_intelligent_jest(jest_context)

        return jest_result["response"]


class DSPyJestOptimizer:
    """Optimizer for DSPy jest generation with feedback loops."""

    @staticmethod
    def configure_for_jesting(model_key: str):
        """Configure DSPy with optimal settings for academic jesting."""
        try:
            lm = dspy.LM(
                model="openai/gpt-4.1-mini",  # Use GPT-4.1-mini for consistency
                api_key=model_key,
                api_base="https://openrouter.ai/api/v1",
                temperature=0.7,  # Higher temperature for creative jesting
                max_tokens=800,  # Allow for detailed responses
            )
            dspy.configure(lm=lm)
            return True
        except Exception as e:
            print(f"DSPy jest configuration error: {e}")
            return False

    @staticmethod
    def add_jest_examples():
        """Add few-shot examples for better jesting consistency."""
        examples = [
            dspy.Example(
                user_intelligence="JavaScript developer, 15 repos, strong frontend focus",
                jest_opportunities="JavaScript type coercion, async/await patterns",
                paper_content="Study on software reliability",
                user_feedback="The methodology seems flawed",
                sophisticated_jest="Your methodological concerns are well-founded - the same careful attention to edge cases that must serve you well when debugging those delightfully unpredictable JavaScript equality comparisons. The reliability issues you've identified here parallel some interesting patterns we see in frontend state management...",
                conversation_hooks="What specific reliability patterns have you encountered in your own development work?",
            ),
            dspy.Example(
                user_intelligence="Python developer, active in data science, 25+ repos",
                jest_opportunities="Python data science workflows, pandas operations",
                paper_content="Machine learning interpretability paper",
                user_feedback="Great insights on model transparency",
                sophisticated_jest="I'm delighted you appreciate the transparency aspects - there's something beautifully ironic about demanding interpretability in ML models while we routinely accept pandas' occasionally cryptic behavioral quirks as 'features.' Your enthusiasm for methodological clarity suggests someone who's spent quality time debugging those wonderfully expressive yet mysteriously failing data transformations...",
                conversation_hooks="How do you approach interpretability in your own data science work?",
            ),
        ]
        return examples


if __name__ == "__main__":
    # Example usage
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    if openrouter_key:
        DSPyJestOptimizer.configure_for_jesting(openrouter_key)

        engine = IntelligentJestEngine()

        # Test with sample data
        test_response = engine.forward(
            username="testuser",
            conversation_context="Discussion about software testing methodologies",
            paper_context={
                "content": "Research on automated testing approaches",
                "user_feedback": "The testing strategy lacks comprehensive coverage",
            },
        )

        print("🎭 Intelligent Jest Engine Test:")
        print(test_response)
