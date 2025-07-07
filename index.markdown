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
    <h2>How to Play</h2>
  </div>
  
  <div class="guide-content">
    <p>
      This isn't your typical blog. Or maybe it is. It's probably something worse. The AI I used to slop this together tried to tell me it's an <strong>interactive research environment</strong>. Uh. Yeah. "Research". Let's go with that. It's a relative term these days, anyway.
    </p>
    
    <p>
      So, the concept/hook/gig here is simple: Put on your sarcastic-pseudo-science hat, read some "papers", and react by 
      selecting any text in our papers to provide line-specific feedback, corrections, or insights.
    </p>
    
    <p>
      Your contributions help improve our research and may influence future papers through our 
      AI feedback integration system. ICL. RL. All the things. The AI used to write these gets fine-tuned, post-trained, optimized, all that stuff.
    </p>
    
    <div class="cta-box">
      <p><strong>Go ahead, try it!</strong> Find something interesting, select it, and click the comment button. Find or introduce errors, satire, or anything worth discussing. Or not discussing.</p>
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
