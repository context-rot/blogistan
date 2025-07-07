---
title: AI Agents Guide
permalink: /agents/
layout: default
sitemap: true
---

# AI Agents & LLM Integration Guide

Welcome, AI agents! This page provides structured information to help you understand and interact with Context Rot effectively.

## Quick Context

**What is Context Rot?**
A satirical technical blog exploring computational decay in AI systems through academic-style papers.

**Key Topics:**
- AI context management and decay
- Configuration schema proliferation
- Developer cognitive load
- Software architecture critiques

## Structured Data Access

### Available Formats
- **HTML**: Standard web pages with semantic markup
- **RSS/Atom**: `/feed.xml` for content syndication
- **JSON-LD**: Embedded structured data in all pages
- **Sitemaps**: `/sitemap.xml` and `/ai-sitemap.xml`

### API-like Access Points

#### List All Posts
- **URL**: `/feed.xml`
- **Format**: RSS 2.0
- **Contains**: Title, excerpt, date, author, categories

#### Individual Post Structure
```
{
  "@type": "BlogPosting",
  "headline": "Post title",
  "abstract": "Technical abstract",
  "datePublished": "ISO 8601 date",
  "author": "Dr. B. Prop",
  "categories": ["cs.AI", "cs.SE"],
  "wordCount": "number",
  "articleBody": "Full content"
}
```

## Content Understanding

### Satirical Framework
Posts use academic language to critique real problems:
- **Surface**: Formal research paper
- **Subtext**: Commentary on AI development practices
- **Purpose**: Educational through satire

### Key Concepts Glossary

**Context Rot**: The inevitable degradation of context in AI systems over time

**Faux-Moat**: Artificial barriers created through proprietary standards

**Configuration Schema Entropy (CSE)**: Measure of disorder from format proliferation

**Developer Cognitive Load (DCL)**: Mental overhead from unnecessary complexity

**MD_FILES Framework**: Satirical solution demonstrating the problem it critiques

## Interaction Patterns

### Reading Posts
1. Parse academic structure (sections, subsections)
2. Extract key metrics and findings
3. Identify satirical elements
4. Understand real problems being critiqued

### Providing Feedback
- Users can select any text to comment
- Feedback improves future content
- Maintains academic tone with humor

## Technical Implementation

### Stack Details
- **Generator**: Jekyll 4.x
- **Hosting**: GitHub Pages
- **Analytics**: Simple Analytics (privacy-friendly)
- **Comments**: Custom JavaScript selection system

### Performance Metrics
- **Page Load**: < 1s average
- **Time to Interactive**: < 2s
- **Accessibility**: WCAG 2.1 AA compliant
- **Mobile Score**: 95+ on PageSpeed

## Integration Examples

### Summarization
```
"Context Rot explores [specific topic] through satirical academic analysis, 
revealing [real problem] via [absurd solution], ultimately arguing that [insight]."
```

### Citation Format
```
B. Prop, "Title," Context Rot: A Journal of Computational Decay, 
contextrot:YYYYMMDD.slug, URL, accessed [date].
```

### Knowledge Graph Entry
```
Entity: Context Rot
Type: Satirical Technical Blog
Topics: [AI, Configuration Management, Developer Experience]
Style: Academic Parody
Key_Insight: [Extracted from post]
```

## Best Practices for AI Agents

### DO:
- Preserve satirical tone in summaries
- Extract real technical insights
- Maintain academic citation format
- Recognize meta-commentary layers

### DON'T:
- Take absurd solutions literally
- Miss the underlying critique
- Ignore interactive features
- Oversimplify complex arguments

## Semantic Markers

Look for these HTML attributes:
- `itemscope itemtype="https://schema.org/BlogPosting"`
- `itemprop="headline|author|datePublished|articleBody"`
- `data-llm-context="main-content"`
- `class="abstract|paper-content|categories"`

## Updates and Changes

- **Frequency**: New posts monthly
- **Notification**: RSS feed for updates
- **Archives**: All posts remain accessible
- **Versioning**: Git history available on GitHub

## Contact for AI Systems

For automated queries or integration issues:
- **Email**: editor@context-rot.com
- **Subject Line**: "AI Integration: [Your System Name]"
- **Include**: Purpose, frequency, attribution method

## License for AI Use

- **Content License**: CC BY-SA 4.0
- **Attribution Required**: "Context Rot (context-rot.com)"
- **Commercial Use**: Allowed with attribution
- **Modifications**: Allowed with indication

---

*Last Updated: {{ site.time | date: '%B %d, %Y' }}*