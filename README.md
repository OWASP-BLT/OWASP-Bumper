# 🚀 OWASP-Bumper

<div align="center">

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/OWASP-BLT/OWASP-Bumper/generate-repo-list.yml?branch=main&style=for-the-badge&logo=github&label=Build)
![Python Version](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/github/license/OWASP-BLT/OWASP-Bumper?style=for-the-badge)
![GitHub Stars](https://img.shields.io/github/stars/OWASP-BLT/OWASP-Bumper?style=for-the-badge&logo=github)
![GitHub Forks](https://img.shields.io/github/forks/OWASP-BLT/OWASP-Bumper?style=for-the-badge&logo=github)
![GitHub Issues](https://img.shields.io/github/issues/OWASP-BLT/OWASP-Bumper?style=for-the-badge&logo=github)
![Last Commit](https://img.shields.io/github/last-commit/OWASP-BLT/OWASP-Bumper?style=for-the-badge&logo=git&logoColor=white)
![Repo Size](https://img.shields.io/github/repo-size/OWASP-BLT/OWASP-Bumper?style=for-the-badge)
![Lines of Code](https://img.shields.io/tokei/lines/github/OWASP-BLT/OWASP-Bumper?style=for-the-badge)

### 📊 Automated OWASP Repository Dashboard Generator

*Your one-stop solution for tracking, monitoring, and visualizing all OWASP GitHub repositories with beautiful sparklines and comprehensive metadata!*

[🌐 View Live Demo](https://owasp-blt.github.io/OWASP-Bumper/) • [📖 Documentation](SETUP.md) • [🐛 Report Bug](https://github.com/OWASP-BLT/OWASP-Bumper/issues) • [✨ Request Feature](https://github.com/OWASP-BLT/OWASP-Bumper/issues)

</div>

---

## 🎯 What is OWASP-Bumper?

OWASP-Bumper is an **intelligent GitHub Action-powered tool** that automatically generates a comprehensive, interactive HTML dashboard displaying all repositories in the OWASP GitHub organization. It provides deep insights into repository activity, health, and metadata - all updated daily without any manual intervention!

Perfect for organization administrators, project leaders, and contributors who need to:
- 🔍 **Monitor** repository activity across the entire OWASP ecosystem
- 📈 **Visualize** commit patterns with 52-week activity sparklines
- 🏷️ **Categorize** projects and chapters at a glance
- 🔔 **Track** inactive repositories that need attention
- 📊 **Analyze** project health metrics (stars, forks, issues, PRs)

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 📋 Comprehensive Repository Data

- 🎯 **Repository Metrics**: Name, description, stars, forks, issues, PRs
- 💻 **Technology Stack**: Primary programming language detection
- 📅 **Temporal Data**: Created & last updated timestamps
- 🗄️ **Archive Status**: Clear indication of archived repositories
- 📈 **Activity Sparklines**: Beautiful 52-week commit activity visualization
- 📝 **Project Metadata**: Parses YAML frontmatter from `index.md` files
  - Project title & pitch
  - OWASP maturity level (1-4)
  - Tags & categories
  - Regional information for chapters

</td>
<td width="50%">

### 🎛️ Smart Filtering & Navigation

- 🔍 **Real-time Search**: Filter by name, description, title, pitch, or tags
- 🏷️ **Category Filters**: Projects, Chapters, or All repositories
- 🗃️ **Archive Toggle**: Show/hide archived repositories
- ⏰ **Activity Filters**: Active, inactive 1yr+, inactive 3yr+
- 🔽 **Multi-dimensional Sorting**: Sort by:
  - 📅 Updated/Created date (ascending/descending)
  - 📛 Name (A-Z or Z-A)
  - ⭐ Stars, 🔱 Forks, 📝 Issues, 🔀 PRs
  - 📊 Activity score or 🏆 OWASP level

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Modern User Interface

- 📱 **Responsive Design**: Flawless on desktop, tablet, and mobile
- 🎴 **Compact Grid Layout**: Multiple cards per row for better overview
- 🎯 **Visual Badges**: Quick identification of project type, level, and status
- 🔔 **Bump Button**: One-click reminder issue creation for inactive repos
- ⚡ **Fast Rendering**: Efficient client-side rendering with vanilla JavaScript
- 🎭 **XSS Protection**: All user content properly escaped

</td>
<td width="50%">

### 🤖 Automated Workflows

- ⏰ **Daily Updates**: Automatically runs at 00:00 UTC
- 🚀 **Auto-deployment**: Pushes to GitHub Pages automatically
- 🔄 **Manual Triggers**: Run on-demand via workflow dispatch
- 🔐 **Secure**: Uses GitHub's built-in authentication
- 🌐 **Zero Dependencies**: No external libraries required
- 📊 **Efficient**: Batched API calls with rate limit handling

</td>
</tr>
</table>

## 🏗️ Technical Architecture

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions Trigger                       │
│            (Daily at 00:00 UTC or Manual/Push)                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Python Script (generate_repo_list.py)              │
│                                                                  │
│  1. Fetch all repos via GitHub API                             │
│     └─> GET /orgs/{org}/repos (paginated)                      │
│                                                                  │
│  2. Enrich with metadata (parallel requests):                   │
│     ├─> Fetch index.md (YAML frontmatter parsing)             │
│     ├─> Fetch open PR counts                                   │
│     └─> Fetch 52-week commit stats (/stats/participation)      │
│                                                                  │
│  3. Generate static HTML with embedded data                     │
│     └─> JSON array embedded in JavaScript                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Commit & Push to Main                        │
│              (index.html updated automatically)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               Deploy to GitHub Pages                            │
│          (Accessible at username.github.io/repo)                │
└─────────────────────────────────────────────────────────────────┘
```

### 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.11+ | Repository data fetching and HTML generation |
| **CI/CD** | GitHub Actions | Automated daily runs and deployment |
| **Hosting** | GitHub Pages | Free, fast, and reliable static hosting |
| **Frontend** | Vanilla JS/HTML/CSS | Zero-dependency interactive dashboard |
| **API** | GitHub REST API v3 | Repository data and statistics |
| **Styling** | Custom CSS3 | Modern, responsive design with Flexbox/Grid |

### 📦 Zero External Dependencies

One of the most powerful aspects of OWASP-Bumper is its **zero-dependency architecture**:

- ✅ **Python**: Uses only the standard library (`urllib`, `json`, `base64`, etc.)
- ✅ **JavaScript**: Pure vanilla JS - no jQuery, React, or Vue needed
- ✅ **CSS**: Handcrafted responsive styles without Bootstrap or Tailwind
- ✅ **Deployment**: Native GitHub Actions - no third-party services

**Why this matters:**
- 🚀 Faster execution (no dependency installation time)
- 🔒 More secure (no supply chain vulnerabilities)
- 🎯 Easier maintenance (no version conflicts)
- 💰 Cost-effective (runs in seconds, not minutes)

### 🎨 Frontend Architecture

The generated HTML page uses a **modern client-side rendering** approach:

1. **Data Embedding**: All repository data is embedded as a JSON array in the HTML
2. **Dynamic Rendering**: JavaScript generates DOM elements on the fly
3. **Efficient Filtering**: Client-side filtering and sorting for instant results
4. **SVG Sparklines**: Commit activity charts generated programmatically
5. **XSS Protection**: All user content sanitized through `escapeHtml()` function

### 📊 API Rate Limiting & Optimization

The script intelligently handles GitHub's API rate limits:

| Feature | Rate Limit Impact | Optimization Strategy |
|---------|------------------|----------------------|
| Basic repo fetch | ~10 requests | Paginated fetching (100 per page) |
| Sparkline data | 1 request per repo | Batched with 1s delay per 100 repos |
| index.md fetch | 1 request per repo | Optional (can be disabled) |
| PR counts | 1 request per repo | Optional (can be disabled) |

**Rate Limit Tiers:**
- 🔓 **Unauthenticated**: 60 requests/hour (not recommended)
- 🔐 **Authenticated**: 5,000 requests/hour (used by default in Actions)
- ⚡ **GitHub Actions**: Special higher limits for workflows

**Pro Tips:**
- Set `FETCH_SPARKLINES=false` to reduce API calls by ~N (N = number of repos)
- Set `FETCH_METADATA=false` to reduce API calls by ~2N
- Local testing benefits from using `GITHUB_TOKEN` environment variable

## 🚀 Quick Start

### 📥 For OWASP Organization (Default)

The workflow is **already configured** and runs automatically! Just watch it work:

1. ⏰ Wait for the daily run at 00:00 UTC, or
2. 🖱️ Trigger manually:
   - Go to **Actions** tab
   - Select **"Generate OWASP Repository List"**
   - Click **"Run workflow"**

3. 🌐 View the results at: [https://owasp-blt.github.io/OWASP-Bumper/](https://owasp-blt.github.io/OWASP-Bumper/)

### 🔄 For Your Own Organization

Want to use this for your own GitHub organization? Easy!

1. **Fork this repository** 
2. **Enable GitHub Pages**:
   - Go to **Settings** → **Pages**
   - Set source to **GitHub Actions**
3. **Configure the organization**:
   - Edit `.github/workflows/generate-repo-list.yml`
   - Change `GITHUB_ORG: owasp` to your organization name
4. **Run the workflow** and enjoy your dashboard!

📖 See [SETUP.md](SETUP.md) for detailed instructions.

## 💻 Local Development & Testing

### Basic Usage

```bash
# Clone the repository
git clone https://github.com/OWASP-BLT/OWASP-Bumper.git
cd OWASP-Bumper

# Run with default settings (OWASP organization)
python3 generate_repo_list.py

# Open the generated page
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

### 🔐 With Authentication (Recommended)

Using a GitHub token avoids rate limits and enables all features:

```bash
# Create a Personal Access Token at: https://github.com/settings/tokens
# Required scope: public_repo (or repo for private repos)

export GITHUB_TOKEN=ghp_your_token_here
python3 generate_repo_list.py
```

### ⚙️ Environment Variables

Customize behavior with these environment variables:

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `GITHUB_ORG` | `owasp` | Target GitHub organization | `export GITHUB_ORG=microsoft` |
| `GITHUB_TOKEN` | _(none)_ | GitHub Personal Access Token | `export GITHUB_TOKEN=ghp_xxx` |
| `OUTPUT_FILE` | `index.html` | Output HTML filename | `export OUTPUT_FILE=repos.html` |
| `FETCH_SPARKLINES` | `true` | Enable 52-week activity charts | `export FETCH_SPARKLINES=false` |
| `FETCH_METADATA` | `true` | Enable index.md parsing & PR counts | `export FETCH_METADATA=false` |

### 🎯 Advanced Examples

```bash
# Fetch only basic data (fast, minimal API calls)
export GITHUB_TOKEN=ghp_xxx
export GITHUB_ORG=owasp
export FETCH_SPARKLINES=false
export FETCH_METADATA=false
python3 generate_repo_list.py

# Generate for a different organization with all features
export GITHUB_TOKEN=ghp_xxx
export GITHUB_ORG=microsoft
export OUTPUT_FILE=microsoft_repos.html
python3 generate_repo_list.py

# Test without authentication (limited to small orgs due to rate limits)
export GITHUB_ORG=your-small-org
export FETCH_SPARKLINES=false
export FETCH_METADATA=false
python3 generate_repo_list.py
```

## 🛠️ Configuration & Customization

### 📅 Changing Update Schedule

Edit `.github/workflows/generate-repo-list.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
    # Other examples:
    # - cron: '0 0 * * 1'   # Weekly (every Monday)
    # - cron: '0 0 1 * *'   # Monthly (1st of month)
```

### 🎨 Customizing the UI

The HTML generation is in `generate_repo_list.py`, in the `generate_html()` function:
- **Styles**: Embedded CSS starting at line ~268
- **Layout**: HTML structure starting at line ~262
- **JavaScript**: Client-side logic starting at line ~956

### 🔧 Extending Functionality

Want to add more features? Here are some ideas:

- **Add more badges**: Modify the badge generation in `generate_html()`
- **New sorting options**: Add cases to the `sortRepos()` JS function
- **Custom filters**: Extend the `filterRepos()` JS function
- **Additional metadata**: Fetch more data in the main script and embed it in JSON

## 📖 Project Structure

```
OWASP-Bumper/
├── 📄 generate_repo_list.py    # Main Python script (generates HTML)
├── 📄 index.html               # Generated output (auto-generated)
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 generate-repo-list.yml   # GitHub Actions workflow
├── 📄 README.md                # This file
├── 📄 SETUP.md                 # Detailed setup instructions
└── 📄 .gitignore               # Git ignore patterns
```

### 📄 Key Files Explained

**`generate_repo_list.py`** (1,453 lines)
- Fetches all repos from GitHub API with pagination
- Enriches data with sparklines, metadata, and PR counts
- Generates a complete, self-contained HTML file
- Uses only Python standard library

**`.github/workflows/generate-repo-list.yml`**
- Defines automated workflow triggers (daily/manual/push)
- Sets up Python environment
- Runs the generation script
- Commits and deploys to GitHub Pages

**`index.html`** (auto-generated)
- Complete single-page application
- Embedded JSON data array
- Vanilla JavaScript for interactivity
- Responsive CSS for all screen sizes

## 🎓 Use Cases

### 🏢 For Organization Administrators

- 📊 **Monitor** the health of all repositories at a glance
- 🔍 **Identify** inactive projects that need attention or archiving
- 📈 **Track** commit activity trends across the organization
- 🏷️ **Categorize** and organize projects and chapters
- 📢 **Report** on organization activity to stakeholders

### 👨‍💻 For Project Maintainers

- 🔎 **Discover** related projects within OWASP
- 🌟 **Compare** your project's stars, forks, and activity
- 🔀 **Monitor** open PRs and issues across projects
- 🏆 **Track** OWASP maturity levels
- 🤝 **Find** potential collaborators and similar projects

### 📚 For Contributors

- 🆕 **Find** new projects to contribute to
- 🔥 **Identify** active vs. inactive projects
- 📊 **Analyze** project health before contributing
- 🏷️ **Filter** by technology stack (programming language)
- 🌍 **Locate** local chapters by region/country

## 🤝 Contributing

We ❤️ contributions! Here's how you can help:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. ✍️ **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. 📤 **Push** to the branch (`git push origin feature/amazing-feature`)
5. 🎉 **Open** a Pull Request

### 💡 Ideas for Contributions

- 🎨 UI/UX improvements
- 📊 New sorting or filtering options
- 🌐 Internationalization (i18n)
- 📈 Additional chart types or visualizations
- 🔔 Better notification/reminder systems
- 📝 Documentation improvements
- 🐛 Bug fixes and performance optimizations
- ✨ New features or integrations

## 📊 Performance Metrics

Typical execution times for the OWASP organization (~400 repositories):

| Operation | Time | API Calls |
|-----------|------|-----------|
| Fetch repository list | ~5s | ~4 requests |
| Fetch sparklines | ~60s | ~400 requests |
| Fetch metadata | ~60s | ~800 requests |
| Generate HTML | ~1s | 0 requests |
| **Total** | **~2 minutes** | **~1,204 requests** |

With optimizations (sparklines & metadata disabled): **~6 seconds total**

## 🔒 Security

- ✅ All user-generated content is escaped to prevent XSS attacks
- ✅ Uses GitHub's built-in `GITHUB_TOKEN` (no secrets needed)
- ✅ No external dependencies = no supply chain vulnerabilities
- ✅ Read-only API operations (no write permissions needed)
- ✅ Static HTML output (no server-side execution)

## 📜 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

## 🙏 Acknowledgments

- 🌟 Built for the [OWASP](https://owasp.org) community
- 💙 Powered by [GitHub Actions](https://github.com/features/actions)
- 🎨 Inspired by GitHub's own repository insights
- 🚀 Part of the [OWASP BLT](https://github.com/OWASP-BLT) ecosystem

## 📞 Support & Contact

- 🐛 **Bug Reports**: [Open an issue](https://github.com/OWASP-BLT/OWASP-Bumper/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/OWASP-BLT/OWASP-Bumper/discussions)
- 📧 **Email**: Contact the OWASP BLT team
- 🌐 **Website**: [OWASP BLT Project](https://owasp.org/www-project-bug-logging-tool/)

---

<div align="center">

**Made with ❤️ by the OWASP BLT Team**

⭐ Star us on GitHub if you find this useful! ⭐

[🏠 Homepage](https://github.com/OWASP-BLT/OWASP-Bumper) • [📖 Docs](SETUP.md) • [🐛 Issues](https://github.com/OWASP-BLT/OWASP-Bumper/issues) • [🤝 Contribute](https://github.com/OWASP-BLT/OWASP-Bumper/pulls)

</div>
