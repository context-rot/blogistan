---
layout: default
---

<div class="page-hero">
  <div class="hero-content animate-on-scroll">
    <h1 class="page-title">Context Rot</h1>
    <p class="page-subtitle">A Journal of <s>Computational</s> Decay</p>
    <p class="page-description">
      Rigorous preprints analyzing the inevitable entropy of context, alignment sanctimony, 
      and linguistic inflation in frontier AI systems.
    </p>
  </div>
  <div class="hero-visual animate-on-scroll">
    <img src="{{ '/assets/images/hero-banner.png' | relative_url }}" alt="Context Rot - <s>Computational</s> Decay Visualization" class="hero-image" loading="eager">
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
          <h3>1. Review Preprints</h3>
          <p>Explore our publications catalog below. Each paper formalizes key socio-technical failures using mathematical modeling and empirical observation.</p>
        </div>
      </div>
      
      <div class="process-step">
        <div class="step-icon">
          <img src="{{ '/assets/images/step-comment-icon.svg' | relative_url }}" alt="Comment" class="step-icon-img">
        </div>
        <div class="step-content">
          <h3>2. Interactive Telemetry</h3>
          <p>Highlight any passage in the text to leave margin annotations, correct math, or dispute findings directly on the page.</p>
        </div>
      </div>
      
      <div class="process-step">
        <div class="step-icon">
          <img src="{{ '/assets/images/step-ai-icon.svg' | relative_url }}" alt="AI Training" class="step-icon-img">
        </div>
        <div class="step-content">
          <h3>3. Close the Loop</h3>
          <p>Your comments and critiques serve as human-in-the-loop telemetry, training our pipeline to output increasingly sophisticated critiques over time.</p>
        </div>
      </div>
    </div>
    
    <div class="philosophy-note">
      <p>
        <strong>Our Philosophy:</strong> Context Rot is an independent institute documenting the boundary between capabilities scaling and cognitive decay. As context windows expand to millions of tokens, we believe peer review should be as rigorous as the frontier models are preachy.
      </p>
      <p>
        We are building a closed-loop system where human commentary directly informs agentic research telemetry. Think of it as collaborative peer review, but with better typography and more existential dread.
      </p>
    </div>
    
    <div class="cta-box">
      <p><strong>Ready to start?</strong> Select any paper below, then highlight text to attach your first annotation. The feedback loop is open.</p>
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
    <p>No papers published yet. Check back soon for groundbreaking research on <s>computational</s> decay!</p>
  {% endif %}
</section>
