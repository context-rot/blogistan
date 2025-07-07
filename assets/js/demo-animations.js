/**
 * Demo Animations & Micro-interactions
 * Context Rot - Sophisticated UI animations
 */

class DemoAnimations {
  constructor() {
    this.hasShownDemo = localStorage.getItem('contextrot-demo-shown') === 'true';
    this.init();
  }

  init() {
    this.setupScrollAnimations();
    this.setupMicroInteractions();
    
    // Show auto-demo after 3 seconds if user hasn't seen it
    if (!this.hasShownDemo) {
      setTimeout(() => this.showAutoDemo(), 3000);
    }
  }

  showAutoDemo() {
    const demoText = this.createDemoText();
    const demoTooltip = this.createDemoTooltip();
    
    // Insert demo elements
    document.body.appendChild(demoText);
    document.body.appendChild(demoTooltip);
    
    // Animate demo sequence
    this.runDemoSequence(demoText, demoTooltip);
  }

  createDemoText() {
    const demo = document.createElement('div');
    demo.className = 'demo-text-container';
    demo.innerHTML = `
      <div class="demo-text">
        <span class="demo-highlight">Select any text like this</span> to leave feedback and comments!
      </div>
      <div class="demo-close" onclick="this.parentElement.remove()">×</div>
    `;
    return demo;
  }

  createDemoTooltip() {
    const tooltip = document.createElement('div');
    tooltip.className = 'demo-tooltip';
    tooltip.innerHTML = `
      <div class="demo-tooltip-content">
        <div class="demo-tooltip-header">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 0C3.58 0 0 3.58 0 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm3.5 6L7 10.5 4.5 8 5.91 6.59 7 7.68l3.59-3.59L12 5.5z"/>
          </svg>
          <span>Interactive Research Papers</span>
        </div>
        <div class="demo-steps">
          <div class="demo-step">
            <span class="demo-step-number">1</span>
            <span>Select any text in research papers</span>
          </div>
          <div class="demo-step">
            <span class="demo-step-number">2</span>
            <span>Leave feedback, corrections, or insights</span>
          </div>
          <div class="demo-step">
            <span class="demo-step-number">3</span>
            <span>Your comments train our AI to write better papers</span>
          </div>
        </div>
        <div class="demo-rl-note">
          <small>🤖 <strong>RL Loop:</strong> Community feedback → Model fine-tuning → Better research</small>
        </div>
        <button class="demo-dismiss" onclick="this.closest('.demo-tooltip').remove()">Start Reading →</button>
      </div>
    `;
    return tooltip;
  }

  runDemoSequence(demoText, demoTooltip) {
    // Phase 1: Show demo text
    setTimeout(() => {
      demoText.classList.add('demo-active');
    }, 100);

    // Phase 2: Simulate text selection
    setTimeout(() => {
      const highlight = demoText.querySelector('.demo-highlight');
      highlight.classList.add('demo-selected');
    }, 1500);

    // Phase 3: Show tooltip
    setTimeout(() => {
      demoTooltip.classList.add('demo-tooltip-active');
    }, 2500);

    // Phase 4: Auto-dismiss after 8 seconds
    setTimeout(() => {
      this.dismissDemo(demoText, demoTooltip);
    }, 8000);

    // Mark as shown
    localStorage.setItem('contextrot-demo-shown', 'true');
  }

  dismissDemo(demoText, demoTooltip) {
    demoText?.classList.add('demo-fade-out');
    demoTooltip?.classList.add('demo-fade-out');
    
    setTimeout(() => {
      demoText?.remove();
      demoTooltip?.remove();
    }, 500);
  }

  setupScrollAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
      threshold: 0.15,
      rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          
          // Special handling for post list items
          if (entry.target.classList.contains('post-list')) {
            const listItems = entry.target.querySelectorAll('li');
            listItems.forEach(item => {
              item.classList.add('animate-in');
            });
          }
        }
      });
    }, observerOptions);

    // Immediate animation for hero elements
    const heroElements = document.querySelectorAll('.hero-content, .hero-visual');
    setTimeout(() => {
      heroElements.forEach(el => el.classList.add('animate-in'));
    }, 300);

    // Observe elements for scroll animation
    const animateElements = document.querySelectorAll(
      '.paper-preview, .interaction-section, .recent-papers, .modern-card, .post-list'
    );
    
    animateElements.forEach(el => {
      observer.observe(el);
    });

    // Progressive disclosure observer
    const progressiveElements = document.querySelectorAll('.widen-on-scroll');
    progressiveElements.forEach(el => {
      observer.observe(el);
    });

    // Parallax effect for hero image
    this.setupParallax();
    
    // Staggered section animations
    this.setupStaggeredAnimations();
  }

  setupParallax() {
    const heroImage = document.querySelector('.hero-image');
    if (!heroImage) return;

    let ticking = false;
    
    const updateParallax = () => {
      const scrolled = window.pageYOffset;
      const rate = scrolled * -0.2;
      
      if (scrolled < window.innerHeight * 1.5) {
        heroImage.style.transform = `translateY(${rate}px)`;
      }
      ticking = false;
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    });
  }

  setupStaggeredAnimations() {
    // Additional entrance animations for content sections
    const sections = document.querySelectorAll('section');
    
    sections.forEach((section, index) => {
      section.style.animationDelay = `${index * 0.1}s`;
    });

    // Enhanced scroll-triggered effects
    const enhancedObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Add subtle scale effect to images
          const images = entry.target.querySelectorAll('img');
          images.forEach((img, index) => {
            setTimeout(() => {
              img.style.transform = 'scale(1)';
              img.style.opacity = '1';
            }, index * 100);
          });

          // Animate text elements progressively
          const textElements = entry.target.querySelectorAll('h2, h3, p');
          textElements.forEach((el, index) => {
            setTimeout(() => {
              el.style.opacity = '1';
              el.style.transform = 'translateY(0)';
            }, index * 50);
          });
        }
      });
    }, {
      threshold: 0.2,
      rootMargin: '0px 0px -50px 0px'
    });

    // Apply to sections that should have enhanced animations
    const enhancedSections = document.querySelectorAll('.interaction-section, .recent-papers');
    enhancedSections.forEach(section => {
      enhancedObserver.observe(section);
      
      // Pre-set styles for animation
      const textElements = section.querySelectorAll('h2, h3, p');
      textElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1)';
      });
    });
  }

  setupMicroInteractions() {
    // Enhanced button interactions
    const buttons = document.querySelectorAll('.modern-button, .read-paper');
    buttons.forEach(button => {
      button.addEventListener('mouseenter', (e) => {
        this.createRipple(e);
      });
    });

    // Subtle card hover effects (no more disorienting tilt)
    const cards = document.querySelectorAll('.paper-preview, .modern-card');
    cards.forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.style.transition = 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)';
        card.style.transform = 'translateY(-4px) scale(1.01)';
        card.style.boxShadow = '0 20px 40px -12px rgba(0, 0, 0, 0.15), 0 8px 16px -8px rgba(0, 0, 0, 0.1)';
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = '';
      });
    });

    // Icon pulse on hover
    const icons = document.querySelectorAll('.guide-icon, .section-icon');
    icons.forEach(icon => {
      icon.addEventListener('mouseenter', () => {
        icon.style.animation = 'icon-pulse 0.6s ease-out';
      });
      
      icon.addEventListener('animationend', () => {
        icon.style.animation = '';
      });
    });

    // Category chip hover effects
    const categories = document.querySelectorAll('.category');
    categories.forEach(category => {
      category.addEventListener('mouseenter', () => {
        category.style.transform = 'translateY(-1px)';
        category.style.boxShadow = '0 4px 8px rgba(0, 102, 204, 0.3)';
      });
      
      category.addEventListener('mouseleave', () => {
        category.style.transform = '';
        category.style.boxShadow = '';
      });
    });
  }

  createRipple(e) {
    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const ripple = document.createElement('span');
    const size = Math.max(rect.width, rect.height);
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
    ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
    ripple.classList.add('ripple-effect');
    
    button.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
  }

  // Removed the disorienting cardTiltEffect method
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new DemoAnimations();
  
  // Hide page loader after content is ready
  window.addEventListener('load', () => {
    const loader = document.querySelector('.page-loader');
    if (loader) {
      setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 300);
      }, 1000);
    }
  });
});

// Smooth scroll for anchor links
document.addEventListener('click', (e) => {
  if (e.target.matches('a[href^="#"]')) {
    e.preventDefault();
    const target = document.querySelector(e.target.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }
  }
});