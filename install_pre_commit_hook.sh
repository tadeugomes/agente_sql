#!/bin/bash

# Script to install the pre-commit hook for API key detection

echo "Installing pre-commit hook for API key detection..."

# Check if .git directory exists
if [ ! -d ".git" ]; then
    echo "❌ Error: .git directory not found. Make sure you're in the root of a Git repository."
    exit 1
fi

# Check if hooks directory exists, create if not
if [ ! -d ".git/hooks" ]; then
    echo "Creating hooks directory..."
    mkdir -p .git/hooks
fi

# Check if pre-commit hook already exists
if [ -f ".git/hooks/pre-commit" ]; then
    echo "⚠️ A pre-commit hook already exists."
    read -p "Do you want to overwrite it? (y/n): " overwrite
    if [[ $overwrite != "y" && $overwrite != "Y" ]]; then
        echo "Operation cancelled."
        exit 0
    fi
fi

# Copy the pre-commit hook
cp .git/hooks/pre-commit .git/hooks/pre-commit.bak 2>/dev/null || :
cp .git/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed successfully!"
echo "This hook will check for potential API keys in your commits."
echo "If you need to bypass the check for a specific commit, use: git commit --no-verify"
