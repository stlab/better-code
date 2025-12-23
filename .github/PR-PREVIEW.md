# PR Preview System

This repository uses GitHub Pages for automated PR preview deployments without any third-party dependencies.

## How It Works

### Architecture

- **Production**: `gh-pages` branch root → https://stlab.github.io/better-code/
- **PR Previews**: `gh-pages` branch under `pr-preview/[NUMBER]/` → https://stlab.github.io/better-code/pr-preview/123/
- **Preview Index**: https://stlab.github.io/better-code/pr-preview/ (lists all active previews)

### Workflow

1. **Open PR** → Builds and deploys to `gh-pages:pr-preview/[PR-NUMBER]/`
2. **Push to PR** → Updates the preview deployment
3. **Close/Merge PR** → Automatically removes the preview directory
4. **Merge to main** → Deploys to production (root of gh-pages)

## Features

✅ **Automatic deployment** - No manual steps required  
✅ **PR comments** - Bot posts preview URL on every PR  
✅ **Automatic cleanup** - Previews removed when PR closes  
✅ **No third-party services** - Pure GitHub Pages  
✅ **Fast builds** - Only builds changed content  
✅ **Isolated environments** - Each PR gets its own subdirectory  

## File Structure on gh-pages Branch

```
gh-pages/
├── index.html              # Production site
├── chapter-1-intro.html
├── ...
└── pr-preview/
    ├── index.html         # List of all PR previews
    ├── 123/               # Preview for PR #123
    │   ├── index.html
    │   └── ...
    ├── 124/               # Preview for PR #124
    │   └── ...
    └── ...
```

## Configuration

### Required Permissions

The workflow requires these permissions (already configured):
- `contents: write` - To push to gh-pages branch
- `pages: write` - To deploy to GitHub Pages
- `pull-requests: write` - To comment on PRs

### GitHub Pages Settings

Ensure GitHub Pages is configured to deploy from the `gh-pages` branch:
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `root`

## Troubleshooting

### Preview not deploying

Check:
1. Workflow ran successfully in Actions tab
2. `gh-pages` branch exists and has the preview directory
3. GitHub Pages is enabled and set to deploy from `gh-pages` branch

### Preview URL 404

- Wait 1-2 minutes after deployment for GitHub Pages to update
- Check if the directory exists in the `gh-pages` branch
- Verify the PR number in the URL matches the directory name

### Old previews not cleaning up

- Check if the cleanup workflow ran when PR closed
- Manually remove with: `git checkout gh-pages && git rm -rf pr-preview/[NUMBER] && git commit && git push`

## Manual Cleanup

To manually remove all PR previews:

```bash
git checkout gh-pages
git rm -rf pr-preview/
git commit -m "Clean up all PR previews"
git push
```

To remove a specific preview:

```bash
git checkout gh-pages
git rm -rf pr-preview/123
git commit -m "Remove preview for PR #123"
git push
```

