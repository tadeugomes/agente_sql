#!/bin/bash

# Script to remove API keys from Git history
# This script uses git filter-branch to rewrite history

# Set to exit on error
set -e

echo "=== API Key Removal from Git History ==="
echo "This script will help remove API keys from your Git history."
echo "WARNING: This will rewrite your Git history. If you've already pushed to a remote repository,"
echo "you will need to force push after this operation, which can cause issues for collaborators."
echo ""
echo "Make sure you have:"
echo "1. Committed all current changes"
echo "2. Created a backup of your repository"
echo "3. Notified collaborators about this operation"
echo ""
read -p "Do you want to continue? (y/n): " confirm

if [[ $confirm != "y" && $confirm != "Y" ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Get the API key pattern to remove
echo ""
echo "Enter the API key pattern to remove from history."
echo "This should be a regex pattern that matches your API key."
echo "Example: If your API key is 'sk-abcd1234', you might use 'sk-[a-zA-Z0-9]{8,}'"
echo ""
read -p "API key pattern: " API_KEY_PATTERN

if [[ -z "$API_KEY_PATTERN" ]]; then
    echo "No pattern provided. Operation cancelled."
    exit 1
fi

# Confirm the pattern
echo ""
echo "You entered: $API_KEY_PATTERN"
read -p "Is this correct? (y/n): " pattern_confirm

if [[ $pattern_confirm != "y" && $pattern_confirm != "Y" ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Create a backup
echo ""
echo "Creating a backup of your repository..."
BACKUP_DIR="../$(basename $(pwd))_backup_$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r .git "$BACKUP_DIR"
echo "Backup created at: $BACKUP_DIR"

# Run git filter-branch to remove the API key
echo ""
echo "Removing API key from history..."
echo "This may take some time depending on the size of your repository."

# Filter the .env file
git filter-branch --force --index-filter \
    "git ls-files -z '*.env' | xargs -0 sed -i '' 's/$API_KEY_PATTERN/your-api-key-here/g'" \
    --prune-empty --tag-name-filter cat -- --all

# Filter Python files
git filter-branch --force --index-filter \
    "git ls-files -z '*.py' | xargs -0 sed -i '' 's/$API_KEY_PATTERN/your-api-key-here/g'" \
    --prune-empty --tag-name-filter cat -- --all

# Clean up
echo ""
echo "Cleaning up..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "Operation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Verify that the API key has been removed from the history"
echo "2. If you've already pushed to a remote repository, you'll need to force push:"
echo "   git push --force origin main"
echo "   (Replace 'main' with your branch name if different)"
echo ""
echo "IMPORTANT: If you're using this repository with collaborators,"
echo "make sure they are aware of this change and know how to handle it."
echo "They will need to clone the repository again or run:"
echo "git fetch --all"
echo "git reset --hard origin/main"
echo "(Replace 'main' with your branch name if different)"
