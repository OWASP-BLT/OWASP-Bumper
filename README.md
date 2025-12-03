# OWASP-Bumper

## OWASP Repository List Generator

This repository contains a GitHub Action that automatically generates an HTML page listing all repositories in the OWASP GitHub organization.

### Features

- **Comprehensive Listing**: Displays all repositories with essential information including:
  - Repository name and description
  - Star count, fork count, open issues, and **open PRs**
  - Primary programming language
  - Last updated date
  - Archive status
  - **Activity sparkline** showing commit activity over the last 52 weeks
  - **Project metadata from index.md** (title, level, pitch, tags)
  
- **Smart Filtering**: Quick filter buttons to view:
  - All repositories
  - Projects only (repositories with "www-project" in the name)
  - Chapters only (repositories with "www-chapter" in the name)
  
- **Multiple Sorting Options**:
  - Updated date (default)
  - Name (alphabetical)
  - Stars
  - Forks
  - **PRs (open pull requests)**
  - **Issues**
  - **Level (OWASP project level from index.md)**
  - Created Date
  
- **Real-time Search**: Filter repositories by name, description, title, pitch, or tags

- **Compact Grid Layout**: Displays multiple repository cards per row for better overview

- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Usage

The GitHub Action runs automatically:
- **Daily** at 00:00 UTC
- **On push** to the main branch (when workflow or script files change)
- **Manually** via workflow dispatch

The generated HTML page is deployed to GitHub Pages and can be accessed at your repository's GitHub Pages URL.

### Manual Generation

To generate the HTML page locally:

```bash
python3 generate_repo_list.py
```

Environment variables:
- `GITHUB_TOKEN`: GitHub personal access token (optional, but recommended to avoid rate limits)
- `GITHUB_ORG`: GitHub organization name (default: "owasp")
- `OUTPUT_FILE`: Output HTML file name (default: "index.html")
- `FETCH_SPARKLINES`: Set to "true" to fetch activity data for sparklines (default: "true", requires `GITHUB_TOKEN`)
- `FETCH_METADATA`: Set to "true" to fetch index.md metadata and PR counts (default: "true", requires `GITHUB_TOKEN`)

Example:
```bash
export GITHUB_TOKEN=your_token_here
export GITHUB_ORG=owasp
export OUTPUT_FILE=repos.html
export FETCH_SPARKLINES=true
export FETCH_METADATA=true
python3 generate_repo_list.py
```

### Configuration

To use this action in your own repository:

1. Enable GitHub Pages in your repository settings
2. Set the Pages source to "GitHub Actions"
3. The workflow will automatically run and deploy the page

### Requirements

- Python 3.x (no additional dependencies required)
- GitHub Token with read access to organization repositories (automatically provided in GitHub Actions)
