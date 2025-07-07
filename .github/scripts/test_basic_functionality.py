#!/usr/bin/env python3
"""
Basic functionality tests for Dr. B. Prop Handler v2.0
Tests core functionality without DSPy dependencies
"""

import os
import sys
import json
import unittest
from unittest.mock import Mock, patch
import tempfile
from datetime import datetime

# Set up environment before imports
os.environ["GITHUB_TOKEN"] = "test_token"
os.environ["GITHUB_REPOSITORY"] = "test/repo"

# Add the scripts directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dr_b_prop_handler_v2 import (
        ContextualDrBProp,
        ConversationContext,
        ResearchAnalysis,
        SnarkProfile,
    )

    HANDLER_AVAILABLE = True
except ImportError as e:
    print(f"Handler import error: {e}")
    HANDLER_AVAILABLE = False


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality without DSPy."""

    def setUp(self):
        """Set up test environment."""
        if not HANDLER_AVAILABLE:
            self.skipTest("Handler not available")

        self.handler = ContextualDrBProp()
        self.handler.issue_data = {
            "number": 123,
            "title": "Test Issue",
            "body": "Test feedback about methodology.",
            "user": {"login": "test_user"},
            "labels": [{"name": "reader-feedback"}],
        }

    def test_spam_detection_basic(self):
        """Test basic spam detection."""
        # Legitimate feedback
        is_spam, score = self.handler.detect_spam(
            "Methodology feedback",
            "I have concerns about the empirical validation approach used in this research.",
            "academic_user",
        )
        self.assertFalse(is_spam)
        self.assertLess(score, 8)

        # Obvious spam
        is_spam, score = self.handler.detect_spam(
            "Make Money Fast!!!",
            "Bitcoin investment opportunity!!! GUARANTEED RETURNS!!!",
            "spammer",
        )
        self.assertTrue(is_spam)
        self.assertGreaterEqual(score, 8)

    def test_context_extraction(self):
        """Test conversation context extraction."""
        title = 'Feedback on "Test Paper Title"'
        body = """## My Feedback
        Great paper! Found it at https://context-rot.com/papers/test.html
        
        ## Context
        - Line: 42"""

        context = self.handler.extract_conversation_context(title, body)

        self.assertEqual(context.paper_url, "https://context-rot.com/papers/test.html")
        self.assertEqual(context.paper_title, "Test Paper Title")
        self.assertEqual(context.line_number, 42)

    def test_academic_topic_extraction(self):
        """Test academic topic extraction."""
        text = (
            "The methodology used in computational linguistics employs NLP techniques."
        )
        topics = self.handler._extract_academic_topics(text)

        self.assertIn("computational linguistics", topics)
        self.assertIn("research methodology", topics)

    def test_user_expertise_assessment(self):
        """Test user expertise assessment."""
        expert_profile = {
            "account_age_days": 2000,
            "public_repos": 50,
            "bio": "PhD in Computer Science",
        }
        expert_feedback = "The methodology lacks rigorous empirical validation."

        novice_profile = {"account_age_days": 30, "public_repos": 2, "bio": ""}
        novice_feedback = "Good paper!"

        expert_score = self.handler._assess_user_expertise(
            expert_profile, expert_feedback
        )
        novice_score = self.handler._assess_user_expertise(
            novice_profile, novice_feedback
        )

        self.assertGreater(expert_score, novice_score)

    def test_citation_extraction(self):
        """Test citation extraction."""
        research_text = """
        Studies by Johnson et al. (2023) show improvements.
        DOI 10.1234/example.2023.456 provides methodology details.
        """

        citations = self.handler._extract_citations(research_text)

        self.assertGreater(len(citations), 0)
        self.assertTrue(any("Johnson et al." in cite for cite in citations))
        self.assertTrue(any("10.1234/example.2023.456" in cite for cite in citations))

    def test_research_quality_assessment(self):
        """Test research quality assessment."""
        high_quality = [
            "Peer reviewed study with rigorous methodology and statistical evidence.",
            "Empirical validation with proper academic citations.",
        ]

        low_quality = [
            "Blog post with anecdotal evidence.",
            "Personal opinion without citations.",
        ]

        high_score = self.handler._assess_research_quality(high_quality)
        low_score = self.handler._assess_research_quality(low_quality)

        self.assertGreater(high_score, low_score)

    @patch("requests.get")
    def test_paper_content_fetching(self, mock_get):
        """Test paper content fetching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <html>
            <body>
                <article>
                    <h1>Research Paper</h1>
                    <p>Important academic content.</p>
                </article>
            </body>
        </html>
        """
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        content = self.handler.fetch_paper_content("https://example.com/paper")

        self.assertIn("Research Paper", content)
        self.assertIn("academic content", content)

    def test_snark_profile_generation(self):
        """Test snark profile generation."""
        context = ConversationContext(
            paper_url="",
            paper_title="Test Paper",
            paper_content="",
            line_number=None,
            conversation_history=[],
            user_profile={"login": "test"},
            research_context="",
        )

        research = ResearchAnalysis(
            research_quality_score=0.8,
            academic_references=[],
            key_insights=[],
            contradictory_evidence=[],
            research_gaps=[],
            methodological_concerns=[],
        )

        disagreeable_feedback = "This is wrong and I disagree completely."
        snark_profile = self.handler.generate_snark_profile(
            context, disagreeable_feedback, research
        )

        appreciative_feedback = "This is interesting and helpful, thank you!"
        nice_snark_profile = self.handler.generate_snark_profile(
            context, appreciative_feedback, research
        )

        self.assertGreater(snark_profile.snark_level, nice_snark_profile.snark_level)
        self.assertIsInstance(snark_profile.conversational_hooks, list)

    def test_emergency_response(self):
        """Test emergency response generation."""
        context = ConversationContext(
            paper_url="",
            paper_title="Emergency Test Paper",
            paper_content="",
            line_number=99,
            conversation_history=[],
            user_profile={"login": "test"},
            research_context="",
        )

        response = self.handler._emergency_contextual_response(context, "Test feedback")

        self.assertIn("Emergency Test Paper", response)
        self.assertIn("line 99", response)
        self.assertIn("?", response)  # Should ask a question

    @patch("subprocess.run")
    def test_rate_limit_check(self, mock_run):
        """Test rate limit checking."""
        # Mock GraphQL response indicating rate limit exceeded
        mock_response = {"data": {"search": {"issueCount": 6}}}
        mock_run.return_value.stdout = json.dumps(mock_response)
        mock_run.return_value.returncode = 0

        is_rate_limited = self.handler.check_rate_limit("prolific_user")
        self.assertTrue(is_rate_limited)

        # Mock response under limit
        mock_response["data"]["search"]["issueCount"] = 3
        mock_run.return_value.stdout = json.dumps(mock_response)

        is_rate_limited = self.handler.check_rate_limit("normal_user")
        self.assertFalse(is_rate_limited)


class TestWorkflowIntegration(unittest.TestCase):
    """Test workflow integration."""

    def setUp(self):
        """Set up test environment."""
        if not HANDLER_AVAILABLE:
            self.skipTest("Handler not available")

        # Create temporary event file
        self.temp_event = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        event_data = {
            "issue": {
                "number": 456,
                "title": 'Feedback on "Integration Test"',
                "body": "The methodology needs improvement. Line: 123",
                "user": {"login": "tester"},
                "labels": [{"name": "reader-feedback"}],
            }
        }
        json.dump(event_data, self.temp_event)
        self.temp_event.close()

        os.environ["GITHUB_EVENT_PATH"] = self.temp_event.name
        self.handler = ContextualDrBProp()

    def tearDown(self):
        """Clean up."""
        if os.path.exists(self.temp_event.name):
            os.unlink(self.temp_event.name)
        if "GITHUB_EVENT_PATH" in os.environ:
            del os.environ["GITHUB_EVENT_PATH"]

    def test_issue_data_extraction(self):
        """Test issue data extraction from GitHub event."""
        issue_data = self.handler._get_issue_data()

        self.assertEqual(issue_data["number"], 456)
        self.assertEqual(issue_data["user"]["login"], "tester")
        self.assertIn("Integration Test", issue_data["title"])

    @patch.object(ContextualDrBProp, "check_rate_limit")
    @patch.object(ContextualDrBProp, "detect_spam")
    def test_spam_detection_workflow(self, mock_detect_spam, mock_rate_limit):
        """Test spam detection workflow."""
        mock_rate_limit.return_value = False
        mock_detect_spam.return_value = (False, 3)

        results = self.handler.run_spam_detection()

        self.assertTrue(results["should_respond"])
        self.assertFalse(results["user_rate_limited"])
        self.assertEqual(results["spam_score"], 3)


def run_basic_tests():
    """Run basic tests and report results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTest(loader.loadTestsFromTestCase(TestBasicFunctionality))
    suite.addTest(loader.loadTestsFromTestCase(TestWorkflowIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'='*60}")
    print("BASIC TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print(f"\nFAILURES:")
        for test, error in result.failures:
            print(f"- {test}")

    if result.errors:
        print(f"\nERRORS:")
        for test, error in result.errors:
            print(f"- {test}")

    success_rate = (
        (result.testsRun - len(result.failures) - len(result.errors))
        / result.testsRun
        * 100
    )
    print(f"\nSUCCESS RATE: {success_rate:.1f}%")

    return result.wasSuccessful()


if __name__ == "__main__":
    if not HANDLER_AVAILABLE:
        print("ERROR: Handler not available for testing")
        sys.exit(1)

    success = run_basic_tests()
    sys.exit(0 if success else 1)
