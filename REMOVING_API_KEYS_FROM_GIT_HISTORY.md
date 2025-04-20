# Removing API Keys from Git History

This guide provides instructions on how to remove sensitive information like API keys from your Git history.

## Option 1: Using the Provided Script (Recommended for Most Users)

We've created a script that automates the process of removing API keys from your Git history using `git filter-branch`.

### Prerequisites

- Bash shell (comes with macOS and Linux, use Git Bash on Windows)
- Git installed
- All current changes committed

### Steps

1. Make sure you have committed all current changes
2. Create a backup of your repository (the script will do this automatically)
3. Run the script:
   ```bash
   ./remove_api_key_from_history.sh
   ```
4. Follow the prompts in the script:
   - Confirm you want to proceed
   - Enter the pattern that matches your API key
   - Confirm the pattern is correct
5. The script will:
   - Create a backup of your repository
   - Remove the API key from all .env and .py files in your history
   - Clean up the repository
6. After the script completes, force push to your remote repository:
   ```bash
   git push --force origin main
   ```
   (Replace 'main' with your branch name if different)

## Option 2: Using BFG Repo-Cleaner (For Larger Repositories)

For larger repositories, the BFG Repo-Cleaner is more efficient than `git filter-branch`.

### Prerequisites

- Java installed
- Download BFG Repo-Cleaner from https://rtyley.github.io/bfg-repo-cleaner/

### Steps

1. Create a text file containing your API key pattern, e.g., `api-keys.txt`:
   ```
   your-actual-api-key-here
   ```

2. Run BFG to replace the API key with "***REMOVED***":
   ```bash
   java -jar bfg.jar --replace-text api-keys.txt your-repo.git
   ```

3. Change into your repository and clean up:
   ```bash
   cd your-repo.git
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```

4. Force push to your remote repository:
   ```bash
   git push --force origin main
   ```

## Option 3: Using git-filter-repo (For Advanced Users)

`git-filter-repo` is a more powerful and efficient alternative to `git filter-branch`.

### Prerequisites

- Python 3 installed
- Install git-filter-repo: `pip install git-filter-repo`

### Steps

1. Create a Python script to define the replacements, e.g., `remove_keys.py`:
   ```python
   import re
   
   def replace_api_keys(text):
       # Replace OpenAI API keys (adjust pattern as needed)
       text = re.sub(r'sk-[a-zA-Z0-9]{48}', 'your-api-key-here', text)
       return text
   ```

2. Run git-filter-repo:
   ```bash
   git-filter-repo --force --blob-callback "blob.data = replace_api_keys(blob.data)"
   ```

3. Force push to your remote repository:
   ```bash
   git push --force origin main
   ```

## Important Notes for All Methods

1. **Rewriting Git history is destructive**. Make sure you have a backup before proceeding.

2. **Force pushing can cause issues for collaborators**. They will need to:
   - Clone the repository again, or
   - Run:
     ```bash
     git fetch --all
     git reset --hard origin/main
     ```

3. **Revoke and rotate your API keys**. Even after removing them from Git history, consider them compromised and generate new ones.

4. **Update your local .env file** with your new API keys after the operation.

5. **GitHub's secret scanning may still show the alert** for a while after you've removed the secret. This is normal and should eventually clear up.

## Preventing Future Leaks

1. **Use environment variables** and `.env` files (already implemented in your project)
2. **Add sensitive files to .gitignore** (already done for `.env` files)
3. **Consider using a pre-commit hook** to prevent committing sensitive information
4. **Use a secret scanning tool** in your development workflow

For more information, refer to the `API_KEY_SECURITY.md` file in this repository.
