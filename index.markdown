---
layout: default
---

<div class="home-intro">
  <h2>Welcome to Context Rot</h2>
  <p class="lead">
    A journal of computational decay, featuring ArXiv-style preprints that explore 
    the inevitable entropy of context in AI systems. Each paper combines rigorous 
    analysis with appropriate academic irreverence.
  </p>
  
  <div class="interaction-guide">
    <h3>§ How to Play</h3>
    <p>
      This isn't your typical blog. Or maybe it is. It's probably something worse. The AI I used to slop this together tried to tell me it's an <strong>interactive research environment</strong>. Uh. Yeah. "Research". Let's go with that. It's a relative term these days, anyway.

      </p>
      <p>
      So, the concept/hook/gig here is simple. Put on your sarcastic-pseudo-science hat, read some "papers", and react by 
      selecting any text in our papers to provide line-specific feedback, corrections, or insights. 
      Your contributions help improve our research and may influence future papers through our 
      AI feedback integration system. ICL. RL. All the things. The AI used to write these gets fine-tuned, post-trained, optimized, all that stuff. 

    </p>
    <p>
I will build this in the open. Just getting started now. I'll OSS the stuff as I build it.
    </p>
    <p class="cta">
      <strong>Go ahead, try it!</strong> Find something interesting, select it, and click the comment button. 
      Find or introduce errors, satire, or anything worth discussing. Or not discussing.
    </p>
  </div>
</div>

<section class="recent-papers">
  <h2>Recent Publications</h2>
  
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
              <a href="{{ post.url | relative_url }}" class="read-paper">Read Full Paper →</a>
            </footer>
          </article>
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>No papers published yet. Check back soon for groundbreaking research on computational decay!</p>
  {% endif %}
</section>
