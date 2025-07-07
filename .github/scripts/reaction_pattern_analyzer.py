#!/usr/bin/env python3
"""
Dr. B. Prop - Reaction Pattern Analysis System
Analyzes emoji reactions to optimize future response generation
"""

import os
import json
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import pandas as pd


@dataclass
class ReactionAnalysis:
    """Analysis of emoji reaction patterns."""

    username: str
    reaction_history: Dict[str, List[Dict[str, Any]]]
    response_effectiveness: Dict[str, float]
    preferred_reaction_types: List[str]
    jest_response_scores: Dict[str, float]
    conversation_engagement_level: float
    last_analyzed: str


class ReactionPatternAnalyzer:
    """Analyzes emoji reactions to improve Dr. B. Prop's jesting effectiveness."""

    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.repository = os.environ.get("GITHUB_REPOSITORY")
        self.databricks_host = os.environ.get("DATABRICKS_HOST")
        self.databricks_token = os.environ.get("DATABRICKS_TOKEN")

    def _gh_api(self, endpoint: str, method: str = "GET") -> Optional[Dict]:
        """Make GitHub API calls with authentication."""
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        try:
            url = f"https://api.github.com/{endpoint}"
            response = requests.request(method, url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"GitHub API error for {endpoint}: {e}")
            return None

    def get_dr_b_prop_comments(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get all Dr. B. Prop comments from recent issues."""
        dr_b_prop_comments = []

        # Get recent issues with reader-feedback label
        since_date = (
            datetime.now(timezone.utc) - timedelta(days=days_back)
        ).isoformat()

        search_query = (
            f"repo:{self.repository} label:reader-feedback updated:>{since_date[:10]}"
        )
        search_results = self._gh_api(f"search/issues?q={search_query}&per_page=50")

        if not search_results or not search_results.get("items"):
            return []

        for issue in search_results["items"]:
            issue_number = issue["number"]

            # Get comments for this issue
            comments = self._gh_api(
                f"repos/{self.repository}/issues/{issue_number}/comments"
            )
            if comments:
                for comment in comments:
                    # Check if this is a Dr. B. Prop comment
                    if comment["user"][
                        "login"
                    ] == "github-actions[bot]" and "Dr. B. Prop responds:" in comment.get(
                        "body", ""
                    ):

                        # Get reactions for this comment
                        reactions = self._gh_api(
                            f"repos/{self.repository}/issues/comments/{comment['id']}/reactions"
                        )

                        dr_b_prop_comments.append(
                            {
                                "comment_id": comment["id"],
                                "issue_number": issue_number,
                                "body": comment["body"],
                                "created_at": comment["created_at"],
                                "reactions": reactions or [],
                                "original_user": issue.get("user", {}).get("login", ""),
                            }
                        )

        return dr_b_prop_comments

    def analyze_reaction_patterns(
        self, comments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze patterns in emoji reactions to Dr. B. Prop's responses."""
        reaction_stats = {
            "total_reactions": 0,
            "reaction_types": {},
            "positive_reactions": 0,
            "negative_reactions": 0,
            "engagement_score": 0.0,
            "user_specific_patterns": {},
        }

        positive_emojis = {"👍", "😄", "🎉", "❤️", "🚀", "👀"}
        negative_emojis = {"👎", "😕", "😞", "😠"}

        for comment_data in comments:
            reactions = comment_data.get("reactions", [])
            original_user = comment_data.get("original_user", "")

            if original_user not in reaction_stats["user_specific_patterns"]:
                reaction_stats["user_specific_patterns"][original_user] = {
                    "reactions": [],
                    "engagement_level": 0,
                    "preferred_emojis": {},
                }

            for reaction in reactions:
                emoji = reaction.get("content", "")
                reactor = reaction.get("user", {}).get("login", "")

                reaction_stats["total_reactions"] += 1
                reaction_stats["reaction_types"][emoji] = (
                    reaction_stats["reaction_types"].get(emoji, 0) + 1
                )

                if emoji in positive_emojis:
                    reaction_stats["positive_reactions"] += 1
                elif emoji in negative_emojis:
                    reaction_stats["negative_reactions"] += 1

                # Track user-specific patterns
                if reactor == original_user:
                    user_patterns = reaction_stats["user_specific_patterns"][
                        original_user
                    ]
                    user_patterns["reactions"].append(
                        {
                            "emoji": emoji,
                            "comment_id": comment_data["comment_id"],
                            "timestamp": reaction.get("created_at", ""),
                        }
                    )
                    user_patterns["preferred_emojis"][emoji] = (
                        user_patterns["preferred_emojis"].get(emoji, 0) + 1
                    )
                    user_patterns["engagement_level"] += 1

        # Calculate engagement score
        if reaction_stats["total_reactions"] > 0:
            reaction_stats["engagement_score"] = (
                reaction_stats["positive_reactions"]
                - reaction_stats["negative_reactions"]
            ) / reaction_stats["total_reactions"]

        return reaction_stats

    def identify_jest_effectiveness(
        self, comments: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Identify which types of jesting are most effective based on reactions."""
        jest_patterns = {
            "language_jests": ["JavaScript", "Python", "Java", "undefined", "null"],
            "documentation_jests": ["documentation", "README", "comments", "docs"],
            "ci_cd_jests": ["deployment", "testing", "CI/CD", "pipeline"],
            "verbose_jests": ["verbose", "concise", "dissertation", "brief"],
            "technical_jests": [
                "algorithm",
                "framework",
                "optimization",
                "architecture",
            ],
        }

        jest_scores = {}

        for jest_type, keywords in jest_patterns.items():
            total_reactions = 0
            positive_reactions = 0
            comments_with_jest = 0

            for comment_data in comments:
                body = comment_data.get("body", "").lower()

                # Check if this comment contains this type of jest
                if any(keyword.lower() in body for keyword in keywords):
                    comments_with_jest += 1
                    reactions = comment_data.get("reactions", [])

                    for reaction in reactions:
                        emoji = reaction.get("content", "")
                        total_reactions += 1

                        if emoji in {"👍", "😄", "🎉", "❤️", "🚀"}:
                            positive_reactions += 1

            # Calculate effectiveness score
            if total_reactions > 0:
                jest_scores[jest_type] = positive_reactions / total_reactions
            else:
                jest_scores[jest_type] = 0.0

        return jest_scores

    def generate_personalized_recommendations(
        self, user_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate personalized jesting recommendations for specific users."""
        recommendations = {}

        for username, patterns in user_patterns.items():
            if not patterns["reactions"]:
                continue

            user_rec = {
                "preferred_jest_intensity": "moderate",
                "effective_topics": [],
                "avoid_topics": [],
                "optimal_response_length": "medium",
                "engagement_strategy": "collegial_banter",
            }

            # Analyze emoji preferences
            preferred_emojis = patterns["preferred_emojis"]

            if preferred_emojis.get("😄", 0) > 2:
                user_rec["preferred_jest_intensity"] = "high"
                user_rec["engagement_strategy"] = "witty_banter"
            elif preferred_emojis.get("👍", 0) > preferred_emojis.get("😄", 0):
                user_rec["preferred_jest_intensity"] = "moderate"
                user_rec["engagement_strategy"] = "respectful_jest"

            if preferred_emojis.get("🚀", 0) > 1:
                user_rec["effective_topics"].append("technical_sophistication")
            if preferred_emojis.get("👀", 0) > 1:
                user_rec["effective_topics"].append("curiosity_hooks")

            # Adjust based on engagement level
            if patterns["engagement_level"] > 5:
                user_rec["optimal_response_length"] = "long"
            elif patterns["engagement_level"] < 2:
                user_rec["optimal_response_length"] = "short"

            recommendations[username] = user_rec

        return recommendations

    def store_analysis_results(self, analysis_data: Dict[str, Any]):
        """Store reaction analysis results for future use."""
        try:
            # For now, save to local file (would normally use Databricks)
            output_file = "/tmp/reaction_analysis.json"
            with open(output_file, "w") as f:
                json.dump(analysis_data, f, indent=2, default=str)

            print(f"Reaction analysis stored to {output_file}")
            print(
                f"Overall engagement score: {analysis_data.get('engagement_score', 0):.2f}"
            )
            print(
                f"Most effective jest types: {sorted(analysis_data.get('jest_effectiveness', {}).items(), key=lambda x: x[1], reverse=True)[:3]}"
            )

        except Exception as e:
            print(f"Error storing analysis results: {e}")

    def run_reaction_analysis(self):
        """Main workflow for analyzing reaction patterns."""
        try:
            print("Starting reaction pattern analysis...")

            # Get Dr. B. Prop comments from last 30 days
            comments = self.get_dr_b_prop_comments(days_back=30)
            print(f"Found {len(comments)} Dr. B. Prop comments to analyze")

            if not comments:
                print("No comments found for analysis")
                return

            # Analyze reaction patterns
            reaction_patterns = self.analyze_reaction_patterns(comments)

            # Identify jest effectiveness
            jest_effectiveness = self.identify_jest_effectiveness(comments)

            # Generate personalized recommendations
            user_patterns = reaction_patterns.get("user_specific_patterns", {})
            recommendations = self.generate_personalized_recommendations(user_patterns)

            # Compile analysis results
            analysis_results = {
                "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
                "comments_analyzed": len(comments),
                "reaction_patterns": reaction_patterns,
                "jest_effectiveness": jest_effectiveness,
                "personalized_recommendations": recommendations,
                "engagement_score": reaction_patterns.get("engagement_score", 0.0),
            }

            # Store results
            self.store_analysis_results(analysis_results)

            print("Reaction analysis completed successfully")

        except Exception as e:
            print(f"Reaction analysis error: {e}")


if __name__ == "__main__":
    analyzer = ReactionPatternAnalyzer()
    analyzer.run_reaction_analysis()
