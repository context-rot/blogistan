#!/bin/bash

# Setup security tools for Context Rot development
set -e

echo "🔒 Setting up security tools for Context Rot..."

# Check if we're in the right directory
if [ ! -f "_config.yml" ] || [ ! -d ".github" ]; then
    echo "❌ Please run this script from the Context Rot repository root"
    exit 1
fi

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
else
    echo "✅ pre-commit already installed"
fi

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Install additional security tools
echo "🛡️ Installing security tools..."

# TruffleHog for secret detection
if ! command -v trufflehog &> /dev/null; then
    echo "📦 Installing TruffleHog..."
    # Install from GitHub releases
    curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
else
    echo "✅ TruffleHog already installed"
fi

# bundler-audit for Ruby dependency scanning
if command -v gem &> /dev/null; then
    echo "📦 Installing bundler-audit..."
    gem install bundler-audit
else
    echo "⚠️ Ruby not found, skipping bundler-audit installation"
fi

# Create git hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create a pre-push hook for additional security checks
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash

echo "🔍 Running security checks before push..."

# Check for secrets one more time
if command -v trufflehog &> /dev/null; then
    echo "Scanning for secrets..."
    trufflehog git file://. --since-commit HEAD~1 --only-verified --fail
fi

# Check for large files that might contain sensitive data
find . -name "*.key" -o -name "*.pem" -o -name "*.p12" | while read file; do
    if [ -f "$file" ]; then
        echo "⚠️ Found potential key file: $file"
        echo "Please ensure this is not a real private key!"
    fi
done

echo "✅ Security checks passed"
EOF

chmod +x .git/hooks/pre-push

# Initialize secrets baseline if it doesn't exist
if [ ! -f ".secrets.baseline" ]; then
    echo "🔧 Creating secrets baseline..."
    detect-secrets scan --baseline .secrets.baseline
fi

# Set up GitHub CLI if available
if command -v gh &> /dev/null; then
    echo "🐙 GitHub CLI detected - enabling additional security features..."
    
    # Enable security features on the repository
    echo "Enabling security features..."
    gh api repos/:owner/:repo --method PATCH --field security_and_analysis='{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}' 2>/dev/null || echo "⚠️ Could not enable all security features (may require admin access)"
fi

echo ""
echo "🎉 Security setup complete!"
echo ""
echo "📋 What was set up:"
echo "   ✅ Pre-commit hooks installed"
echo "   ✅ Security scanning tools configured"
echo "   ✅ Git hooks for additional protection"
echo "   ✅ Secrets baseline created"
echo ""
echo "🚨 Important reminders:"
echo "   • Never commit real API keys or secrets"
echo "   • Run 'pre-commit run --all-files' to test hooks"
echo "   • Update .secrets.baseline if you add legitimate secrets"
echo ""
echo "Happy secure coding! 🔒"