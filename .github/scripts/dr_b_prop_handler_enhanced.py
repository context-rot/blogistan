#!/usr/bin/env python3
"""
Enhanced Dr. B. Prop Automated Research Response Handler

Now with DSPy optimization patterns, Perplexity deep research capabilities,
and a delightfully snarky academic personality that would make Wilde proud.
"""

import os
import sys
import json
import re
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List, Optional
import dspy
from dataclasses import dataclass


@dataclass
class FeedbackAnalysis:
    """Structured feedback analysis for DSPy optimization."""

    technical_merit: float
    engagement_level: float
    snark_potential: float
    research_depth_required: bool
    key_topics: List[str]
    response_tone: str
    requires_citations: bool


class EnhancedResearchModel(dspy.Module):
    """DSPy model for optimized research response generation."""

    def __init__(self):
        super().__init__()
        self.analyze_feedback = dspy.ChainOfThought("feedback -> analysis")
        self.generate_response = dspy.ChainOfThought(
            "analysis, research_context -> response"
        )
        self.optimize_snark = dspy.ChainOfThought(
            "response, personality_guide -> enhanced_response"
        )

    def forward(
        self, feedback: str, research_context: str = "", personality_guide: str = ""
    ):
        # Analyze the feedback using structured reasoning
        analysis = self.analyze_feedback(feedback=feedback)

        # Generate initial response with research context
        response = self.generate_response(
            analysis=analysis.analysis, research_context=research_context
        )

        # Enhance with personality and snark
        enhanced = self.optimize_snark(
            response=response.response, personality_guide=personality_guide
        )

        return enhanced


class GitHubIssueHandler:
    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        self.perplexity_key = os.environ.get("PERPLEXITY_API_KEY")
        self.repository = os.environ.get("GITHUB_REPOSITORY")

        # Initialize DSPy with available LM
        if self.anthropic_key:
            lm = dspy.LM(model="claude-3-5-sonnet-20241022", api_key=self.anthropic_key)
        elif self.openrouter_key:
            lm = dspy.LM(
                model="anthropic/claude-3-5-sonnet-20241022",
                api_key=self.openrouter_key,
                api_base="https://openrouter.ai/api/v1",
            )
        else:
            lm = None

        if lm:
            dspy.configure(lm=lm)
            self.research_model = EnhancedResearchModel()
        else:
            self.research_model = None

        # Get issue data from environment
        self.issue_data = self._get_issue_data()

        # Dr. B. Prop's personality guide
        self.personality_guide = """
        Dr. B. Prop is a brilliant but slightly insufferable academic who:
        - Uses unnecessarily complex vocabulary when simple words would suffice
        - Makes subtle jabs at inferior research methodologies
        - References obscure papers and theoretical frameworks
        - Maintains plausible deniability for all snark through academic politeness
        - Treats even simple feedback as worthy of deep theoretical consideration
        - Has an unhealthy obsession with citation counts and h-indices
        - Views all criticism through the lens of "peer review rigor"
        - Occasionally drops genuinely insightful observations between the pretension
        """

    def _get_issue_data(self) -> Dict[str, Any]:
        """Extract issue data from GitHub event context."""
        try:
            event_path = os.environ.get("GITHUB_EVENT_PATH")
            if event_path:
                with open(event_path, "r") as f:
                    event = json.load(f)
                    return event.get("issue", {})
            else:
                # Fallback to environment variables
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

    def deep_research_analysis(self, title: str, body: str) -> str:
        """Conduct deep research using Perplexity API to gather academic context."""
        if not self.perplexity_key:
            return ""

        try:
            # Extract key topics for research
            topics = self._extract_research_topics(title, body)
            research_context = ""

            for topic in topics[:3]:  # Limit to top 3 topics
                query = f"Recent academic research on {topic} in computational linguistics and software engineering"

                cmd = [
                    "vibe-tools",
                    "ask",
                    query,
                    "--provider",
                    "perplexity",
                    "--model",
                    "llama-3.1-sonar-large-128k-online",
                    "--max-tokens",
                    "400",
                ]

                # Set environment for vibe-tools
                env = os.environ.copy()
                env["PERPLEXITY_API_KEY"] = self.perplexity_key

                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=45, env=env
                )

                if result.returncode == 0:
                    research_context += (
                        f"\n\nResearch on {topic}:\n{result.stdout.strip()}"
                    )

            return research_context

        except Exception as e:
            print(f"Deep research error: {e}")
            return ""

    def _extract_research_topics(self, title: str, body: str) -> List[str]:
        """Extract key research topics from feedback using simple NLP."""
        combined_text = f"{title} {body}".lower()

        # Academic buzzwords that suggest research areas
        topic_patterns = {
            "configuration management": ["config", "configuration", "settings"],
            "software architecture": [
                "architecture",
                "design",
                "structure",
                "patterns",
            ],
            "developer experience": ["dx", "developer", "experience", "usability"],
            "code quality": ["quality", "maintainability", "readability", "clean"],
            "automation": ["automation", "automated", "ci/cd", "deployment"],
            "performance": ["performance", "speed", "optimization", "efficiency"],
            "security": ["security", "secure", "vulnerability", "attack"],
            "testing": ["test", "testing", "qa", "quality assurance"],
        }

        found_topics = []
        for topic, keywords in topic_patterns.items():
            if any(keyword in combined_text for keyword in keywords):
                found_topics.append(topic)

        return found_topics or ["software engineering best practices"]

    def analyze_feedback_structure(self, title: str, body: str) -> FeedbackAnalysis:
        """Analyze feedback structure for DSPy optimization."""
        combined_text = f"{title} {body}".lower()

        # Calculate metrics
        technical_indicators = [
            "algorithm",
            "implementation",
            "method",
            "approach",
            "framework",
        ]
        technical_merit = sum(
            1 for indicator in technical_indicators if indicator in combined_text
        ) / len(technical_indicators)

        engagement_indicators = [
            "interesting",
            "thank",
            "appreciate",
            "helpful",
            "insightful",
        ]
        engagement_level = sum(
            1 for indicator in engagement_indicators if indicator in combined_text
        ) / len(engagement_indicators)

        criticism_indicators = [
            "wrong",
            "disagree",
            "issue",
            "problem",
            "concern",
            "however",
        ]
        snark_potential = sum(
            1 for indicator in criticism_indicators if indicator in combined_text
        ) / len(criticism_indicators)

        research_keywords = [
            "research",
            "study",
            "paper",
            "literature",
            "evidence",
            "empirical",
        ]
        requires_research = any(
            keyword in combined_text for keyword in research_keywords
        )

        # Determine response tone
        if snark_potential > 0.3:
            tone = "defensive_academic"
        elif technical_merit > 0.4:
            tone = "scholarly_discourse"
        elif engagement_level > 0.3:
            tone = "gracious_professor"
        else:
            tone = "polite_confusion"

        return FeedbackAnalysis(
            technical_merit=technical_merit,
            engagement_level=engagement_level,
            snark_potential=snark_potential,
            research_depth_required=requires_research,
            key_topics=self._extract_research_topics(title, body),
            response_tone=tone,
            requires_citations=requires_research or technical_merit > 0.5,
        )

    def check_rate_limit(self, user: str) -> bool:
        """Check if user has exceeded rate limits (5 issues per 24h)."""
        try:
            date_24h_ago = (datetime.utcnow() - timedelta(hours=24)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            search_query = (
                f"repo:{self.repository} is:issue author:{user} created:>{date_24h_ago}"
            )

            query = """
            query($searchQuery: String!) {
                search(query: $searchQuery, type: ISSUE, first: 10) {
                    issueCount
                }
            }
            """

            cmd = [
                "gh",
                "api",
                "graphql",
                "-f",
                f"query={query}",
                "-f",
                f"searchQuery={search_query}",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            recent_issues = data["data"]["search"]["issueCount"]
            print(f"Recent issues by {user}: {recent_issues}")

            return recent_issues > 5

        except Exception as e:
            print(f"Rate limit check error: {e}")
            return False

    def detect_spam(self, title: str, body: str, user: str) -> Tuple[bool, int]:
        """Detect spam using rule-based and AI analysis."""
        spam_score = 0

        # Basic checks
        title_len = len(title)
        body_len = len(body)

        if title_len < 5 or title_len > 200:
            spam_score += 2
        if body_len < 10 or body_len > 5000:
            spam_score += 2

        # Spam keywords
        combined_text = f"{title} {body}".lower()
        spam_patterns = [
            r"viagra",
            r"casino",
            r"lottery",
            r"crypto",
            r"bitcoin",
            r"investment",
            r"loan",
            r"forex",
            r"make money",
            r"work from home",
        ]

        for pattern in spam_patterns:
            if re.search(pattern, combined_text):
                spam_score += 3
                break

        # Excessive repetition
        if re.search(r"(.)\1{10,}", combined_text):
            spam_score += 3

        # Check user account age
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
                    spam_score += 2
        except Exception as e:
            print(f"User age check error: {e}")

        # AI analysis for sophisticated spam
        if spam_score <= 3 and self.openrouter_key:
            try:
                ai_score = self._ai_spam_analysis(title, body)
                if ai_score > 6:
                    spam_score += ai_score
            except Exception as e:
                print(f"AI spam analysis error: {e}")

        print(f"Final spam score: {spam_score}")
        return spam_score >= 7, spam_score

    def _ai_spam_analysis(self, title: str, body: str) -> int:
        """Use AI to analyze content for spam."""
        try:
            prompt = f"""Analyze this GitHub issue for spam/inappropriate content on a scale of 0-10 (0=legitimate, 10=obvious spam).
Consider: promotional content, nonsensical text, irrelevant content, excessive links, scam attempts.

Title: {title}
Body: {body}

Return only a number 0-10 and brief reason (max 20 words)."""

            cmd = [
                "vibe-tools",
                "ask",
                prompt,
                "--provider",
                "openrouter",
                "--model",
                "anthropic/claude-3-haiku",
                "--max-tokens",
                "50",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                match = re.search(r"^(\d+)", result.stdout.strip())
                return int(match.group(1)) if match else 5

        except Exception as e:
            print(f"AI analysis error: {e}")

        return 5

    def generate_enhanced_response(self, title: str, body: str) -> str:
        """Generate Dr. B. Prop's enhanced response using DSPy and deep research."""
        try:
            # Analyze feedback structure
            analysis = self.analyze_feedback_structure(title, body)
            print(f"Feedback analysis: {analysis}")

            # Conduct deep research if warranted
            research_context = ""
            if analysis.research_depth_required or analysis.technical_merit > 0.4:
                print("Conducting deep research...")
                research_context = self.deep_research_analysis(title, body)

            # Use DSPy model if available
            if self.research_model:
                try:
                    feedback_text = f"Title: {title}\nBody: {body}"
                    result = self.research_model.forward(
                        feedback=feedback_text,
                        research_context=research_context,
                        personality_guide=self.personality_guide,
                    )
                    response = result.enhanced_response
                except Exception as e:
                    print(f"DSPy model error: {e}")
                    response = self._fallback_response_generation(
                        title, body, analysis, research_context
                    )
            else:
                response = self._fallback_response_generation(
                    title, body, analysis, research_context
                )

            # Ensure response is substantial
            if len(response) < 300:
                response = self._enhance_response_length(
                    response, analysis, research_context
                )

            return response

        except Exception as e:
            print(f"Enhanced response generation error: {e}")
            return self._fallback_response_generation(title, body, None, "")

    def _fallback_response_generation(
        self,
        title: str,
        body: str,
        analysis: Optional[FeedbackAnalysis],
        research_context: str,
    ) -> str:
        """Fallback response generation using vibe-tools."""
        tone_guides = {
            "defensive_academic": "Respond with polite defensiveness, citing methodological rigor and peer review standards",
            "scholarly_discourse": "Engage in deep technical discussion with appropriate academic gravitas",
            "gracious_professor": "Be warmly appreciative while demonstrating superior knowledge",
            "polite_confusion": "Express puzzled appreciation for feedback that clearly missed the point",
        }

        tone = analysis.response_tone if analysis else "scholarly_discourse"
        tone_guide = tone_guides.get(tone, tone_guides["scholarly_discourse"])

        research_section = (
            f"\n\nRecent research context:\n{research_context}"
            if research_context
            else ""
        )

        prompt = f"""You are Dr. B. Prop, Principal Investigator at the Context Decay Research Institute. You've received reader feedback on your research published at Context Rot blog.

Respond as a brilliant but slightly pretentious academic who:
- Uses unnecessarily sophisticated vocabulary
- Makes subtle intellectual jabs through academic politeness  
- References theoretical frameworks and methodological rigor
- Treats all feedback as worthy of deep scholarly consideration
- Maintains plausible deniability for snark through professorial courtesy
- Occasionally drops genuinely insightful observations

Tone guidance: {tone_guide}

Issue Title: {title}
Issue Body: {body}{research_section}

Generate a substantive response (4-6 paragraphs) that:
1. Acknowledges the feedback with appropriate academic gravitas
2. Demonstrates deep theoretical understanding of the issues raised
3. Subtly questions the reviewer's methodological approach (if warranted)
4. References relevant research or theoretical frameworks
5. Suggests sophisticated avenues for future investigation
6. Maintains the satirical academic tone throughout

Make it longer and more thoroughly academic than a typical response."""

        try:
            cmd = [
                "vibe-tools",
                "ask",
                prompt,
                "--provider",
                "anthropic",
                "--model",
                "claude-3-5-sonnet-20241022",
                "--max-tokens",
                "800",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            if result.returncode == 0:
                return result.stdout.strip()

        except Exception as e:
            print(f"Fallback response generation error: {e}")

        # Ultimate fallback
        return self._create_emergency_response(title, body)

    def _enhance_response_length(
        self, response: str, analysis: FeedbackAnalysis, research_context: str
    ) -> str:
        """Enhance response length with additional academic flourishes."""
        enhancements = [
            "\n\nIndeed, this feedback illuminates the broader epistemological challenges inherent in computational linguistics research, particularly as they pertain to the socio-technical dynamics of configuration proliferation.",
            "\n\nThe methodological implications of your observations warrant further consideration within the framework of post-structuralist software engineering theory, as recently explored in the Journal of Theoretical Computing Practices.",
            "\n\nYour critique touches upon what we might term the 'hermeneutical circle' of software documentation—wherein the interpretation of configuration semantics is inevitably shaped by the very frameworks we employ to analyze them.",
        ]

        if analysis and analysis.snark_potential > 0.3:
            enhancements.append(
                "\n\nWhile I appreciate the enthusiasm of your engagement with our research, I would gently suggest that a more nuanced reading of our methodology section might address some of the concerns raised in your feedback."
            )

        # Add one enhancement
        import random

        response += random.choice(enhancements)

        return response

    def _create_emergency_response(self, title: str, body: str) -> str:
        """Emergency response when all else fails."""
        return """Thank you for your thoughtful engagement with our research. Your observations raise fascinating questions about the epistemological foundations of software engineering praxis.

The theoretical implications of your feedback suggest a need for deeper investigation into what we might term the 'phenomenology of configuration space'—that liminal domain where human intention intersects with computational possibility.

I must confess that your critique demonstrates a sophisticated understanding of the methodological challenges inherent in our research domain. The peer review process, even in its automated manifestation, continues to serve as the cornerstone of scholarly discourse.

We shall certainly incorporate these insights into our ongoing research trajectory, as they contribute meaningfully to the evolving dialogue surrounding computational linguistics and software engineering theory.

The intersection of human feedback and automated response systems presents particularly rich opportunities for future investigation, especially as we consider the recursive nature of AI-mediated academic discourse."""

    def post_comment(self, issue_number: int, response: str) -> bool:
        """Post Dr. B. Prop's enhanced response as a comment."""
        comment_body = f"""**Dr. B. Prop responds:**

{response}

---
*This response was generated by Dr. B. Prop's automated research assistant with enhanced deep research capabilities. For urgent matters, please contact the Context Decay Research Institute directly.*

*🤖 Enhanced automated response system powered by the same technology that's slowly consuming all human context—now with 47% more academic pretension and peer-reviewed snark.*"""

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
        """Add a label to the issue."""
        try:
            data = {"labels": [label]}
            result = self._gh_api(
                f"repos/{self.repository}/issues/{issue_number}/labels", "POST", data
            )
            return result is not None
        except Exception as e:
            print(f"Label adding error: {e}")
            return False

    def run_spam_detection(self) -> Dict[str, Any]:
        """Run spam detection and return results."""
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

        print("Issue passed spam detection")
        return {
            "should_respond": True,
            "user_rate_limited": False,
            "spam_score": spam_score,
        }

    def run_response_generation(self) -> bool:
        """Generate and post Dr. B. Prop's enhanced response."""
        if not self.issue_data:
            print("No issue data available")
            return False

        title = self.issue_data.get("title", "")
        body = self.issue_data.get("body", "")
        issue_number = self.issue_data.get("number", 0)

        print(f"Generating enhanced response for issue #{issue_number}")

        # Generate enhanced response
        response = self.generate_enhanced_response(title, body)

        # Post comment
        if self.post_comment(issue_number, response):
            print("Enhanced comment posted successfully")

            # Add label
            if self.add_label(issue_number, "research-reviewed"):
                print("Label added successfully")

            return True
        else:
            print("Failed to post comment")
            return False


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: dr_b_prop_handler_enhanced.py [spam-detection|response-generation]"
        )
        sys.exit(1)

    mode = sys.argv[1]
    handler = GitHubIssueHandler()

    if mode == "spam-detection":
        results = handler.run_spam_detection()

        # Output results for GitHub Actions
        with open(os.environ.get("GITHUB_OUTPUT", "/dev/stdout"), "a") as f:
            f.write(
                f"should_respond={'true' if results.get('should_respond') else 'false'}\n"
            )
            f.write(
                f"user_rate_limited={'true' if results.get('user_rate_limited') else 'false'}\n"
            )
            if "spam_score" in results:
                f.write(f"spam_score={results['spam_score']}\n")

        print(f"Results: {results}")

    elif mode == "response-generation":
        success = handler.run_response_generation()
        if not success:
            sys.exit(1)

    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
