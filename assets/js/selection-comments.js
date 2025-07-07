// Selection and comment functionality with rate limiting
(function() {
  'use strict';
  
  let selectedText = '';
  let selectedElement = null;
  let tooltip = null;
  
  // Rate limiting configuration
  const RATE_LIMIT = {
    maxAttempts: 3,
    windowMinutes: 60,
    storageKey: 'contextrot_feedback_attempts'
  };
  
  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', function() {
    tooltip = document.getElementById('selection-tooltip');
    if (!tooltip) return;
    
    const paperContent = document.getElementById('paper-content');
    if (!paperContent) return;
    
    // Handle text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('touchend', handleSelection);
    
    // Handle comment button click
    const commentBtn = document.getElementById('comment-button');
    if (commentBtn) {
      commentBtn.addEventListener('click', openFeedbackIssue);
    }
    
    // Hide tooltip on outside click
    document.addEventListener('click', function(e) {
      if (!tooltip.contains(e.target) && !window.getSelection().toString()) {
        hideTooltip();
      }
    });
    
    // Hide tooltip on scroll
    window.addEventListener('scroll', hideTooltip);
  });
  
  function handleSelection(e) {
    setTimeout(() => {
      const selection = window.getSelection();
      const text = selection.toString().trim();
      
      if (text.length === 0) {
        hideTooltip();
        return;
      }
      
      if (text.length < 5) {
        hideTooltip();
        return; // Don't show tooltip for very short selections
      }
      
      selectedText = text;
      selectedElement = selection.anchorNode;
      
      // Get selection position
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      
      showTooltip(rect);
    }, 50);
  }
  
  function showTooltip(rect) {
    if (!tooltip) return;
    
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
      // On mobile, show at bottom of screen
      tooltip.style.position = 'fixed';
      tooltip.style.bottom = '2rem';
      tooltip.style.left = '50%';
      tooltip.style.transform = 'translateX(-50%)';
      tooltip.style.top = 'auto';
    } else {
      // On desktop, show above selection
      tooltip.style.position = 'absolute';
      tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
      tooltip.style.top = (rect.top + window.scrollY - tooltip.offsetHeight - 10) + 'px';
      tooltip.style.transform = 'none';
      tooltip.style.bottom = 'auto';
    }
    
    tooltip.style.display = 'block';
    setTimeout(() => {
      tooltip.classList.add('show');
    }, 10);
  }
  
  function hideTooltip() {
    if (!tooltip) return;
    
    tooltip.classList.remove('show');
    setTimeout(() => {
      tooltip.style.display = 'none';
    }, 200);
  }
  
  // Rate limiting functions
  function getRateLimitData() {
    try {
      const data = localStorage.getItem(RATE_LIMIT.storageKey);
      return data ? JSON.parse(data) : { attempts: [], lastReset: Date.now() };
    } catch (e) {
      return { attempts: [], lastReset: Date.now() };
    }
  }
  
  function setRateLimitData(data) {
    try {
      localStorage.setItem(RATE_LIMIT.storageKey, JSON.stringify(data));
    } catch (e) {
      // Ignore localStorage errors
    }
  }
  
  function isRateLimited() {
    const data = getRateLimitData();
    const now = Date.now();
    const windowMs = RATE_LIMIT.windowMinutes * 60 * 1000;
    
    // Reset if window has passed
    if (now - data.lastReset > windowMs) {
      data.attempts = [];
      data.lastReset = now;
      setRateLimitData(data);
    }
    
    // Filter attempts within current window
    const recentAttempts = data.attempts.filter(timestamp => 
      now - timestamp < windowMs
    );
    
    return recentAttempts.length >= RATE_LIMIT.maxAttempts;
  }
  
  function recordFeedbackAttempt() {
    const data = getRateLimitData();
    data.attempts.push(Date.now());
    
    // Keep only recent attempts
    const windowMs = RATE_LIMIT.windowMinutes * 60 * 1000;
    const now = Date.now();
    data.attempts = data.attempts.filter(timestamp => 
      now - timestamp < windowMs
    );
    
    setRateLimitData(data);
  }
  
  function getTimeUntilReset() {
    const data = getRateLimitData();
    const windowMs = RATE_LIMIT.windowMinutes * 60 * 1000;
    const now = Date.now();
    
    if (data.attempts.length === 0) return 0;
    
    const oldestAttempt = Math.min(...data.attempts);
    const resetTime = oldestAttempt + windowMs;
    
    return Math.max(0, resetTime - now);
  }

  function openFeedbackIssue() {
    if (!selectedText) return;
    
    // Check rate limiting
    if (isRateLimited()) {
      const timeUntilReset = getTimeUntilReset();
      const minutesLeft = Math.ceil(timeUntilReset / (1000 * 60));
      
      showToast(`Rate limit reached! Please wait ${minutesLeft} minutes before submitting more feedback. 
                 This helps prevent spam and ensures quality discussions.`, 'warning');
      hideTooltip();
      return;
    }
    
    // Get the current page info
    const title = document.querySelector('.paper-title')?.textContent || document.title;
    const url = window.location.href;
    
    // Find line number (approximate)
    const lineNumber = findApproximateLineNumber();
    
    // Create GitHub issue URL
    const repoUrl = getRepositoryUrl();
    const issueTitle = encodeURIComponent(`Feedback on "${title}" - Line ${lineNumber}`);
    const issueBody = encodeURIComponent(`## Selected Text
> ${selectedText}

## My Feedback
[Please provide your feedback, suggestions, corrections, or insights here]

## Context
- Paper: ${title}
- URL: ${url}
- Approximate line: ${lineNumber}

---
*This feedback was submitted via the interactive comment system. Thank you for helping improve the quality of our research!*`);
    
    const issueUrl = `${repoUrl}/issues/new?title=${issueTitle}&body=${issueBody}&labels=reader-feedback`;
    
    // Record the attempt for rate limiting
    recordFeedbackAttempt();
    
    // Open in new tab
    window.open(issueUrl, '_blank', 'noopener,noreferrer');
    
    // Show thank you message with rate limit info
    const data = getRateLimitData();
    const remaining = RATE_LIMIT.maxAttempts - data.attempts.length;
    showToast(`Thank you! Opening GitHub issue for your feedback... (${remaining} submissions remaining this hour)`);
    
    // Hide tooltip
    hideTooltip();
  }
  
  function findApproximateLineNumber() {
    if (!selectedElement) return 1;
    
    const paperContent = document.getElementById('paper-content');
    if (!paperContent) return 1;
    
    // Count paragraphs and headings before the selection
    const walker = document.createTreeWalker(
      paperContent,
      NodeFilter.SHOW_ELEMENT,
      {
        acceptNode: function(node) {
          if (['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LI'].includes(node.tagName)) {
            return NodeFilter.FILTER_ACCEPT;
          }
          return NodeFilter.FILTER_SKIP;
        }
      }
    );
    
    let lineCount = 1;
    let currentNode = walker.nextNode();
    
    while (currentNode && !currentNode.contains(selectedElement)) {
      lineCount++;
      currentNode = walker.nextNode();
    }
    
    return lineCount;
  }
  
  function getRepositoryUrl() {
    // Try to get from meta tag or config
    const metaRepo = document.querySelector('meta[property="github:repository"]');
    if (metaRepo) {
      return `https://github.com/${metaRepo.content}`;
    }
    
    // Fallback to hardcoded (should be replaced with Jekyll variable)
    return 'https://github.com/context-rot/blogistan';
  }
  
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `feedback-toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);
    
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        document.body.removeChild(toast);
      }, 300);
    }, 3000);
  }
  
  // Keyboard shortcuts
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to open feedback for selected text
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && selectedText) {
      e.preventDefault();
      openFeedbackIssue();
    }
    
    // Escape to hide tooltip
    if (e.key === 'Escape') {
      hideTooltip();
    }
  });
  
})();