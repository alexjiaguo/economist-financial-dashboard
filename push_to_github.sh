#!/bin/bash
# Script to push Economist Dashboard to GitHub

echo "🚀 Economist Dashboard - GitHub Push Script"
echo "==========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository. Run 'git init' first."
    exit 1
fi

# Prompt for GitHub username
echo "📝 Please enter your GitHub username:"
read -p "Username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: Username cannot be empty."
    exit 1
fi

# Repository name
REPO_NAME="economist-financial-dashboard"

echo ""
echo "Repository URL will be:"
echo "https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "⚠️  IMPORTANT: Make sure you've created this repository on GitHub first!"
echo "   1. Go to: https://github.com/new"
echo "   2. Repository name: $REPO_NAME"
echo "   3. Do NOT initialize with README (we have one)"
echo "   4. Click 'Create repository'"
echo ""
read -p "Have you created the repository on GitHub? (y/n): " CREATED

if [ "$CREATED" != "y" ] && [ "$CREATED" != "Y" ]; then
    echo ""
    echo "Please create the repository first, then run this script again."
    echo "Repository name: $REPO_NAME"
    echo "URL: https://github.com/new"
    exit 0
fi

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo ""
    echo "⚠️  Remote 'origin' already exists. Removing and re-adding..."
    git remote remove origin
fi

# Add remote
echo ""
echo "📡 Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Check for changes
if ! git diff-index --quiet HEAD --; then
    echo ""
    echo "⚠️  You have uncommitted changes. Committing them first..."
    git add .
    git commit -m "Update before GitHub push"
fi

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
echo "   Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

# Try to push
if git push -u origin main 2>/dev/null; then
    echo ""
    echo "✅ SUCCESS! Your dashboard is now on GitHub!"
    echo ""
    echo "🔗 Repository URL:"
    echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "📊 View your dashboard:"
    echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "Next steps:"
    echo "   1. Add topics: financial-dashboard, forex, stock-market, python, flask"
    echo "   2. Star your repository"
    echo "   3. Share with the community!"
    echo ""
else
    echo ""
    echo "❌ Push failed. This might be because:"
    echo "   1. Repository doesn't exist on GitHub"
    echo "   2. You don't have permission"
    echo "   3. Authentication issue"
    echo ""
    echo "Solutions:"
    echo "   - Make sure the repository exists: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "   - Check your GitHub authentication (you may need a personal access token)"
    echo "   - Try: gh auth login (if you have GitHub CLI)"
    echo ""
    echo "Manual push command:"
    echo "   git push -u origin main"
    exit 1
fi

