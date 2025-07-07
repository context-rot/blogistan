#!/usr/bin/env python3
"""
Dr. B. Prop - User Intelligence Collection System
Sophisticated analysis of user behavior, code patterns, and preferences for academic jesting
"""

import os
import json
import time
import requests
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import pandas as pd
from databricks import sql
from databricks.sdk import WorkspaceClient
import re


@dataclass
class UserProfile:
    """Comprehensive user profile for intelligent academic jesting."""

    username: str
    account_age_days: int
    total_repos: int
    followers: int
    following: int

    # Code analysis
    primary_languages: List[str]
    code_quality_indicators: Dict[str, float]
    repository_patterns: Dict[str, Any]

    # Behavioral patterns
    interaction_style: str
    comment_sentiment: float
    emoji_preferences: Dict[str, int]
    reaction_patterns: Dict[str, List[str]]

    # Academic indicators
    research_indicators: List[str]
    technical_sophistication: float
    domain_expertise: List[str]

    # Jest targets (areas for sophisticated academic humor)
    jest_opportunities: Dict[str, str]
    preferred_jest_style: str

    # Interaction history with Dr. B. Prop
    previous_interactions: List[Dict[str, Any]]
    response_effectiveness: Dict[str, float]

    # Metadata
    last_updated: str
    confidence_score: float


class UserIntelligenceCollector:
    """Sophisticated user analysis system for academic discourse enhancement."""

    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.databricks_host = os.environ.get("DATABRICKS_HOST")
        self.databricks_token = os.environ.get("DATABRICKS_TOKEN")
        self.repository = os.environ.get("GITHUB_REPOSITORY")

        # Initialize Databricks client
        self.workspace_client = WorkspaceClient(
            host=self.databricks_host, token=self.databricks_token
        )

        # Get current issue/comment context
        self.event_data = self._get_event_data()

    def _get_event_data(self) -> Dict[str, Any]:
        """Extract event data from GitHub context."""
        try:
            event_path = os.environ.get("GITHUB_EVENT_PATH")
            if event_path:
                with open(event_path, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading event data: {e}")
            return {}

    def _gh_api(
        self, endpoint: str, method: str = "GET", params: Dict = None
    ) -> Optional[Dict]:
        """Make GitHub API calls with authentication and proper error handling."""
        if not self.github_token:
            print("GitHub token not available")
            return None

        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Dr-B-Prop-Intelligence-Bot/1.0",
        }

        try:
            url = f"https://api.github.com/{endpoint}"
            print(f"GitHub API call: {method} {url}")

            response = requests.request(
                method, url, headers=headers, params=params, timeout=30
            )

            print(f"GitHub API response: {response.status_code}")

            # Handle rate limiting
            if response.status_code == 403:
                reset_time = response.headers.get("X-RateLimit-Reset")
                print(f"GitHub API rate limited. Reset time: {reset_time}")
                return None

            # Handle 422 validation errors
            if response.status_code == 422:
                print(f"GitHub API validation error: {response.text}")
                return None

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            print(f"GitHub API timeout for {endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"GitHub API request error for {endpoint}: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            return None
        except Exception as e:
            print(f"GitHub API error for {endpoint}: {e}")
            return None

    def analyze_user_repositories(self, username: str) -> Dict[str, Any]:
        """Analyze user's repositories for patterns and quality indicators."""
        repos_data = self._gh_api(f"users/{username}/repos?per_page=100")
        if not repos_data:
            return {}

        # Language analysis
        languages = {}
        total_size = 0
        repo_patterns = {
            "fork_ratio": 0,
            "has_documentation": 0,
            "uses_ci_cd": 0,
            "recent_activity": 0,
            "star_ratio": 0,
        }

        for repo in repos_data:
            if repo["size"] > 0:
                total_size += repo["size"]

                # Get repository languages
                lang_data = self._gh_api(f"repos/{repo['full_name']}/languages")
                if lang_data:
                    for lang, bytes_count in lang_data.items():
                        languages[lang] = languages.get(lang, 0) + bytes_count

                # Analyze repository patterns
                if repo["fork"]:
                    repo_patterns["fork_ratio"] += 1

                if repo["has_wiki"] or "README" in str(repo):
                    repo_patterns["has_documentation"] += 1

                # Check for CI/CD indicators
                workflows = self._gh_api(f"repos/{repo['full_name']}/actions/workflows")
                if workflows and workflows.get("total_count", 0) > 0:
                    repo_patterns["uses_ci_cd"] += 1

                # Recent activity (last 6 months)
                updated = datetime.fromisoformat(
                    repo["updated_at"].replace("Z", "+00:00")
                )
                if (datetime.now(timezone.utc) - updated).days < 180:
                    repo_patterns["recent_activity"] += 1

                repo_patterns["star_ratio"] += repo["stargazers_count"]

        # Normalize patterns
        repo_count = len([r for r in repos_data if not r["fork"] or r["size"] > 0])
        if repo_count > 0:
            for key in repo_patterns:
                if key != "star_ratio":
                    repo_patterns[key] = repo_patterns[key] / repo_count

        # Get top languages
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        top_languages = [lang for lang, _ in sorted_langs[:5]]

        return {
            "primary_languages": top_languages,
            "repository_patterns": repo_patterns,
            "total_repos_analyzed": len(repos_data),
            "code_quality_score": self._calculate_code_quality_score(repo_patterns),
        }

    def _calculate_code_quality_score(self, patterns: Dict[str, float]) -> float:
        """Calculate a code quality score based on repository patterns."""
        score = 0.0

        # Documentation bonus
        score += patterns.get("has_documentation", 0) * 0.3

        # CI/CD usage bonus
        score += patterns.get("uses_ci_cd", 0) * 0.25

        # Recent activity bonus
        score += patterns.get("recent_activity", 0) * 0.2

        # Original work bonus (non-forks)
        score += (1 - patterns.get("fork_ratio", 1)) * 0.25

        return min(score, 1.0)

    def analyze_interaction_style(self, username: str) -> Dict[str, Any]:
        """Analyze user's commenting and interaction patterns."""
        # Get recent issues and PRs created by user with safer query
        try:
            # Use a simpler, more reliable search query
            from urllib.parse import quote

            search_query = quote(f"author:{username} type:issue")
            search_endpoint = f"search/issues?q={search_query}&per_page=20&sort=updated"

            print(f"Searching for user interactions: {search_query}")
            search_results = self._gh_api(search_endpoint)
        except Exception as e:
            print(f"Error in search query construction: {e}")
            search_results = None

        if not search_results or not search_results.get("items"):
            return {"interaction_style": "minimal", "comment_sentiment": 0.5}

        # Analyze comment patterns
        comment_lengths = []
        technical_terms = 0
        question_count = 0
        total_comments = 0

        for item in search_results["items"][:20]:  # Analyze recent 20 items
            if item.get("body"):
                body = item["body"]
                comment_lengths.append(len(body))
                total_comments += 1

                # Count technical terms
                tech_patterns = [
                    r"\b(algorithm|function|class|method|variable|array|object)\b",
                    r"\b(database|api|framework|library|repository|deployment)\b",
                    r"\b(performance|optimization|scalability|security|testing)\b",
                ]

                for pattern in tech_patterns:
                    technical_terms += len(re.findall(pattern, body.lower()))

                # Count questions
                question_count += body.count("?")

        # Determine interaction style
        avg_length = (
            sum(comment_lengths) / len(comment_lengths) if comment_lengths else 0
        )
        tech_density = technical_terms / total_comments if total_comments > 0 else 0
        question_ratio = question_count / total_comments if total_comments > 0 else 0

        if avg_length > 500 and tech_density > 5:
            style = "verbose_technical"
        elif question_ratio > 0.3:
            style = "inquisitive"
        elif tech_density > 3:
            style = "technical"
        elif avg_length > 200:
            style = "detailed"
        else:
            style = "concise"

        return {
            "interaction_style": style,
            "average_comment_length": avg_length,
            "technical_density": tech_density,
            "question_ratio": question_ratio,
            "comment_sentiment": 0.6,  # Placeholder - could use sentiment analysis
        }

    def identify_jest_opportunities(
        self, profile_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Identify sophisticated opportunities for academic jesting."""
        opportunities = {}

        # Language-based jests
        languages = profile_data.get("primary_languages", [])
        if "JavaScript" in languages:
            opportunities["js_jest"] = (
                "the eternal struggle between 'undefined' and 'null' that haunts your repositories"
            )
        if "Python" in languages:
            opportunities["python_jest"] = (
                "your apparent devotion to the Zen of Python, though 'explicit is better than implicit' seems negotiable"
            )
        if "Java" in languages:
            opportunities["java_jest"] = (
                "the beautiful verbosity that only enterprise-grade AbstractFactoryFactoryBeans can provide"
            )

        # Repository pattern jests
        patterns = profile_data.get("repository_patterns", {})
        if patterns.get("fork_ratio", 0) > 0.7:
            opportunities["fork_jest"] = (
                "your impressive collection of other people's code with minimal modifications"
            )
        if patterns.get("has_documentation", 0) < 0.3:
            opportunities["docs_jest"] = (
                "the bold assumption that your code is so intuitive it documents itself"
            )
        if patterns.get("uses_ci_cd", 0) < 0.2:
            opportunities["cicd_jest"] = (
                "the thrilling life of manual deployment and prayer-based testing"
            )

        # Interaction style jests
        style = profile_data.get("interaction_style", "")
        if style == "verbose_technical":
            opportunities["verbosity_jest"] = (
                "your delightful ability to turn a simple bug report into a dissertation"
            )
        elif style == "concise":
            opportunities["brevity_jest"] = (
                "the minimalist approach to communication that leaves so much to interpretation"
            )

        return opportunities

    def determine_jest_style(self, profile_data: Dict[str, Any]) -> str:
        """Determine the most effective jesting style for this user."""
        code_quality = profile_data.get("code_quality_score", 0.5)
        interaction_style = profile_data.get("interaction_style", "")
        technical_density = profile_data.get("technical_density", 0)

        if code_quality > 0.7 and technical_density > 5:
            return "sophisticated_peer"  # Treat as technical equal
        elif interaction_style == "verbose_technical":
            return "gentle_deflation"  # Playfully deflate verbosity
        elif interaction_style == "concise":
            return "elaborate_response"  # Match brevity with elaborate analysis
        elif code_quality < 0.3:
            return "educational_jest"  # Jest while educating
        else:
            return "collegial_banter"  # Standard academic banter

    def collect_emoji_reactions(self, username: str) -> Dict[str, int]:
        """Analyze emoji reaction patterns for this user."""
        # This would typically require webhook data or periodic polling
        # For now, return placeholder data structure
        return {"👍": 0, "👎": 0, "😄": 0, "🎉": 0, "😕": 0, "❤️": 0, "🚀": 0, "👀": 0}

    def build_user_profile(self, username: str) -> UserProfile:
        """Build comprehensive user profile for intelligent academic discourse."""
        print(f"Building intelligence profile for user: {username}")

        # Get basic user data
        user_data = self._gh_api(f"users/{username}")
        if not user_data:
            return None

        # Calculate account age
        created_at = datetime.fromisoformat(
            user_data["created_at"].replace("Z", "+00:00")
        )
        account_age = (datetime.now(timezone.utc) - created_at).days

        # Analyze repositories
        repo_analysis = self.analyze_user_repositories(username)

        # Analyze interaction patterns
        interaction_analysis = self.analyze_interaction_style(username)

        # Identify jest opportunities
        profile_data = {**repo_analysis, **interaction_analysis}
        jest_opportunities = self.identify_jest_opportunities(profile_data)
        jest_style = self.determine_jest_style(profile_data)

        # Build profile
        profile = UserProfile(
            username=username,
            account_age_days=account_age,
            total_repos=user_data.get("public_repos", 0),
            followers=user_data.get("followers", 0),
            following=user_data.get("following", 0),
            primary_languages=repo_analysis.get("primary_languages", []),
            code_quality_indicators={
                "overall_score": repo_analysis.get("code_quality_score", 0.5)
            },
            repository_patterns=repo_analysis.get("repository_patterns", {}),
            interaction_style=interaction_analysis.get("interaction_style", "minimal"),
            comment_sentiment=interaction_analysis.get("comment_sentiment", 0.5),
            emoji_preferences=self.collect_emoji_reactions(username),
            reaction_patterns={},
            research_indicators=[],
            technical_sophistication=repo_analysis.get("code_quality_score", 0.5),
            domain_expertise=repo_analysis.get("primary_languages", [])[:3],
            jest_opportunities=jest_opportunities,
            preferred_jest_style=jest_style,
            previous_interactions=[],
            response_effectiveness={},
            last_updated=datetime.now(timezone.utc).isoformat(),
            confidence_score=0.8,
        )

        return profile

    def store_profile_in_databricks(self, profile: UserProfile):
        """Store user profile in Databricks for fast retrieval."""
        try:
            # Convert profile to dictionary
            profile_dict = asdict(profile)
            profile_json = json.dumps(profile_dict, default=str)

            # Create DataFrame
            df = pd.DataFrame([profile_dict])

            # Store in Databricks (using Unity Catalog)
            table_name = "dr_b_prop.user_intelligence.profiles"

            # For now, print the profile (would normally write to Databricks)
            print(f"Storing profile for {profile.username}:")
            print(f"Jest style: {profile.preferred_jest_style}")
            print(f"Opportunities: {list(profile.jest_opportunities.keys())}")
            print(f"Technical sophistication: {profile.technical_sophistication}")

            # TODO: Implement actual Databricks storage when lakehouse features are available
            # df.write.mode("append").saveAsTable(table_name)

        except Exception as e:
            print(f"Error storing profile in Databricks: {e}")

    def run_intelligence_collection(self):
        """Main workflow for collecting user intelligence."""
        try:
            # Get user from current event
            user = None
            if "issue" in self.event_data:
                user = self.event_data["issue"].get("user", {}).get("login")
            elif "comment" in self.event_data:
                user = self.event_data["comment"].get("user", {}).get("login")

            if not user:
                print("No user found in event data")
                return

            print(f"Collecting intelligence for user: {user}")

            # Build comprehensive profile
            profile = self.build_user_profile(user)
            if profile:
                # Store in Databricks
                self.store_profile_in_databricks(profile)
                print(f"Intelligence collection completed for {user}")
            else:
                print(f"Failed to build profile for {user}")

        except Exception as e:
            print(f"Intelligence collection error: {e}")


if __name__ == "__main__":
    collector = UserIntelligenceCollector()
    collector.run_intelligence_collection()
