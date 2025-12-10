# How to Create a GitHub Repository from VSCode

## Method 1: Using VSCode's Built-in GitHub Integration (Easiest)

### Step 1: Open Source Control
1. Click on the **Source Control** icon in the left sidebar (looks like a branch icon)
2. Or press `Cmd+Shift+G` (Mac) or `Ctrl+Shift+G` (Windows/Linux)

### Step 2: Publish to GitHub
1. You should see a button that says **"Publish to GitHub"**
2. Click on it
3. VSCode will ask you to sign in to GitHub if you haven't already
4. Choose whether to make the repository **Public** or **Private**
5. Select the files you want to include (all should be selected by default)
6. Click **"Publish"**

That's it! Your repository is now on GitHub.

---

## Method 2: Using GitHub CLI (gh)

### Step 1: Install GitHub CLI
```bash
# On Mac (using Homebrew)
brew install gh

# On Windows (using winget)
winget install --id GitHub.cli

# On Linux
# See: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
```

### Step 2: Authenticate
```bash
gh auth login
```
Follow the prompts to authenticate with your GitHub account.

### Step 3: Create Repository
```bash
cd /Users/raivisbabris/Documents/ownai
gh repo create ai-image-generator --public --source=. --remote=origin --push
```

Options:
- `--public` - Make it public (use `--private` for private)
- `--source=.` - Use current directory
- `--remote=origin` - Set remote name
- `--push` - Push immediately

---

## Method 3: Manual GitHub Setup

### Step 1: Create Repository on GitHub.com
1. Go to https://github.com
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Fill in:
   - **Repository name**: `ai-image-generator`
   - **Description**: "AI Image Generator using Stable Diffusion"
   - Choose **Public** or **Private**
   - **DO NOT** initialize with README (we already have one)
5. Click **"Create repository"**

### Step 2: Connect Your Local Repository
GitHub will show you commands. Use these in your terminal:

```bash
cd /Users/raivisbabris/Documents/ownai
git remote add origin https://github.com/YOUR_USERNAME/ai-image-generator.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Verifying Your Repository

After publishing, you can:

1. **View on GitHub**: 
   - Go to `https://github.com/YOUR_USERNAME/ai-image-generator`

2. **Check Remote in VSCode**:
   ```bash
   git remote -v
   ```
   Should show:
   ```
   origin  https://github.com/YOUR_USERNAME/ai-image-generator.git (fetch)
   origin  https://github.com/YOUR_USERNAME/ai-image-generator.git (push)
   ```

3. **View in VSCode Source Control**:
   - Open Source Control panel
   - You should see "Sync Changes" button
   - Click to push/pull changes

---

## Making Future Changes

### After editing files:

1. **Stage Changes** (in VSCode Source Control):
   - Click the **"+"** icon next to changed files
   - Or click **"+"** next to "Changes" to stage all

2. **Commit**:
   - Type a commit message in the text box
   - Press `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows)

3. **Push to GitHub**:
   - Click the **"Sync Changes"** button
   - Or click the circular arrows icon in the status bar

### Or use terminal:
```bash
git add .
git commit -m "Your commit message"
git push
```

---

## Troubleshooting

### "Permission denied" error
**Solution**: Set up SSH keys or use Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### "Repository not found" error
**Solution**: Check the remote URL
```bash
git remote -v
```
Make sure it matches your GitHub username and repository name.

### Can't see "Publish to GitHub" button
**Solution**: 
1. Make sure you're signed in to GitHub in VSCode
2. Click on the account icon in the bottom left
3. Select "Sign in to GitHub"

---

## Recommended: Add Repository Description

After creating the repository, add a description on GitHub:

1. Go to your repository on GitHub
2. Click the **⚙️ Settings** icon (top right of repository)
3. Add description: "AI Image Generator using Stable Diffusion with Gradio web interface"
4. Add topics: `ai`, `stable-diffusion`, `image-generation`, `gradio`, `python`
5. Save changes

---

## Quick Reference

| Action | VSCode | Terminal |
|--------|--------|----------|
| View changes | Source Control panel | `git status` |
| Stage files | Click "+" | `git add .` |
| Commit | Type message + Cmd+Enter | `git commit -m "message"` |
| Push | Click "Sync Changes" | `git push` |
| Pull | Click "Sync Changes" | `git pull` |

---

**Need Help?**
- VSCode Git docs: https://code.visualstudio.com/docs/sourcecontrol/overview
- GitHub docs: https://docs.github.com/en/get-started
