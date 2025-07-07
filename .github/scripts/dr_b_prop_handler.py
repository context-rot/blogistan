#!/usr/bin/env python3
"""
Dr. B. Prop Automated Research Response Handler

A clean, professional script that handles spam detection and automated responses
without the nightmare of YAML shell escaping.
"""

import os
import sys
import json
import re
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple


class GitHubIssueHandler:
    def __init__(self):
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        self.repository = os.environ.get("GITHUB_REPOSITORY")

        # Get issue data from environment
        self.issue_data = self._get_issue_data()

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
                    # For arrays, use --field key=@- and stdin
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

    def check_rate_limit(self, user: str) -> bool:
        """Check if user has exceeded rate limits (5 issues per 24h)."""
        try:
            # Get date 24 hours ago
            date_24h_ago = (datetime.utcnow() - timedelta(hours=24)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            # Search for recent issues by user
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

        # Length checks
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

        # AI analysis for sophisticated spam (if score is low so far)
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
                # Extract number from response
                match = re.search(r"^(\d+)", result.stdout.strip())
                return int(match.group(1)) if match else 5

        except Exception as e:
            print(f"AI analysis error: {e}")

        return 5  # Default moderate score if AI fails

    def generate_response(self, title: str, body: str) -> str:
        """Generate Dr. B. Prop's response using AI."""
        prompt = f"""You are Dr. B. Prop, Principal Investigator at the Context Decay Research Institute. You've received reader feedback on one of your papers published at Context Rot blog. 

Respond in character as a slightly pompous but ultimately well-meaning academic researcher. Be witty, acknowledge valid points, defend your research where appropriate, and maintain the satirical but scholarly tone of the blog.

Issue Title: {title}
Issue Body: {body}

Provide a thoughtful, in-character response that:
1. Acknowledges the reader's feedback
2. Addresses any technical points raised  
3. Maintains academic humor and tone
4. Thanks them for engaging with the research
5. Potentially suggests follow-up research directions

Keep it concise (2-3 paragraphs max) but substantive."""

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
                "500",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return result.stdout.strip()

        except Exception as e:
            print(f"Response generation error: {e}")

        # Fallback response
        return """Thank you for your thoughtful feedback on our research. Your observations contribute valuable perspective to the ongoing discourse on configuration proliferation in the computational linguistics domain. 

We will certainly consider these points for future iterations of our analysis framework. The peer review process, even in its automated form, remains essential to advancing our understanding of these complex socio-technical phenomena."""

    def post_comment(self, issue_number: int, response: str) -> bool:
        """Post Dr. B. Prop's response as a comment."""
        comment_body = f"""**Dr. B. Prop responds:**

{response}

---
*This response was generated by Dr. B. Prop's automated research assistant. For urgent matters, please contact the Context Decay Research Institute directly.*

*🤖 Automated response system powered by the same technology that's slowly consuming all human context.*"""

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
        """Generate and post Dr. B. Prop's response."""
        if not self.issue_data:
            print("No issue data available")
            return False

        title = self.issue_data.get("title", "")
        body = self.issue_data.get("body", "")
        issue_number = self.issue_data.get("number", 0)

        print(f"Generating response for issue #{issue_number}")

        # Generate response
        response = self.generate_response(title, body)

        # Post comment
        if self.post_comment(issue_number, response):
            print("Comment posted successfully")

            # Add label
            if self.add_label(issue_number, "research-reviewed"):
                print("Label added successfully")

            return True
        else:
            print("Failed to post comment")
            return False


def main():
    if len(sys.argv) < 2:
        print("Usage: dr_b_prop_handler.py [spam-detection|response-generation]")
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
