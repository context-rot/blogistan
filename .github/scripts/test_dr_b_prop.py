#!/usr/bin/env python3
"""
Comprehensive Test Suite for Dr. B. Prop Handler v2.0

Tests all functionality including:
- Spam detection and rate limiting
- Context extraction and paper fetching
- Research capabilities and API integrations
- DSPy integration and fallback mechanisms
- Response generation and conversation hooks
- Error handling and edge cases
"""

import os
import sys
import json
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
from datetime import datetime, timedelta

# Add the scripts directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the handler
from dr_b_prop_handler_v2 import (
    ContextualDrBProp,
    ConversationContext,
    ResearchAnalysis,
    SnarkProfile,
    AdvancedResearchAgent,
)


class TestSpamDetection(unittest.TestCase):
    """Test spam detection functionality."""

    def setUp(self):
        """Set up test environment."""
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["GITHUB_REPOSITORY"] = "test/repo"
        self.handler = ContextualDrBProp()

        # Mock issue data
        self.handler.issue_data = {
            "number": 123,
            "title": "Test Issue",
            "body": "Test feedback about the paper.",
            "user": {"login": "test_user"},
            "labels": [{"name": "reader-feedback"}],
        }

    def test_legitimate_feedback_detection(self):
        """Test that legitimate academic feedback passes spam detection."""
        title = "Feedback on methodology in computational linguistics paper"
        body = """I found the methodology section particularly insightful. 
        However, I have some concerns about the empirical validation approach.
        The theoretical framework seems sound but could benefit from more rigorous peer review."""

        is_spam, score = self.handler.detect_spam(title, body, "academic_user")

        self.assertFalse(
            is_spam, "Legitimate academic feedback should not be flagged as spam"
        )
        self.assertLess(
            score, 8, "Spam score should be below threshold for academic content"
        )

    def test_obvious_spam_detection(self):
        """Test that obvious spam is detected."""
        title = "Make Money Fast!!!"
        body = """URGENT!!! Make $5000 a day working from home!!! 
        Bitcoin investment opportunity!!! GUARANTEED RETURNS!!!
        Call 1-800-SCAM-NOW or email scammer@fake.com"""

        is_spam, score = self.handler.detect_spam(title, body, "spammer")

        self.assertTrue(is_spam, "Obvious spam should be detected")
        self.assertGreaterEqual(score, 8, "Spam score should be above threshold")

    def test_academic_content_spam_reduction(self):
        """Test that academic indicators reduce spam score."""
        title = "Research methodology question"
        body = """I have a methodology question about your empirical study. 
        The research approach seems novel but I'm wondering about the 
        statistical validation methods used in the analysis."""

        # Mock the issue having reader-feedback label
        self.handler.issue_data["labels"] = [{"name": "reader-feedback"}]

        is_spam, score = self.handler.detect_spam(title, body, "researcher")

        self.assertFalse(is_spam, "Academic content should get spam score reduction")
        self.assertLess(
            score, 5, "Academic indicators should significantly reduce spam score"
        )

    def test_short_content_penalty(self):
        """Test that very short content gets penalized."""
        title = "hmm"
        body = "ok"

        is_spam, score = self.handler.detect_spam(title, body, "lazy_user")

        self.assertGreater(score, 2, "Short content should increase spam score")

    def test_excessive_repetition_detection(self):
        """Test detection of excessive repetition."""
        title = "Normal title"
        body = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa" * 10  # Excessive repetition

        is_spam, score = self.handler.detect_spam(title, body, "repetitive_user")

        self.assertGreater(score, 2, "Excessive repetition should increase spam score")

    @patch("subprocess.run")
    def test_rate_limit_check(self, mock_run):
        """Test rate limiting functionality."""
        # Mock successful GraphQL response
        mock_response = {"data": {"search": {"issueCount": 6}}}  # Above the limit of 5
        mock_run.return_value.stdout = json.dumps(mock_response)
        mock_run.return_value.returncode = 0

        is_rate_limited = self.handler.check_rate_limit("prolific_user")

        self.assertTrue(
            is_rate_limited, "User with 6 recent issues should be rate limited"
        )

        # Test user under limit
        mock_response["data"]["search"]["issueCount"] = 3
        mock_run.return_value.stdout = json.dumps(mock_response)

        is_rate_limited = self.handler.check_rate_limit("normal_user")

        self.assertFalse(
            is_rate_limited, "User with 3 recent issues should not be rate limited"
        )


class TestContextExtraction(unittest.TestCase):
    """Test conversation context extraction."""

    def setUp(self):
        """Set up test environment."""
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["GITHUB_REPOSITORY"] = "test/repo"
        self.handler = ContextualDrBProp()

        self.handler.issue_data = {"number": 123, "user": {"login": "test_user"}}

    def test_paper_url_extraction(self):
        """Test extraction of paper URL from issue body."""
        title = 'Feedback on "Test Paper Title"'
        body = """## My Feedback
        Great paper! Found it at https://context-rot.com/papers/test-paper.html
        
        ## Context
        - Line: 42"""

        context = self.handler.extract_conversation_context(title, body)

        self.assertEqual(
            context.paper_url, "https://context-rot.com/papers/test-paper.html"
        )
        self.assertEqual(context.paper_title, "Test Paper Title")
        self.assertEqual(context.line_number, 42)

    def test_line_number_extraction(self):
        """Test extraction of line numbers in various formats."""
        test_cases = [
            ("Line 42", 42),
            ("line: 123", 123),
            ("Line: 999", 999),
            ("around line 55", 55),
            ("no line number here", None),
        ]

        for body_text, expected_line in test_cases:
            with self.subTest(body=body_text):
                context = self.handler.extract_conversation_context("Test", body_text)
                self.assertEqual(context.line_number, expected_line)

    @patch("requests.get")
    def test_paper_content_fetching(self, mock_get):
        """Test fetching paper content from URL."""
        # Mock successful HTTP response with HTML content
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <html>
            <head><title>Test Paper</title></head>
            <body>
                <article>
                    <h1>Research Paper Title</h1>
                    <p>This is the main content of the research paper.</p>
                    <p>It contains important academic insights.</p>
                </article>
                <script>alert('remove me')</script>
            </body>
        </html>
        """
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        content = self.handler.fetch_paper_content("https://example.com/paper")

        self.assertIn("Research Paper Title", content)
        self.assertIn("academic insights", content)
        self.assertNotIn("alert", content)  # Script should be removed
        mock_get.assert_called_once()

    @patch("requests.get")
    def test_paper_content_fetch_error_handling(self, mock_get):
        """Test error handling when fetching paper content fails."""
        mock_get.side_effect = Exception("Network error")

        content = self.handler.fetch_paper_content("https://example.com/paper")

        self.assertEqual(content, "")

    @patch.object(ContextualDrBProp, "_gh_api")
    def test_conversation_history_retrieval(self, mock_gh_api):
        """Test retrieval of conversation history."""
        # Mock GitHub API response with comments
        mock_comments = [
            {
                "user": {"login": "user1"},
                "body": "First comment about the methodology.",
                "created_at": "2023-01-01T12:00:00Z",
            },
            {
                "user": {"login": "dr-b-prop-bot"},
                "body": "**Dr. B. Prop responds:** Thank you for your insightful feedback...",
                "created_at": "2023-01-01T13:00:00Z",
            },
            {
                "user": {"login": "user1"},
                "body": "Thanks for the detailed response!",
                "created_at": "2023-01-01T14:00:00Z",
            },
        ]
        mock_gh_api.return_value = mock_comments

        history = self.handler.get_conversation_history()

        self.assertEqual(len(history), 3)
        self.assertTrue(
            history[1]["is_dr_b_prop"]
        )  # Second comment is from Dr. B. Prop
        self.assertFalse(history[0]["is_dr_b_prop"])  # First comment is not

    @patch.object(ContextualDrBProp, "_gh_api")
    def test_user_profile_retrieval(self, mock_gh_api):
        """Test user profile retrieval and analysis."""
        # Mock GitHub API response for user data
        mock_user_data = {
            "login": "test_user",
            "created_at": "2020-01-01T00:00:00Z",
            "public_repos": 25,
            "followers": 50,
            "bio": "PhD in Computer Science, interested in NLP research",
        }
        mock_gh_api.return_value = mock_user_data

        profile = self.handler.get_user_profile()

        self.assertEqual(profile["login"], "test_user")
        self.assertGreater(profile["account_age_days"], 1000)  # Account is old
        self.assertEqual(profile["public_repos"], 25)
        self.assertIn("PhD", profile["bio"])


class TestResearchCapabilities(unittest.TestCase):
    """Test research and analysis capabilities."""

    def setUp(self):
        """Set up test environment."""
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["PPLX_API_KEY"] = "test_pplx_key"
        self.handler = ContextualDrBProp()

    def test_academic_topic_extraction(self):
        """Test extraction of academic topics from text."""
        text = "The methodology used in this computational linguistics study employs advanced NLP techniques."

        topics = self.handler._extract_academic_topics(text)

        self.assertIn("computational linguistics", topics)
        self.assertIn("research methodology", topics)

    def test_research_query_generation(self):
        """Test generation of targeted research queries."""
        context = ConversationContext(
            paper_url="https://example.com/paper",
            paper_title="Advanced NLP Methodology for Software Engineering",
            paper_content="This paper explores computational linguistics approaches...",
            line_number=42,
            conversation_history=[],
            user_profile={"login": "test_user"},
            research_context="",
        )

        user_feedback = (
            "I have concerns about the methodology and empirical validation approach."
        )

        queries = self.handler._generate_research_queries(context, user_feedback)

        self.assertGreater(len(queries), 0)
        self.assertTrue(any("methodology" in query.lower() for query in queries))
        self.assertTrue(any("Advanced NLP" in query for query in queries))

    @patch("requests.post")
    def test_perplexity_api_integration(self, mock_post):
        """Test Perplexity API integration."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Recent research in computational linguistics shows significant advances in methodology. Studies by Smith et al. (2023) demonstrate improved empirical validation techniques."
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        result = self.handler._query_perplexity(
            "research methodology computational linguistics"
        )

        self.assertIn("computational linguistics", result)
        self.assertIn("Smith et al.", result)
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_perplexity_api_error_handling(self, mock_post):
        """Test error handling for Perplexity API failures."""
        mock_post.side_effect = Exception("API error")

        result = self.handler._query_perplexity("test query")

        self.assertEqual(result, "")

    def test_citation_extraction(self):
        """Test extraction of academic citations from research text."""
        research_text = """
        Recent studies by Johnson et al. (2023) and Williams et al. (2022) have shown 
        significant improvements. The DOI 10.1234/example.2023.456 provides detailed methodology.
        Another study with DOI 10.5678/research.2022.789 confirms these findings.
        """

        citations = self.handler._extract_citations(research_text)

        self.assertGreater(len(citations), 0)
        self.assertTrue(any("Johnson et al." in cite for cite in citations))
        self.assertTrue(any("10.1234/example.2023.456" in cite for cite in citations))

    def test_research_quality_assessment(self):
        """Test assessment of research quality."""
        high_quality_results = [
            "This peer reviewed study employs rigorous methodology with statistical evidence from academic journals.",
            "The empirical validation demonstrates significant findings with proper citations and academic rigor.",
        ]

        low_quality_results = [
            "Some guy on a blog said this might work.",
            "Anecdotal evidence suggests possible benefits.",
        ]

        high_score = self.handler._assess_research_quality(high_quality_results)
        low_score = self.handler._assess_research_quality(low_quality_results)

        self.assertGreater(high_score, low_score)
        self.assertGreater(high_score, 0.5)
        self.assertLess(low_score, 0.3)

    def test_insight_extraction(self):
        """Test extraction of key insights from research."""
        research_results = [
            "The study found that advanced NLP techniques improve accuracy by 25%.",
            "Research demonstrates significant benefits in computational linguistics applications.",
            "Other unrelated content that doesn't show findings.",
        ]

        insights = self.handler._extract_insights(research_results)

        self.assertGreater(len(insights), 0)
        self.assertTrue(any("found" in insight.lower() for insight in insights))
        self.assertTrue(any("demonstrates" in insight.lower() for insight in insights))

    def test_contradiction_detection(self):
        """Test detection of contradictory evidence."""
        research_results = [
            "The methodology works well. However, some studies dispute these findings.",
            "There are conflicting reports about the effectiveness of this approach.",
            "Standard research with no contradictions mentioned.",
        ]

        contradictions = self.handler._find_contradictions(research_results)

        self.assertGreater(len(contradictions), 0)
        self.assertTrue(
            any(
                "however" in contra.lower() or "conflicting" in contra.lower()
                for contra in contradictions
            )
        )


class TestSnarkAndPersonality(unittest.TestCase):
    """Test snark profile generation and personality features."""

    def setUp(self):
        """Set up test environment."""
        os.environ["GITHUB_TOKEN"] = "test_token"
        self.handler = ContextualDrBProp()

    def test_user_expertise_assessment(self):
        """Test assessment of user expertise level."""
        # Expert user profile
        expert_profile = {
            "login": "expert_user",
            "account_age_days": 2000,
            "public_repos": 50,
            "bio": "PhD in Computer Science",
        }
        expert_feedback = "The methodology lacks rigorous empirical validation and statistical significance testing."

        # Novice user profile
        novice_profile = {
            "login": "new_user",
            "account_age_days": 30,
            "public_repos": 2,
            "bio": "",
        }
        novice_feedback = "Good paper!"

        expert_score = self.handler._assess_user_expertise(
            expert_profile, expert_feedback
        )
        novice_score = self.handler._assess_user_expertise(
            novice_profile, novice_feedback
        )

        self.assertGreater(expert_score, novice_score)
        self.assertGreater(expert_score, 0.5)
        self.assertLess(novice_score, 0.3)

    def test_snark_level_adjustment(self):
        """Test snark level adjustment based on feedback tone."""
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

        # Disagreeable feedback should increase snark
        disagreeable_feedback = (
            "This is completely wrong and I disagree with the methodology."
        )
        snark_profile = self.handler.generate_snark_profile(
            context, disagreeable_feedback, research
        )

        # Appreciative feedback should decrease snark
        appreciative_feedback = "This is really interesting and helpful, thank you!"
        nice_snark_profile = self.handler.generate_snark_profile(
            context, appreciative_feedback, research
        )

        self.assertGreater(snark_profile.snark_level, nice_snark_profile.snark_level)

    def test_contextual_hooks_generation(self):
        """Test generation of contextual conversation hooks."""
        context = ConversationContext(
            paper_url="https://example.com/paper",
            paper_title="Advanced Computational Linguistics Methods",
            paper_content="Research methodology details...",
            line_number=42,
            conversation_history=[],
            user_profile={"login": "test_user"},
            research_context="",
        )

        research = ResearchAnalysis(
            research_quality_score=0.7,
            academic_references=["Smith et al. (2023)", "DOI: 10.1234/example"],
            key_insights=[],
            contradictory_evidence=[],
            research_gaps=[],
            methodological_concerns=[],
        )

        user_feedback = "I have concerns about the methodology used in this study."

        hooks = self.handler._generate_contextual_hooks(
            context, user_feedback, research
        )

        self.assertGreater(len(hooks), 0)
        # Should include paper-specific hook
        self.assertTrue(any("Advanced Computational" in hook for hook in hooks))
        # Should include line-specific hook
        self.assertTrue(any("line 42" in hook for hook in hooks))
        # Should include methodology hook
        self.assertTrue(any("methodological" in hook.lower() for hook in hooks))


class TestResponseGeneration(unittest.TestCase):
    """Test response generation and integration."""

    def setUp(self):
        """Set up test environment."""
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["GITHUB_REPOSITORY"] = "test/repo"
        self.handler = ContextualDrBProp()

        self.handler.issue_data = {
            "number": 123,
            "title": "Test Issue",
            "body": "Test feedback",
            "user": {"login": "test_user"},
        }

    def test_conversation_context_summarization(self):
        """Test summarization of conversation context for DSPy."""
        context = ConversationContext(
            paper_url="https://example.com/paper",
            paper_title="Test Paper Title",
            paper_content="Paper content here...",
            line_number=42,
            conversation_history=[
                {"author": "user1", "body": "First comment", "is_dr_b_prop": False},
                {
                    "author": "dr-b-prop",
                    "body": "Response comment",
                    "is_dr_b_prop": True,
                },
            ],
            user_profile={"login": "test_user", "account_age_days": 500},
            research_context="",
        )

        summary = self.handler._summarize_conversation_context(context)

        self.assertIn("Test Paper Title", summary)
        self.assertIn("line 42", summary)
        self.assertIn("test_user", summary)
        self.assertIn("500 days", summary)
        self.assertIn("Previous conversation", summary)

    def test_research_summarization(self):
        """Test summarization of research findings."""
        research = ResearchAnalysis(
            research_quality_score=0.85,
            academic_references=["Smith et al. (2023)", "DOI: 10.1234/example"],
            key_insights=[
                "Machine learning improves accuracy",
                "Statistical significance confirmed",
            ],
            contradictory_evidence=["However, some studies dispute this"],
            research_gaps=["Limited longitudinal studies"],
            methodological_concerns=["Small sample size identified"],
        )

        summary = self.handler._summarize_research(research)

        self.assertIn("0.85", summary)
        self.assertIn("Smith et al.", summary)
        self.assertIn("Machine learning", summary)
        self.assertIn("Small sample", summary)

    @patch("subprocess.run")
    def test_fallback_response_generation(self, mock_run):
        """Test fallback response generation using vibe-tools."""
        # Mock successful vibe-tools response
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = """
        Thank you for your sophisticated feedback on our research methodology. 
        Your observations regarding the empirical validation approach demonstrate 
        considerable insight into the epistemological foundations of our work.
        
        The methodological implications you've raised warrant further investigation 
        within the broader theoretical framework of computational linguistics research.
        
        What's your perspective on the statistical significance testing we employed?
        """

        context = ConversationContext(
            paper_url="https://example.com/paper",
            paper_title="Advanced NLP Research",
            paper_content="Research content...",
            line_number=25,
            conversation_history=[],
            user_profile={"login": "expert_user"},
            research_context="",
        )

        research = ResearchAnalysis(
            research_quality_score=0.7,
            academic_references=["Smith et al. (2023)"],
            key_insights=["NLP advances"],
            contradictory_evidence=[],
            research_gaps=[],
            methodological_concerns=[],
        )

        snark_profile = SnarkProfile(
            snark_level=0.6,
            academic_pretension=0.8,
            methodological_criticism=0.7,
            intellectual_superiority=0.75,
            conversational_hooks=["What are your thoughts on the methodology?"],
        )

        response = self.handler._fallback_contextual_response(
            context, "Test feedback", research, snark_profile
        )

        self.assertIn("methodology", response.lower())
        self.assertIn("epistemological", response.lower())
        mock_run.assert_called_once()

    def test_emergency_response_generation(self):
        """Test emergency response generation."""
        context = ConversationContext(
            paper_url="https://example.com/paper",
            paper_title="Emergency Test Paper",
            paper_content="",
            line_number=99,
            conversation_history=[],
            user_profile={"login": "test_user"},
            research_context="",
        )

        response = self.handler._emergency_contextual_response(context, "Test feedback")

        self.assertIn("Emergency Test Paper", response)
        self.assertIn("line 99", response)
        self.assertIn("methodological", response.lower())
        self.assertIn("?", response)  # Should end with a question


class TestIntegrationAndWorkflow(unittest.TestCase):
    """Test full integration and workflow functionality."""

    def setUp(self):
        """Set up test environment."""
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["GITHUB_REPOSITORY"] = "test/repo"

        # Create temporary event file
        self.temp_event = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        event_data = {
            "issue": {
                "number": 456,
                "title": 'Feedback on "Integration Test Paper"',
                "body": """## My Feedback
                The methodology section needs improvement.
                
                ## Context
                - Paper: Integration Test Paper
                - URL: https://example.com/integration-test
                - Line: 123""",
                "user": {"login": "integration_tester"},
                "labels": [{"name": "reader-feedback"}],
            }
        }
        json.dump(event_data, self.temp_event)
        self.temp_event.close()

        os.environ["GITHUB_EVENT_PATH"] = self.temp_event.name

        self.handler = ContextualDrBProp()

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_event.name):
            os.unlink(self.temp_event.name)
        if "GITHUB_EVENT_PATH" in os.environ:
            del os.environ["GITHUB_EVENT_PATH"]

    def test_issue_data_extraction_from_event(self):
        """Test extraction of issue data from GitHub event."""
        issue_data = self.handler._get_issue_data()

        self.assertEqual(issue_data["number"], 456)
        self.assertEqual(issue_data["user"]["login"], "integration_tester")
        self.assertIn("Integration Test Paper", issue_data["title"])
        self.assertIn("methodology", issue_data["body"])

    @patch.object(ContextualDrBProp, "check_rate_limit")
    @patch.object(ContextualDrBProp, "detect_spam")
    def test_spam_detection_workflow(self, mock_detect_spam, mock_rate_limit):
        """Test complete spam detection workflow."""
        # Mock successful spam detection
        mock_rate_limit.return_value = False
        mock_detect_spam.return_value = (False, 3)  # Not spam, low score

        results = self.handler.run_spam_detection()

        self.assertTrue(results["should_respond"])
        self.assertFalse(results["user_rate_limited"])
        self.assertEqual(results["spam_score"], 3)

        # Test rate limiting
        mock_rate_limit.return_value = True

        results = self.handler.run_spam_detection()

        self.assertFalse(results["should_respond"])
        self.assertTrue(results["user_rate_limited"])

        # Test spam detection
        mock_rate_limit.return_value = False
        mock_detect_spam.return_value = (True, 10)  # Is spam, high score

        results = self.handler.run_spam_detection()

        self.assertFalse(results["should_respond"])
        self.assertFalse(results["user_rate_limited"])
        self.assertEqual(results["spam_score"], 10)

    @patch.object(ContextualDrBProp, "post_enhanced_comment")
    @patch.object(ContextualDrBProp, "add_label")
    @patch.object(ContextualDrBProp, "craft_enhanced_response")
    @patch.object(ContextualDrBProp, "conduct_advanced_research")
    @patch.object(ContextualDrBProp, "extract_conversation_context")
    def test_response_generation_workflow(
        self,
        mock_extract_context,
        mock_research,
        mock_craft_response,
        mock_add_label,
        mock_post_comment,
    ):
        """Test complete response generation workflow."""
        # Mock all the components
        mock_context = ConversationContext(
            paper_url="https://example.com/test-paper",
            paper_title="Integration Test Paper",
            paper_content="Test paper content...",
            line_number=123,
            conversation_history=[],
            user_profile={"login": "integration_tester"},
            research_context="",
        )
        mock_extract_context.return_value = mock_context

        mock_research_result = ResearchAnalysis(
            research_quality_score=0.8,
            academic_references=["Test et al. (2023)"],
            key_insights=["Test insight"],
            contradictory_evidence=[],
            research_gaps=[],
            methodological_concerns=[],
        )
        mock_research.return_value = mock_research_result

        mock_craft_response.return_value = "Test response with academic pretension."
        mock_post_comment.return_value = True
        mock_add_label.return_value = True

        success = self.handler.run_contextual_response_generation()

        self.assertTrue(success)
        mock_extract_context.assert_called_once()
        mock_research.assert_called_once()
        mock_craft_response.assert_called_once()
        mock_post_comment.assert_called_once()
        mock_add_label.assert_called_once()

    def test_error_handling_in_response_generation(self):
        """Test error handling in response generation workflow."""
        # Create handler with no issue data
        self.handler.issue_data = None

        success = self.handler.run_contextual_response_generation()

        self.assertFalse(success, "Should return False when no issue data available")


class TestErrorHandlingAndEdgeCases(unittest.TestCase):
    """Test error handling and edge cases."""

    def setUp(self):
        """Set up test environment."""
        os.environ["GITHUB_TOKEN"] = "test_token"
        self.handler = ContextualDrBProp()

    def test_missing_environment_variables(self):
        """Test handling of missing environment variables."""
        # Remove API keys
        if "PPLX_API_KEY" in os.environ:
            del os.environ["PPLX_API_KEY"]
        if "PERPLEXITY_API_KEY" in os.environ:
            del os.environ["PERPLEXITY_API_KEY"]

        handler = ContextualDrBProp()

        self.assertIsNone(handler.perplexity_key)

        # Research should still work without Perplexity
        context = ConversationContext(
            paper_url="",
            paper_title="Test",
            paper_content="",
            line_number=None,
            conversation_history=[],
            user_profile={},
            research_context="",
        )

        research = handler.conduct_advanced_research(context, "test feedback")

        self.assertIsInstance(research, ResearchAnalysis)

    def test_malformed_issue_data(self):
        """Test handling of malformed issue data."""
        # Test with missing fields
        malformed_data = {
            "number": 123,
            # Missing title, body, user
        }

        self.handler.issue_data = malformed_data

        # Should not crash
        results = self.handler.run_spam_detection()

        self.assertIn("should_respond", results)
        self.assertIn("user_rate_limited", results)

    @patch("requests.get")
    def test_network_error_handling(self, mock_get):
        """Test handling of network errors."""
        mock_get.side_effect = Exception("Network timeout")

        content = self.handler.fetch_paper_content("https://example.com/paper")

        self.assertEqual(content, "")

    def test_empty_research_results(self):
        """Test handling of empty research results."""
        empty_research = ResearchAnalysis(
            research_quality_score=0.0,
            academic_references=[],
            key_insights=[],
            contradictory_evidence=[],
            research_gaps=[],
            methodological_concerns=[],
        )

        # Should not crash when generating response
        context = ConversationContext(
            paper_url="",
            paper_title="",
            paper_content="",
            line_number=None,
            conversation_history=[],
            user_profile={},
            research_context="",
        )

        snark_profile = self.handler.generate_snark_profile(
            context, "test", empty_research
        )

        self.assertIsInstance(snark_profile, SnarkProfile)
        self.assertGreaterEqual(snark_profile.snark_level, 0.0)
        self.assertLessEqual(snark_profile.snark_level, 1.0)


def run_all_tests():
    """Run all tests and provide detailed output."""
    test_suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestSpamDetection,
        TestContextExtraction,
        TestResearchCapabilities,
        TestSnarkAndPersonality,
        TestResponseGeneration,
        TestIntegrationAndWorkflow,
        TestErrorHandlingAndEdgeCases,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%"
    )

    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split(chr(10))[-2]}")

    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split(chr(10))[-2]}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
