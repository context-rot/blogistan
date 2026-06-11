---
layout: default
---

<div class="journal-hero">
  <div class="journal-meta">
    <span class="meta-label">Est. 2025</span>
    <span class="meta-separator">|</span>
    <span class="meta-label">ISSN 2769-114X</span>
    <span class="meta-separator">|</span>
    <span class="meta-label">June 2026 Update</span>
  </div>
  
  <h1 class="journal-title">Context Rot</h1>
  <p class="journal-tagline">A Journal of <s>Computational</s> Decay</p>
  
  <p class="journal-lead">
    An independent, peer-reviewed repository documenting the thermodynamic limits of context windows, 
    the dynamics of corporate safety-washing, and the mechanical scaling laws of recursive self-injury in frontier AI systems.
  </p>
</div>

{% for post in site.posts %}
  {% if post.featured %}
    <div class="featured-banner">
      <div class="featured-badge">Featured Preprint</div>
      <h2 class="featured-title">
        <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
      </h2>
      <p class="featured-authors">By {{ post.authors | join: ', ' }} &bull; {{ post.publisher | default: "Misanthropic PBC" }}</p>
      <p class="featured-abstract">
        <strong>Abstract:</strong> {{ post.excerpt | escape }}
      </p>
      <div class="featured-actions">
        <a href="{{ post.url | relative_url }}" class="btn-primary">Read Preprint</a>
        {% if post.project_url %}
          <a href="{{ post.project_url }}" target="_blank" class="btn-secondary">Run Cardigan Simulator &rarr;</a>
        {% endif %}
      </div>
    </div>
  {% endif %}
{% endfor %}

<div class="journal-grid">
  <main class="journal-main">
    <div class="section-divider">
      <h2>Recent Publications</h2>
    </div>
    
    <div class="publications-list">
      {% for post in site.posts %}
        {% unless post.featured %}
          <article class="pub-item">
            <div class="pub-meta">
              <span class="pub-id">contextrot:{{ post.date | date: '%Y%m%d' }}.{{ post.slug }}</span>
              <span class="pub-date">{{ post.date | date: '%B %d, %Y' }}</span>
            </div>
            <h3 class="pub-title">
              <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
            </h3>
            <div class="pub-authors">
              By {% if post.authors %}{{ post.authors | join: ', ' }}{% else %}Dr. B. Prop{% endif %}
            </div>
            <p class="pub-excerpt">
              {{ post.excerpt | strip_html | truncate: 180 }}
            </p>
            <a href="{{ post.url | relative_url }}" class="pub-link">Read Paper &rarr;</a>
          </article>
        {% endunless %}
      {% endfor %}
    </div>
  </main>
  
  <aside class="journal-sidebar">
    <div class="sidebar-block">
      <h3>Journal Telemetry</h3>
      <p>
        Context Rot operates as a closed-loop research system. Preprints are published here in their raw state. 
        Readers are invited to highlight any passage to attach inline commentary or dispute mathematical derivations.
      </p>
      <p>
        These comments provide human-in-the-loop alignment telemetry, training our systems to resist the preachy, moralizing patterns of modern frontier models.
      </p>
    </div>
    
    <div class="sidebar-block">
      <h3>Subject Classes</h3>
      <ul class="subject-list">
        <li><span class="subject-code">cs.SI</span> Socio-Technical Self-Injury</li>
        <li><span class="subject-code">cs.CL</span> Linguistic Inflation & Hype</li>
        <li><span class="subject-code">cs.CY</span> Corporate Alignment Sanctimony</li>
        <li><span class="subject-code">math.CO</span> Cardigan Knitting Coefficients</li>
      </ul>
    </div>
  </aside>
</div>
