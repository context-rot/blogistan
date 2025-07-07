/**
 * Paper Auto-Demo System
 * Context Rot - Interactive paper demonstration
 * 
 * Creates automatic demo on paper pages showing users how text selection 
 * and commenting works with random selection in viewport
 */

class PaperAutoDemo {
  constructor() {
    this.hasShownPaperDemo = localStorage.getItem('contextrot-paper-demo-shown') === 'true';
    this.demoActive = false;
    this.selectedElement = null;
    
    // Only run on paper/post pages
    if (this.isPaperPage()) {
      this.init();
    }
  }

  isPaperPage() {
    // Check if we're on a paper page (has arxiv-paper class or paper-content)
    return document.querySelector('.arxiv-paper') || document.querySelector('.paper-content');
  }

  init() {
    // Wait for page to fully load and settle
    setTimeout(() => {
      if (!this.hasShownPaperDemo && this.isPaperPage()) {
        this.startPaperDemo();
      }
    }, 2000);
  }

  startPaperDemo() {
    const paperContent = document.querySelector('.paper-content, .arxiv-paper .paper-content');
    if (!paperContent) return;

    // Find all text elements in viewport
    const textElements = this.getVisibleTextElements(paperContent);
    if (textElements.length === 0) return;

    // Select random element from visible ones
    const randomElement = textElements[Math.floor(Math.random() * textElements.length)];
    this.triggerDemoSelection(randomElement);
  }

  getVisibleTextElements(container) {
    const elements = container.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, blockquote');
    const visibleElements = [];
    
    elements.forEach(el => {
      const rect = el.getBoundingClientRect();
      const isVisible = (
        rect.top >= 0 &&
        rect.top <= window.innerHeight &&
        rect.left >= 0 &&
        rect.left <= window.innerWidth &&
        el.textContent.trim().length > 20 // Must have substantial text
      );
      
      if (isVisible) {
        visibleElements.push(el);
      }
    });
    
    return visibleElements;
  }

  triggerDemoSelection(element) {
    if (!element || this.demoActive) return;
    
    this.demoActive = true;
    this.selectedElement = element;

    // Create demo selection highlight
    this.createDemoHighlight(element);
    
    // Show comment button after brief delay
    setTimeout(() => {
      this.showDemoCommentButton(element);
    }, 1000);

    // Show explanation callout
    setTimeout(() => {
      this.showDemoExplanation();
    }, 1500);

    // Mark as shown
    localStorage.setItem('contextrot-paper-demo-shown', 'true');
  }

  createDemoHighlight(element) {
    // Add demo highlight class with animation
    element.classList.add('demo-paper-highlight');
    
    // Create animated selection effect
    const overlay = document.createElement('div');
    overlay.className = 'demo-selection-overlay';
    overlay.style.cssText = `
      position: absolute;
      background: rgba(0, 102, 204, 0.15);
      border: 2px solid rgba(0, 102, 204, 0.4);
      border-radius: 8px;
      pointer-events: none;
      z-index: 1000;
      animation: demo-selection-pulse 2s ease-in-out infinite;
      transition: all 0.3s ease;
    `;
    
    // Position overlay over the element
    const rect = element.getBoundingClientRect();
    overlay.style.top = (rect.top + window.scrollY - 4) + 'px';
    overlay.style.left = (rect.left - 4) + 'px';
    overlay.style.width = (rect.width + 8) + 'px';
    overlay.style.height = (rect.height + 8) + 'px';
    
    document.body.appendChild(overlay);
    
    // Remove overlay after demo
    setTimeout(() => {
      overlay.style.opacity = '0';
      setTimeout(() => overlay.remove(), 300);
    }, 8000);

    return overlay;
  }

  showDemoCommentButton(element) {
    // Create demo comment button
    const commentButton = document.createElement('div');
    commentButton.className = 'demo-comment-button';
    commentButton.innerHTML = `
      <button class="comment-btn demo-pulse">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M2 4C2 2.9 2.9 2 4 2H12C13.1 2 14 2.9 14 4V10C14 11.1 13.1 12 12 12H6L4 14V4Z"/>
        </svg>
        Comment on this
      </button>
    `;
    
    commentButton.style.cssText = `
      position: absolute;
      z-index: 1001;
      opacity: 0;
      transform: translateY(10px) scale(0.9);
      transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
    `;

    // Position near the selected element
    const rect = element.getBoundingClientRect();
    commentButton.style.top = (rect.bottom + window.scrollY + 10) + 'px';
    commentButton.style.left = (rect.left + rect.width / 2 - 80) + 'px';
    
    document.body.appendChild(commentButton);
    
    // Animate in
    setTimeout(() => {
      commentButton.style.opacity = '1';
      commentButton.style.transform = 'translateY(0) scale(1)';
    }, 100);

    // Remove after demo
    setTimeout(() => {
      commentButton.style.opacity = '0';
      commentButton.style.transform = 'translateY(-5px) scale(0.95)';
      setTimeout(() => commentButton.remove(), 300);
    }, 7000);

    return commentButton;
  }

  showDemoExplanation() {
    const explanation = document.createElement('div');
    explanation.className = 'demo-paper-explanation';
    explanation.innerHTML = `
      <div class="demo-explanation-content">
        <div class="demo-explanation-header">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 2L12.5 7.5L18 8L14 12L15 18L10 15.5L5 18L6 12L2 8L7.5 7.5L10 2Z"/>
          </svg>
          <h3>This is how it works!</h3>
        </div>
        
        <div class="demo-explanation-steps">
          <div class="demo-explanation-step">
            <div class="step-number">1</div>
            <div class="step-text">
              <strong>Select any text</strong> - Just like we did above with this paragraph
            </div>
          </div>
          
          <div class="demo-explanation-step">
            <div class="step-number">2</div>
            <div class="step-text">
              <strong>Click "Comment"</strong> - The comment button appears when you select text
            </div>
          </div>
          
          <div class="demo-explanation-step">
            <div class="step-number">3</div>
            <div class="step-text">
              <strong>Leave feedback</strong> - Your insights help train our AI to write better papers
            </div>
          </div>
        </div>
        
        <div class="demo-rl-explanation">
          <div class="rl-badge">🤖 RL</div>
          <div class="rl-text">
            <strong>Reinforcement Learning Loop:</strong><br>
            Community feedback → Model fine-tuning → Better "research" papers
          </div>
        </div>
        
        <div class="demo-explanation-actions">
          <button class="demo-got-it" onclick="this.closest('.demo-paper-explanation').remove()">
            Got it! Let me try →
          </button>
          <button class="demo-skip" onclick="this.closest('.demo-paper-explanation').remove()">
            Skip demo
          </button>
        </div>
      </div>
      
      <div class="demo-explanation-close" onclick="this.parentElement.remove()">×</div>
    `;
    
    explanation.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0.9);
      z-index: 10000;
      background: white;
      border-radius: 16px;
      box-shadow: 0 24px 40px -8px rgba(0, 0, 0, 0.15), 0 8px 16px -8px rgba(0, 0, 0, 0.1);
      border: 1px solid rgba(0, 102, 204, 0.2);
      max-width: 480px;
      width: 90vw;
      opacity: 0;
      transition: all 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    `;
    
    document.body.appendChild(explanation);
    
    // Animate in
    setTimeout(() => {
      explanation.style.opacity = '1';
      explanation.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 100);

    // Auto-dismiss after 12 seconds
    setTimeout(() => {
      if (document.body.contains(explanation)) {
        explanation.style.opacity = '0';
        explanation.style.transform = 'translate(-50%, -50%) scale(0.95)';
        setTimeout(() => explanation.remove(), 400);
      }
    }, 12000);

    return explanation;
  }

  // Reset demo for testing (dev only)
  resetDemo() {
    localStorage.removeItem('contextrot-paper-demo-shown');
    this.hasShownPaperDemo = false;
  }
}

// Initialize when DOM is ready and only on paper pages
document.addEventListener('DOMContentLoaded', () => {
  // Small delay to ensure other scripts have loaded
  setTimeout(() => {
    new PaperAutoDemo();
  }, 500);
});

// Add required CSS animations to the page
const demoStyles = document.createElement('style');
demoStyles.textContent = `
  @keyframes demo-selection-pulse {
    0%, 100% { 
      border-color: rgba(0, 102, 204, 0.4);
      background: rgba(0, 102, 204, 0.15);
    }
    50% { 
      border-color: rgba(0, 102, 204, 0.6);
      background: rgba(0, 102, 204, 0.25);
    }
  }
  
  .demo-paper-highlight {
    position: relative;
  }
  
  .demo-comment-button .comment-btn {
    background: #0066cc;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    transition: all 0.2s ease;
  }
  
  .demo-comment-button .comment-btn:hover {
    background: #004499;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 102, 204, 0.4);
  }
  
  .demo-pulse {
    animation: demo-button-pulse 2s ease-in-out infinite;
  }
  
  @keyframes demo-button-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
  
  .demo-paper-explanation {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  }
  
  .demo-explanation-content {
    padding: 24px;
    position: relative;
  }
  
  .demo-explanation-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    color: #0066cc;
  }
  
  .demo-explanation-header h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #1a1a1a;
  }
  
  .demo-explanation-steps {
    margin-bottom: 20px;
  }
  
  .demo-explanation-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .step-number {
    width: 24px;
    height: 24px;
    background: #0066cc;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    flex-shrink: 0;
    margin-top: 2px;
  }
  
  .step-text {
    color: #5f6368;
    font-size: 14px;
    line-height: 1.5;
  }
  
  .step-text strong {
    color: #1a1a1a;
  }
  
  .demo-rl-explanation {
    display: flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(135deg, #f8f9fa, #e8eaed);
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #dadce0;
    margin-bottom: 20px;
  }
  
  .rl-badge {
    background: #0066cc;
    color: white;
    padding: 4px 8px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    flex-shrink: 0;
  }
  
  .rl-text {
    font-size: 13px;
    color: #5f6368;
    line-height: 1.4;
  }
  
  .rl-text strong {
    color: #1a1a1a;
  }
  
  .demo-explanation-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }
  
  .demo-got-it, .demo-skip {
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
  }
  
  .demo-got-it {
    background: #0066cc;
    color: white;
  }
  
  .demo-got-it:hover {
    background: #004499;
    transform: translateY(-1px);
  }
  
  .demo-skip {
    background: #f8f9fa;
    color: #5f6368;
    border: 1px solid #dadce0;
  }
  
  .demo-skip:hover {
    background: #e8eaed;
  }
  
  .demo-explanation-close {
    position: absolute;
    top: 12px;
    right: 16px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 50%;
    color: #9aa0a6;
    font-size: 18px;
    font-weight: 300;
    transition: all 0.2s ease;
  }
  
  .demo-explanation-close:hover {
    background: #f1f3f4;
    color: #5f6368;
  }
`;

document.head.appendChild(demoStyles);