# GitHub Top 100 Repositories

A static GitHub Pages site listing the top 100 GitHub repositories by star count. Data is refreshed daily at 02:00 UTC via GitHub Actions.

**Live site:** `https://<your-username>.github.io/github-top100/`

## Features

- Sortable columns: rank, name, stars, forks, language, last push
- Real-time search/filter by name, description, or language
- Dark / light mode (auto-detects system preference, persists per browser)
- Responsive layout

## Setup

### 1. Fork or clone this repo to your GitHub account

### 2. Create a GitHub Personal Access Token (PAT)

Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens → Generate new token.

- **Resource owner:** your account
- **Repository access:** Public Repositories (read-only)
- **Permissions:** No additional permissions needed — the Search API is public
- Set an expiration (90 or 365 days) and note the renewal date

### 3. Add the PAT as a repository secret

Go to your repo → Settings → Secrets and variables → Actions → New repository secret:

- **Name:** `GH_PAT`
- **Value:** your PAT string

### 4. Run the workflow manually (first time)

Go to Actions → "Update Top 100 Repos" → Run workflow.

This creates the `gh-pages` branch with the generated `index.html`.

### 5. Enable GitHub Pages

Go to repo Settings → Pages → Source → Deploy from a branch → Branch: `gh-pages` → Folder: `/ (root)` → Save.

Your site will be live at `https://<your-username>.github.io/github-top100/` within a minute.

## How it works

| Component | Description |
|---|---|
| `scripts/fetch_repos.py` | Calls the GitHub Search API, extracts top 100 repos, injects JSON into the HTML template |
| `templates/index.template.html` | Single-file HTML/CSS/JS site with a `/*__REPO_DATA__*/` placeholder |
| `.github/workflows/update-top100.yml` | Daily cron at 02:00 UTC; runs the script, pushes generated `index.html` to `gh-pages` |

## Local development

```bash
pip install -r requirements.txt
export GITHUB_TOKEN=<your-pat>
python scripts/fetch_repos.py --output index.html
# open index.html in a browser
```

## Rotating the PAT

When your PAT expires, generate a new one and update the `GH_PAT` repository secret. No code changes required.
