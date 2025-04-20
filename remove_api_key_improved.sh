#!/bin/bash

# Improved script to remove API keys from Git history
# This script uses a more robust approach than the previous one

# Set to exit on error
set -e

echo "=== Improved API Key Removal from Git History ==="
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

# Get the API key to remove
echo ""
echo "Enter the API key to remove from history (the actual key, not a pattern)."
echo "This will be replaced with a placeholder in all files."
echo ""
read -p "API key: " API_KEY

if [[ -z "$API_KEY" ]]; then
    echo "No API key provided. Operation cancelled."
    exit 1
fi

# Confirm the key
echo ""
echo "You entered: ${API_KEY:0:4}...${API_KEY: -4}"
read -p "Is this correct? (y/n): " key_confirm

if [[ $key_confirm != "y" && $key_confirm != "Y" ]]; then
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

# Create a temporary file with the API key
echo ""
echo "Setting up for API key removal..."
TEMP_FILE=$(mktemp)
echo "$API_KEY" > "$TEMP_FILE"

# Use BFG Repo-Cleaner if available, otherwise use git filter-repo
if command -v bfg &> /dev/null; then
    echo ""
    echo "BFG Repo-Cleaner found. Using BFG for API key removal..."
    bfg --replace-text "$TEMP_FILE" --no-blob-protection
elif command -v git-filter-repo &> /dev/null; then
    echo ""
    echo "git-filter-repo found. Using git-filter-repo for API key removal..."
    git filter-repo --force --replace-text <(echo "$API_KEY==>your-api-key-here")
else
    echo ""
    echo "Neither BFG nor git-filter-repo found. Using git filter-branch..."
    echo "Note: This method is less reliable and may fail on some repositories."
    echo ""
    echo "Creating a script to handle the replacement..."
    
    # Create a temporary script to handle the replacement
    REPLACE_SCRIPT=$(mktemp)
    cat > "$REPLACE_SCRIPT" << 'EOF'
#!/bin/bash
file="$1"
if [ -f "$file" ]; then
    # Use perl instead of sed for better cross-platform compatibility
    perl -i -pe "s/$2/your-api-key-here/g" "$file" 2>/dev/null || true
fi
EOF
    chmod +x "$REPLACE_SCRIPT"
    
    # Get a list of all files in the repository
    echo "Identifying files to process..."
    ALL_FILES=$(git ls-files)
    
    # Process each file individually to avoid errors with non-existent files
    echo "Setting up git filter-branch command..."
    FILTER_CMD="for file in $ALL_FILES; do \"$REPLACE_SCRIPT\" \"\$file\" \"$API_KEY\" || true; done"
    
    # Run git filter-branch
    echo "Running git filter-branch..."
    # Suppress the warning about filter-branch being deprecated
    export FILTER_BRANCH_SQUELCH_WARNING=1
    git filter-branch --force --tree-filter "$FILTER_CMD" --prune-empty --tag-name-filter cat -- --all
    
    # Clean up the temporary script
    rm "$REPLACE_SCRIPT"
fi

# Remove the temporary file with the API key
rm "$TEMP_FILE"

# Clean up
echo ""
echo "Cleaning up..."
rm -rf .git/refs/original/ || true
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
