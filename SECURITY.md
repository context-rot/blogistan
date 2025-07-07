# Security Policy

## Supported Versions

Only the latest version of Context Rot is currently supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

We take security seriously at Context Rot. If you discover a security vulnerability, please follow these guidelines:

### 🚨 **DO NOT** create public issues for security vulnerabilities

### ✅ **DO** report privately via:
- **Email**: security@context-rot.com
- **Subject**: `[SECURITY] Brief description of vulnerability`

### 📋 **Include in your report:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if known)
- Your contact information for follow-up

## Response Timeline

- **48 hours**: Initial acknowledgment
- **7 days**: Regular progress updates
- **30 days**: Target resolution time

## Security Features

Context Rot implements several security measures:

### Rate Limiting
- **Client-side**: 3 feedback submissions per hour
- **Server-side**: 5 GitHub issues per 24 hours per user
- **Automatic escalation**: Suspicious activity flagged for review

### Spam Protection
- Multi-layer spam detection with AI assistance
- Keyword filtering and pattern recognition
- Account age and activity analysis
- Automatic issue closure for detected spam

### Content Security
- No user-generated content stored permanently
- All feedback routed through GitHub's secure infrastructure
- Privacy-friendly analytics (Simple Analytics)
- No tracking cookies or personal data collection

### Infrastructure Security
- GitHub Pages hosting with HTTPS enforcement
- Secrets managed via GitHub Secrets
- Regular dependency updates
- Automated security scanning (CodeQL, TruffleHog)

## Security Best Practices for Contributors

If you're contributing to Context Rot:

1. **Never commit secrets or API keys**
2. **Use environment variables for sensitive data**
3. **Keep dependencies updated**
4. **Follow principle of least privilege**
5. **Test security features before deployment**

## Bug Bounty

We don't currently offer a formal bug bounty program, but we appreciate responsible disclosure and will acknowledge security researchers who help improve our security posture.

## Questions?

For questions about this security policy, contact: editor@context-rot.com

---

*Last updated: January 2025*