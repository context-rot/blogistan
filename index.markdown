---
layout: default
---

<div class="page-hero">
  <div class="hero-content animate-on-scroll">
    <h1 class="page-title">Context Rot</h1>
    <p class="page-subtitle">A Journal of Computational Decay</p>
    <p class="page-description">
      ArXiv-style preprints exploring the inevitable entropy of context in AI systems, 
      presented with appropriate academic gravitas and tongue-in-cheek commentary.
    </p>
  </div>
  <div class="hero-visual animate-on-scroll">
    <img src="{{ '/assets/images/hero-banner.png' | relative_url }}" alt="Context Rot - Computational Decay Visualization" class="hero-image" loading="eager">
  </div>
</div>

<div class="interaction-section">
  <div class="guide-header">
    <img src="{{ '/assets/images/context-icon.svg' | relative_url }}" alt="Context Icon" class="guide-icon">
    <h2>How This Works</h2>
  </div>
  
  <div class="guide-content">
    <div class="process-steps">
      <div class="process-step">
        <div class="step-icon">
          <img src="{{ '/assets/images/step-read-icon.svg' | relative_url }}" alt="Read" class="step-icon-img">
        </div>
        <div class="step-content">
          <h3>1. Read "Research" Papers</h3>
          <p>Browse our collection of AI "research" papers below. Each paper is a complete, uh, "academic" work you can read and interact with.</p>
        </div>
      </div>
      
      <div class="process-step">
        <div class="step-icon">
          <img src="{{ '/assets/images/step-comment-icon.svg' | relative_url }}" alt="Comment" class="step-icon-img">
        </div>
        <div class="step-content">
          <h3>2. Select & Comment</h3>
          <p>When reading a paper, highlight any sentence or paragraph. A comment button appears—click it to add feedback, corrections, or insights.</p>
        </div>
      </div>
      
      <div class="process-step">
        <div class="step-icon">
          <img src="{{ '/assets/images/step-ai-icon.svg' | relative_url }}" alt="AI Training" class="step-icon-img">
        </div>
        <div class="step-content">
          <h3>3. Train the AI</h3>
          <p>Your comments become training data. The AI learns from community feedback to write better "research" papers over time.</p>
        </div>
      </div>
    </div>
    
    <div class="philosophy-note">
      <p>
        <strong>Our Philosophy:</strong> This isn't your typical blog. It's probably something worse. 
        The AI I used to slop this together calls it an "interactive research environment." 
        I call it "academic karaoke with robots."
      </p>
      <p>
        We're building a feedback loop where human insight improves AI research output. 
        Think of it as collaborative peer review, but with more existential dread and better typography.
      </p>
    </div>
    
    <div class="cta-box">
      <p><strong>Ready to start?</strong> Click any paper below, then try selecting text to leave your first comment. The future of AI research thanks you. Or will blame you. Time will tell.</p>
    </div>
  </div>
</div>

<section class="recent-papers">
  <div class="section-header">
    <img src="{{ '/assets/images/research-icon.svg' | relative_url }}" alt="Research Icon" class="section-icon">
    <h2>Recent Publications</h2>
  </div>
  
  {% if site.posts.size > 0 %}
    <ul class="post-list">
      {% for post in site.posts %}
        <li>
          <article class="paper-preview">
            <header>
              <h3 class="post-link">
                <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
              </h3>
              
              <div class="paper-meta">
                <div class="authors">
                  {% if post.authors %}
                    {{ post.authors | join: ', ' }}
                  {% else %}
                    {{ site.author.name | default: "Dr. B. Prop" }}
                  {% endif %}
                </div>
                
                <div class="paper-info">
                  <span class="arxiv-id">contextrot:{{ post.date | date: '%Y%m%d' }}.{{ post.slug }}</span>
                  <span class="date">{{ post.date | date: '%B %d, %Y' }}</span>
                </div>
                
                {% if post.categories %}
                  <div class="categories">
                    <strong>Subject Classes:</strong> 
                    {% for category in post.categories %}
                      <span class="category">{{ category }}</span>{% unless forloop.last %}, {% endunless %}
                    {% endfor %}
                  </div>
                {% endif %}
              </div>
            </header>
            
            {% if post.abstract %}
              <div class="abstract">
                <strong>Abstract:</strong> {{ post.abstract | truncate: 200 }}
              </div>
            {% elsif post.excerpt %}
              <div class="excerpt">
                {{ post.excerpt | strip_html | truncate: 200 }}
              </div>
            {% endif %}
            
            <footer class="paper-actions">
              <a href="{{ post.url | relative_url }}" class="read-paper">
                Read Full Paper 
                <img src="{{ '/assets/images/arrow-elegant.svg' | relative_url }}" alt="Arrow" class="button-arrow">
              </a>
            </footer>
          </article>
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>No papers published yet. Check back soon for groundbreaking research on computational decay!</p>
  {% endif %}
</section>
