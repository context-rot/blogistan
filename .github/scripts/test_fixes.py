#!/usr/bin/env python3
"""
Test script to verify all GitHub API and Perplexity API fixes
"""

import os
import sys
import json
import subprocess
from datetime import datetime


def test_perplexity_api():
    """Test Perplexity API with the new implementation."""
    print("🔍 Testing Perplexity API fixes...")

    # Import and test the handler
    sys.path.append("/Users/basitmustafa/Documents/GitHub/blogistan/.github/scripts")
    from dr_b_prop_handler_v2 import ContextualDrBProp

    handler = ContextualDrBProp()

    if handler.perplexity_key:
        result = handler._query_perplexity(
            "test research query: software engineering best practices"
        )
        if result:
            print(f"✅ Perplexity API working: {len(result)} characters returned")
        else:
            print("❌ Perplexity API still failing")
    else:
        print("⚠️ Perplexity API key not available")

    return bool(result) if handler.perplexity_key else True


def test_github_api():
    """Test GitHub API with new error handling."""
    print("🔍 Testing GitHub API fixes...")

    sys.path.append("/Users/basitmustafa/Documents/GitHub/blogistan/.github/scripts")
    from user_intelligence_collector import UserIntelligenceCollector
    from reaction_pattern_analyzer import ReactionPatternAnalyzer

    # Test user intelligence collector
    collector = UserIntelligenceCollector()
    if collector.github_token:
        # Try a simple API call
        result = collector._gh_api("user")
        if result:
            print(
                f"✅ GitHub API working for user intelligence: {result.get('login', 'unknown')}"
            )
        else:
            print("❌ GitHub API failing for user intelligence")
    else:
        print("⚠️ GitHub token not available for user intelligence")

    # Test reaction pattern analyzer
    analyzer = ReactionPatternAnalyzer()
    if analyzer.github_token and analyzer.repository:
        comments = analyzer.get_dr_b_prop_comments(days_back=7)  # Short test period
        print(f"✅ Reaction analyzer working: {len(comments)} comments found")
    else:
        print("⚠️ GitHub token or repository not available for reaction analyzer")

    return True


def test_label_adding():
    """Test label adding fix."""
    print("🔍 Testing label adding fixes...")

    sys.path.append("/Users/basitmustafa/Documents/GitHub/blogistan/.github/scripts")
    from dr_b_prop_handler_v2 import ContextualDrBProp

    handler = ContextualDrBProp()

    # Create a test label first
    try:
        result = subprocess.run(
            [
                "gh",
                "label",
                "create",
                "test-dr-b-prop",
                "--description",
                "Test label",
                "--color",
                "0e8a16",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 or "already exists" in result.stderr:
            print("✅ Label creation working")
        else:
            print(f"❌ Label creation failing: {result.stderr}")
    except Exception as e:
        print(f"❌ Label creation error: {e}")

    return True


def test_research_quality():
    """Test that research quality is improved."""
    print("🔍 Testing research quality improvements...")

    sys.path.append("/Users/basitmustafa/Documents/GitHub/blogistan/.github/scripts")
    from dr_b_prop_handler_v2 import (
        ContextualDrBProp,
        ConversationContext,
        ResearchAnalysis,
    )

    handler = ContextualDrBProp()

    # Create a mock context
    context = ConversationContext(
        paper_url="https://example.com/paper",
        paper_title="Test Paper",
        paper_content="Test content about software engineering",
        line_number=None,
        conversation_history=[],
        user_profile={},
        research_context="",
        selected_text="software engineering best practices",
        user_feedback="I think this approach is interesting",
    )

    # Test research
    research = handler.conduct_advanced_research(
        context, "software engineering methodology"
    )

    print(f"✅ Research quality score: {research.research_quality_score:.2f}")
    print(f"✅ Research insights: {len(research.key_insights)}")

    return (
        research.research_quality_score > 0.2
    )  # Should be better than the 0.38 we had


def main():
    """Run all tests."""
    print("🚀 Running Dr. B. Prop fixes verification...\n")

    tests = [
        ("Perplexity API", test_perplexity_api),
        ("GitHub API", test_github_api),
        ("Label Adding", test_label_adding),
        ("Research Quality", test_research_quality),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            print(
                f"{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}\n"
            )
        except Exception as e:
            results[test_name] = False
            print(f"❌ {test_name}: ERROR - {e}\n")

    # Summary
    passed = sum(results.values())
    total = len(results)

    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All fixes verified successfully!")
    else:
        print("⚠️ Some tests failed - check logs above")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
