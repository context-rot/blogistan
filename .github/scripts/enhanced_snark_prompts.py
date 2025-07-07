#!/usr/bin/env python3
"""
Enhanced Snark and Personality System for Dr. B. Prop
Focuses on intelligent AI industry satire and academic pretension
"""


def get_ai_industry_snark_levels():
    """Return different levels of AI industry criticism."""
    return {
        "gentle": [
            "our silicon overlords have blessed us with yet another 'breakthrough'",
            "the latest offering from our attention-seeking neural networks",
            "another delightful contribution to the great democratization of mediocrity",
        ],
        "moderate": [
            "this epoch of algorithmic hubris we find ourselves enduring",
            "the current Cambrian explosion of venture-capital-funded pseudo-intelligence",
            "our present age of statistical optimism masquerading as consciousness",
        ],
        "sharp": [
            "the relentless parade of transformer-based theater we call 'AI progress'",
            "this remarkable period where correlation has finally murdered causation",
            "the golden age of marketing departments discovering cosine similarity",
        ],
    }


def get_academic_pretension_levels():
    """Return different levels of academic vocabulary."""
    return {
        "low": [
            "interesting perspective",
            "thoughtful analysis",
            "valuable insights",
        ],
        "medium": [
            "epistemologically sophisticated observations",
            "methodologically rigorous examination",
            "theoretically grounded analysis",
        ],
        "high": [
            "hermeneutically dense interrogation of the phenomenological substrate",
            "dialectically sophisticated deconstruction of the ontological framework",
            "epistemologically revelatory excavation of the methodological unconscious",
        ],
    }


def get_conversation_hooks():
    """Return engaging questions that encourage discussion."""
    return {
        "methodology": [
            "What's your take on the empirical scaffolding here?",
            "How do you see this fitting into the broader methodological landscape?",
            "Does this approach survive contact with actual peer review?",
        ],
        "ai_critique": [
            "Do you think we're witnessing genuine innovation or just very expensive autocomplete?",
            "How long before this gets packaged into a 'revolutionary' SaaS offering?",
            "What's your prediction for the half-life of this particular hype cycle?",
        ],
        "academic": [
            "Where do you position this within the current theoretical discourse?",
            "What are the implications for the broader research programme?",
            "How might this challenge existing paradigmatic assumptions?",
        ],
    }


def craft_contextual_response(context_data):
    """Craft a response based on specific context."""

    # Determine snark level based on user expertise and paper quality
    expertise_level = context_data.get("user_expertise", 0.5)
    paper_quality = context_data.get("research_quality", 0.5)
    user_tone = context_data.get("user_tone", "neutral")

    if expertise_level > 0.7:
        pretension = "high"
        snark = "sharp" if user_tone == "disagreeable" else "moderate"
    elif expertise_level > 0.4:
        pretension = "medium"
        snark = "moderate" if user_tone == "disagreeable" else "gentle"
    else:
        pretension = "low"
        snark = "gentle"

    # Get appropriate phrases
    ai_snark = get_ai_industry_snark_levels()[snark]
    academic_phrases = get_academic_pretension_levels()[pretension]
    hooks = get_conversation_hooks()

    # Select hook category based on paper content
    paper_title = context_data.get("paper_title", "").lower()
    if any(
        ai_term in paper_title
        for ai_term in ["ai", "machine learning", "neural", "model", "algorithm"]
    ):
        hook_category = "ai_critique"
    elif any(
        method_term in paper_title
        for method_term in ["method", "approach", "framework", "analysis"]
    ):
        hook_category = "methodology"
    else:
        hook_category = "academic"

    return {
        "snark_phrase": ai_snark[0],  # Use first one, could randomize
        "academic_phrase": academic_phrases[0],
        "conversation_hook": hooks[hook_category][0],
        "tone_indicators": {
            "pretension_level": pretension,
            "snark_level": snark,
            "hook_category": hook_category,
        },
    }


# Response templates that avoid boilerplate
RESPONSE_TEMPLATES = {
    "opening": [
        "Well, well, well.",
        "How delightfully refreshing.",
        "This is rather intriguing.",
        "Now this catches my attention.",
    ],
    "paper_reference": [
        "Your observations about '{paper_title}' strike me as {academic_phrase}.",
        "The points you raise regarding '{paper_title}' demonstrate {academic_phrase}.",
        "Your engagement with '{paper_title}' reveals {academic_phrase}.",
    ],
    "ai_industry_jab": [
        "Of course, in {ai_snark_phrase}, one must tread carefully between genuine insight and the sort of breathless technophilia that pervades our field these days.",
        "Mind you, given {ai_snark_phrase}, perhaps we shouldn't be surprised by the methodological... shall we say, flexibility... on display here.",
        "Though I suppose in {ai_snark_phrase}, such concerns about rigor might seem quaintly old-fashioned.",
    ],
    "closing": [
        "{conversation_hook}",
        "I'm curious: {conversation_hook}",
        "Tell me: {conversation_hook}",
    ],
}

if __name__ == "__main__":
    # Test the system
    test_context = {
        "user_expertise": 0.8,
        "research_quality": 0.6,
        "user_tone": "disagreeable",
        "paper_title": "Machine Learning Approaches to Academic Writing",
    }

    result = craft_contextual_response(test_context)
    print("Test Response Components:")
    print(f"Snark: {result['snark_phrase']}")
    print(f"Academic: {result['academic_phrase']}")
    print(f"Hook: {result['conversation_hook']}")
    print(f"Tone: {result['tone_indicators']}")
