#!/usr/bin/env python3
"""
Generate an HTML page listing all repositories in the OWASP GitHub organization.
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional
import urllib.request
import urllib.error


def fetch_participation_stats(owner: str, repo: str, token: str = None) -> Optional[List[int]]:
    """Fetch weekly commit participation stats for a repository (last 52 weeks)."""
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/participation"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "OWASP-Bumper-Repo-List-Generator"
    }
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 202:
                # Stats are being computed, return None
                return None
            data = json.loads(response.read().decode())
            # Return the 'all' array which contains commit counts for all contributors
            return data.get("all", [])
    except urllib.error.HTTPError as e:
        if e.code == 202:
            # Stats are being computed
            return None
        return None
    except Exception:
        return None


def fetch_repos(org: str, token: str = None) -> List[Dict]:
    """Fetch all repositories for a GitHub organization."""
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?per_page={per_page}&page={page}&sort=updated&direction=desc"
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "OWASP-Bumper-Repo-List-Generator"
        }
        
        if token:
            headers["Authorization"] = f"token {token}"
        
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                if not data:
                    break
                
                repos.extend(data)
                page += 1
                
                # Check if we've reached the last page
                if len(data) < per_page:
                    break
                    
        except urllib.error.HTTPError as e:
            print(f"Error fetching repositories: {e}", file=sys.stderr)
            print(f"Response: {e.read().decode()}", file=sys.stderr)
            sys.exit(1)
    
    return repos

def format_date(date_str: str) -> str:
    """Format ISO date string to a readable format."""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return date_str

def generate_html(repos: List[Dict], org: str) -> str:
    """Generate HTML page with repository listing."""
    
    # Prepare repository data as JSON for JavaScript
    repo_data = []
    for repo in repos:
        repo_data.append({
            "name": repo.get("name", ""),
            "full_name": repo.get("full_name", ""),
            "description": repo.get("description", "") or "",
            "html_url": repo.get("html_url", ""),
            "stargazers_count": repo.get("stargazers_count", 0),
            "forks_count": repo.get("forks_count", 0),
            "open_issues_count": repo.get("open_issues_count", 0),
            "updated_at": repo.get("updated_at", ""),
            "created_at": repo.get("created_at", ""),
            "language": repo.get("language", "") or "N/A",
            "archived": repo.get("archived", False),
            "is_project": "www-project" in repo.get("name", "").lower(),
            "is_chapter": "www-chapter" in repo.get("name", "").lower(),
            "sparkline": repo.get("sparkline", [])
        })
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{org} GitHub Repositories</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .subtitle {{
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        
        .controls {{
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 250px;
        }}
        
        input[type="text"] {{
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        
        input[type="text"]:focus {{
            outline: none;
            border-color: #3498db;
        }}
        
        .btn-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        button {{
            padding: 12px 20px;
            border: 2px solid #3498db;
            background: white;
            color: #3498db;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        button:hover {{
            background: #3498db;
            color: white;
        }}
        
        button.active {{
            background: #3498db;
            color: white;
        }}
        
        .checkbox-label {{
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            color: #3498db;
            cursor: pointer;
            user-select: none;
        }}
        
        .checkbox-label input[type="checkbox"] {{
            width: 16px;
            height: 16px;
            cursor: pointer;
        }}
        
        .sort-buttons {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }}
        
        .sort-btn {{
            padding: 6px 12px;
            border: 1px solid #95a5a6;
            background: white;
            color: #7f8c8d;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .sort-btn:hover {{
            border-color: #3498db;
            color: #3498db;
        }}
        
        .sort-btn.active {{
            background: #3498db;
            color: white;
            border-color: #3498db;
        }}
        
        .stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .stat {{
            padding: 10px 20px;
            background: #ecf0f1;
            border-radius: 6px;
            font-size: 14px;
        }}
        
        .stat strong {{
            color: #2c3e50;
            font-size: 18px;
        }}
        
        .stat.clickable {{
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .stat.clickable:hover {{
            background: #d5dbdb;
        }}
        
        .stat.clickable.active {{
            background: #3498db;
            color: white;
        }}
        
        .stat.clickable.active strong {{
            color: white;
        }}
        
        .stat.active-within-year {{
            border-left: 4px solid #27ae60;
        }}
        
        .stat.inactive-1yr {{
            border-left: 4px solid #e65100;
        }}
        
        .stat.inactive-3yr {{
            border-left: 4px solid #bf360c;
        }}
        
        .repo-list {{
            display: grid;
            gap: 15px;
        }}
        
        .repo-item {{
            padding: 20px;
            border: 1px solid #e1e8ed;
            border-radius: 6px;
            transition: all 0.3s;
            background: white;
        }}
        
        .repo-item:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        .repo-item.archived {{
            opacity: 0.7;
            background: #f9f9f9;
        }}
        
        .repo-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
            gap: 15px;
        }}
        
        .repo-name {{
            flex: 1;
        }}
        
        .repo-name a {{
            color: #2980b9;
            text-decoration: none;
            font-size: 18px;
            font-weight: 600;
            word-break: break-word;
        }}
        
        .repo-name a:hover {{
            text-decoration: underline;
        }}
        
        .repo-badges {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .badge {{
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            white-space: nowrap;
        }}
        
        .badge.project {{
            background: #e8f5e9;
            color: #2e7d32;
        }}
        
        .badge.chapter {{
            background: #e3f2fd;
            color: #1565c0;
        }}
        
        .badge.archived {{
            background: #ffebee;
            color: #c62828;
        }}
        
        .badge.language {{
            background: #f5f5f5;
            color: #666;
        }}
        
        .badge.inactive-1yr {{
            background: #fff3e0;
            color: #e65100;
        }}
        
        .badge.inactive-3yr {{
            background: #ffccbc;
            color: #bf360c;
        }}
        
        .bump-btn {{
            padding: 6px 12px;
            background: #ff9800;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: background 0.3s;
        }}
        
        .bump-btn:hover {{
            background: #f57c00;
        }}
        
        .bump-btn.archived {{
            background: #bdbdbd;
            cursor: not-allowed;
        }}
        
        .repo-description {{
            color: #666;
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        
        .repo-meta {{
            display: flex;
            gap: 20px;
            font-size: 13px;
            color: #7f8c8d;
            flex-wrap: wrap;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .meta-item::before {{
            content: "•";
            font-weight: bold;
        }}
        
        .meta-item:first-child::before {{
            content: "";
        }}
        
        .sparkline-container {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #f0f0f0;
        }}
        
        .sparkline-label {{
            font-size: 12px;
            color: #7f8c8d;
            white-space: nowrap;
        }}
        
        .sparkline {{
            stroke: #3498db;
            fill: none;
            stroke-width: 1.5;
        }}
        
        .sparkline-fill {{
            fill: rgba(52, 152, 219, 0.1);
            stroke: none;
        }}
        
        .repo-item.archived .sparkline {{
            stroke: #95a5a6;
        }}
        
        .repo-item.archived .sparkline-fill {{
            fill: rgba(149, 165, 166, 0.1);
        }}
        
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #7f8c8d;
            font-size: 18px;
        }}
        
        .loading {{
            text-align: center;
            padding: 40px;
            color: #3498db;
        }}
        
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e1e8ed;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .controls {{
                flex-direction: column;
            }}
            
            .search-box {{
                width: 100%;
            }}
            
            .btn-group {{
                width: 100%;
            }}
            
            button {{
                flex: 1;
            }}
            
            .sort-buttons {{
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{org} Repositories</h1>
        <div class="subtitle">Comprehensive listing of all GitHub repositories | <a href="https://github.com/OWASP-BLT/OWASP-Bumper" target="_blank" style="color: #3498db;">View on GitHub</a></div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search repositories by name or description...">
            </div>
            <div class="btn-group">
                <button id="filterAll" class="active" onclick="setFilter('all')">All</button>
                <button id="filterProject" onclick="setFilter('project')">Projects</button>
                <button id="filterChapter" onclick="setFilter('chapter')">Chapters</button>
            </div>
            <label class="checkbox-label">
                <input type="checkbox" id="hideArchived" checked onchange="toggleHideArchived()">
                Hide Archived
            </label>
        </div>
        
        <div class="sort-buttons">
            <button class="sort-btn active" data-sort="updated-desc">Updated ↓</button>
            <button class="sort-btn" data-sort="updated-asc">Updated ↑</button>
            <button class="sort-btn" data-sort="name-asc">Name A-Z</button>
            <button class="sort-btn" data-sort="name-desc">Name Z-A</button>
            <button class="sort-btn" data-sort="stars-desc">Stars ↓</button>
            <button class="sort-btn" data-sort="stars-asc">Stars ↑</button>
            <button class="sort-btn" data-sort="forks-desc">Forks ↓</button>
            <button class="sort-btn" data-sort="forks-asc">Forks ↑</button>
            <button class="sort-btn" data-sort="created-desc">Created ↓</button>
            <button class="sort-btn" data-sort="created-asc">Created ↑</button>
        </div>
        
        <div class="stats">
            <div class="stat">
                <strong id="totalCount">0</strong> Total Repositories
                (<strong id="activeReposCount">0</strong> active, <strong id="archivedReposCount">0</strong> archived)
            </div>
            <div class="stat">
                <strong id="visibleCount">0</strong> Visible
            </div>
            <div class="stat">
                <strong id="projectCount">0</strong> Projects
                (<strong id="activeProjectsCount">0</strong> active, <strong id="archivedProjectsCount">0</strong> archived)
            </div>
            <div class="stat">
                <strong id="chapterCount">0</strong> Chapters
                (<strong id="activeChaptersCount">0</strong> active, <strong id="archivedChaptersCount">0</strong> archived)
            </div>
        </div>
        
        <div class="stats">
            <div class="stat clickable active-within-year" id="filterActiveYear" onclick="setActivityFilter('within-year')">
                <strong id="activeYearCount">0</strong> Updated within 1 year
            </div>
            <div class="stat clickable inactive-1yr" id="filterInactive1yr" onclick="setActivityFilter('1yr-old')">
                <strong id="inactive1yrCount">0</strong> Older than 1 year
            </div>
            <div class="stat clickable inactive-3yr" id="filterInactive3yr" onclick="setActivityFilter('3yr-old')">
                <strong id="inactive3yrCount">0</strong> Older than 3 years
            </div>
        </div>
        
        <div id="repoList" class="repo-list"></div>
        
        <footer>
            Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC | Total: {len(repos)} repositories
        </footer>
    </div>
    
    <script>
        const repos = {json.dumps(repo_data, indent=8)};
        
        let currentFilter = 'all';
        let currentSort = 'updated-desc';
        let searchTerm = '';
        let activityFilter = 'all';
        let hideArchived = true;
        
        function formatDate(dateStr) {{
            if (!dateStr) return 'N/A';
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', {{ year: 'numeric', month: 'short', day: 'numeric' }});
        }}
        
        function getTimeAgo(dateStr) {{
            if (!dateStr) return '';
            const date = new Date(dateStr);
            const now = new Date();
            const diffMs = now - date;
            const diffSeconds = Math.floor(diffMs / 1000);
            const diffMinutes = Math.floor(diffSeconds / 60);
            const diffHours = Math.floor(diffMinutes / 60);
            const diffDays = Math.floor(diffHours / 24);
            const diffWeeks = Math.floor(diffDays / 7);
            const diffMonths = Math.floor(diffDays / 30);
            const diffYears = Math.floor(diffDays / 365);
            
            if (diffYears > 0) {{
                return diffYears === 1 ? '1 year ago' : `${{diffYears}} years ago`;
            }} else if (diffMonths > 0) {{
                return diffMonths === 1 ? '1 month ago' : `${{diffMonths}} months ago`;
            }} else if (diffWeeks > 0) {{
                return diffWeeks === 1 ? '1 week ago' : `${{diffWeeks}} weeks ago`;
            }} else if (diffDays > 0) {{
                return diffDays === 1 ? '1 day ago' : `${{diffDays}} days ago`;
            }} else if (diffHours > 0) {{
                return diffHours === 1 ? '1 hour ago' : `${{diffHours}} hours ago`;
            }} else if (diffMinutes > 0) {{
                return diffMinutes === 1 ? '1 minute ago' : `${{diffMinutes}} minutes ago`;
            }} else {{
                return 'just now';
            }}
        }}
        
        function getYearsSinceUpdate(dateStr) {{
            if (!dateStr) return 0;
            const lastUpdate = new Date(dateStr);
            const now = new Date();
            const diffTime = now - lastUpdate;
            const diffYears = diffTime / (1000 * 60 * 60 * 24 * 365.25);
            return diffYears;
        }}
        
        function generateSparklineSVG(data, width = 100, height = 20) {{
            if (!data || data.length === 0) {{
                return '<span class="sparkline-label" style="color: #bdc3c7;">No activity data</span>';
            }}
            
            const max = Math.max(...data, 1);
            const divisor = data.length > 1 ? data.length - 1 : 1;
            
            // Helper to calculate coordinates
            const getCoord = (value, index) => {{
                const x = (index / divisor) * width;
                const y = height - (value / max) * height;
                return `${{x.toFixed(1)}},${{y.toFixed(1)}}`;
            }};
            
            const points = data.map((value, index) => getCoord(value, index)).join(' ');
            
            // Create fill path (area under the line)
            const fillPoints = data.map((value, index) => getCoord(value, index));
            const fillPath = `M0,${{height}} L${{fillPoints.join(' L')}} L${{width}},${{height}} Z`;
            
            const totalCommits = data.reduce((a, b) => a + b, 0);
            const title = `${{totalCommits}} commits in the last 52 weeks`;
            
            return `<svg class="sparkline-svg" width="${{width}}" height="${{height}}" viewBox="0 0 ${{width}} ${{height}}" title="${{title}}">
                <title>${{title}}</title>
                <path class="sparkline-fill" d="${{fillPath}}"></path>
                <polyline class="sparkline" points="${{points}}"></polyline>
            </svg>`;
        }}
        
        function getBumpIssueUrl(repo) {{
            const title = encodeURIComponent('Repository Activity Reminder');
            const body = encodeURIComponent(
`Hello from the OWASP BLT team! 👋

We noticed that this repository hasn't seen much activity recently. We wanted to reach out to check on the status of this project.

**Please consider one of the following actions:**
- ✅ If this project is still active, please update it with any recent changes or a simple commit to show it's maintained
- 📦 If this project is no longer maintained, please consider archiving it to help keep the OWASP organization tidy
- 💬 If you need help or resources, please let us know in the comments

Thank you for contributing to the OWASP community!

---
*This issue was created via the [OWASP Bumper](https://github.com/OWASP-BLT/OWASP-Bumper) tool to help keep track of repository activity.*`
            );
            return `${{repo.html_url}}/issues/new?title=${{title}}&body=${{body}}`;
        }}
        
        function setFilter(filter) {{
            currentFilter = filter;
            
            // Update button states
            document.querySelectorAll('.btn-group button').forEach(btn => btn.classList.remove('active'));
            document.getElementById('filter' + filter.charAt(0).toUpperCase() + filter.slice(1)).classList.add('active');
            
            renderRepos();
        }}
        
        function setActivityFilter(filter) {{
            // Toggle filter - if clicking the same one, clear it
            if (activityFilter === filter) {{
                activityFilter = 'all';
            }} else {{
                activityFilter = filter;
            }}
            
            // Update button states
            document.querySelectorAll('.stat.clickable').forEach(stat => stat.classList.remove('active'));
            if (activityFilter !== 'all') {{
                if (activityFilter === 'within-year') {{
                    document.getElementById('filterActiveYear').classList.add('active');
                }} else if (activityFilter === '1yr-old') {{
                    document.getElementById('filterInactive1yr').classList.add('active');
                }} else if (activityFilter === '3yr-old') {{
                    document.getElementById('filterInactive3yr').classList.add('active');
                }}
            }}
            
            renderRepos();
        }}
        
        function toggleHideArchived() {{
            hideArchived = document.getElementById('hideArchived').checked;
            renderRepos();
        }}
        
        function sortRepos(repos, sortBy) {{
            const sorted = [...repos];
            
            switch(sortBy) {{
                case 'updated-desc':
                    sorted.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
                    break;
                case 'updated-asc':
                    sorted.sort((a, b) => new Date(a.updated_at) - new Date(b.updated_at));
                    break;
                case 'created-desc':
                    sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                    break;
                case 'created-asc':
                    sorted.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
                    break;
                case 'name-asc':
                    sorted.sort((a, b) => a.name.localeCompare(b.name));
                    break;
                case 'name-desc':
                    sorted.sort((a, b) => b.name.localeCompare(a.name));
                    break;
                case 'stars-desc':
                    sorted.sort((a, b) => b.stargazers_count - a.stargazers_count);
                    break;
                case 'stars-asc':
                    sorted.sort((a, b) => a.stargazers_count - b.stargazers_count);
                    break;
                case 'forks-desc':
                    sorted.sort((a, b) => b.forks_count - a.forks_count);
                    break;
                case 'forks-asc':
                    sorted.sort((a, b) => a.forks_count - b.forks_count);
                    break;
            }}
            
            return sorted;
        }}
        
        function filterRepos(repos) {{
            let filtered = repos;
            
            // Apply hide archived filter
            if (hideArchived) {{
                filtered = filtered.filter(repo => !repo.archived);
            }}
            
            // Apply filter
            if (currentFilter === 'project') {{
                filtered = filtered.filter(repo => repo.is_project);
            }} else if (currentFilter === 'chapter') {{
                filtered = filtered.filter(repo => repo.is_chapter);
            }}
            
            // Apply activity filter
            if (activityFilter === 'within-year') {{
                filtered = filtered.filter(repo => getYearsSinceUpdate(repo.updated_at) < 1);
            }} else if (activityFilter === '1yr-old') {{
                filtered = filtered.filter(repo => getYearsSinceUpdate(repo.updated_at) >= 1);
            }} else if (activityFilter === '3yr-old') {{
                filtered = filtered.filter(repo => getYearsSinceUpdate(repo.updated_at) >= 3);
            }}
            
            // Apply search
            if (searchTerm) {{
                const term = searchTerm.toLowerCase();
                filtered = filtered.filter(repo => 
                    repo.name.toLowerCase().includes(term) || 
                    repo.description.toLowerCase().includes(term)
                );
            }}
            
            return filtered;
        }}
        
        function renderRepos() {{
            const sorted = sortRepos(repos, currentSort);
            const filtered = filterRepos(sorted);
            
            const container = document.getElementById('repoList');
            
            if (filtered.length === 0) {{
                container.innerHTML = '<div class="no-results">No repositories match your criteria</div>';
                document.getElementById('visibleCount').textContent = '0';
                return;
            }}
            
            container.innerHTML = filtered.map(repo => {{
                const badges = [];
                const yearsSinceUpdate = getYearsSinceUpdate(repo.updated_at);
                
                if (repo.is_project) {{
                    badges.push('<span class="badge project">Project</span>');
                }}
                if (repo.is_chapter) {{
                    badges.push('<span class="badge chapter">Chapter</span>');
                }}
                if (repo.archived) {{
                    badges.push('<span class="badge archived">Archived</span>');
                }}
                if (repo.language) {{
                    badges.push(`<span class="badge language">${{repo.language}}</span>`);
                }}
                
                // Add activity indicator badges
                if (yearsSinceUpdate >= 3) {{
                    badges.push('<span class="badge inactive-3yr" title="No activity in 3+ years">3+ Years Inactive</span>');
                }} else if (yearsSinceUpdate >= 1) {{
                    badges.push('<span class="badge inactive-1yr" title="No activity in 1+ year">1+ Year Inactive</span>');
                }}
                
                // Only show bump button for repos not updated in over 1 year (and not archived)
                let bumpButton = '';
                if (yearsSinceUpdate >= 1) {{
                    bumpButton = repo.archived 
                        ? `<span class="bump-btn archived" title="Cannot bump archived repositories">🔔 Bump</span>`
                        : `<a href="${{getBumpIssueUrl(repo)}}" target="_blank" class="bump-btn" title="Create a reminder issue in this repository">🔔 Bump</a>`;
                }}
                
                // Generate sparkline
                const sparklineHtml = generateSparklineSVG(repo.sparkline, 120, 24);
                
                return `
                    <div class="repo-item ${{repo.archived ? 'archived' : ''}}">
                        <div class="repo-header">
                            <div class="repo-name">
                                <a href="${{repo.html_url}}" target="_blank">${{repo.name}}</a>
                            </div>
                            <div class="repo-badges">
                                ${{badges.join('')}}
                                ${{bumpButton}}
                            </div>
                        </div>
                        <div class="repo-description">${{repo.description || 'No description provided'}}</div>
                        <div class="repo-meta">
                            <span class="meta-item">⭐ ${{repo.stargazers_count}} stars</span>
                            <span class="meta-item">🔱 ${{repo.forks_count}} forks</span>
                            <span class="meta-item">📝 ${{repo.open_issues_count}} issues</span>
                            <span class="meta-item">📅 Updated: ${{formatDate(repo.updated_at)}} (${{getTimeAgo(repo.updated_at)}})</span>
                        </div>
                        <div class="sparkline-container">
                            <span class="sparkline-label">📈 Activity (52 weeks):</span>
                            ${{sparklineHtml}}
                        </div>
                    </div>
                `;
            }}).join('');
            
            document.getElementById('visibleCount').textContent = filtered.length;
        }}
        
        function updateStats() {{
            const totalRepos = repos.length;
            const archivedRepos = repos.filter(r => r.archived).length;
            const activeRepos = totalRepos - archivedRepos;
            
            const totalProjects = repos.filter(r => r.is_project).length;
            const archivedProjects = repos.filter(r => r.is_project && r.archived).length;
            const activeProjects = totalProjects - archivedProjects;
            
            const totalChapters = repos.filter(r => r.is_chapter).length;
            const archivedChapters = repos.filter(r => r.is_chapter && r.archived).length;
            const activeChapters = totalChapters - archivedChapters;
            
            // Activity-based counts
            const activeWithinYear = repos.filter(r => getYearsSinceUpdate(r.updated_at) < 1).length;
            const olderThan1Year = repos.filter(r => getYearsSinceUpdate(r.updated_at) >= 1).length;
            const olderThan3Years = repos.filter(r => getYearsSinceUpdate(r.updated_at) >= 3).length;
            
            document.getElementById('totalCount').textContent = totalRepos;
            document.getElementById('visibleCount').textContent = totalRepos;
            document.getElementById('activeReposCount').textContent = activeRepos;
            document.getElementById('archivedReposCount').textContent = archivedRepos;
            
            document.getElementById('projectCount').textContent = totalProjects;
            document.getElementById('activeProjectsCount').textContent = activeProjects;
            document.getElementById('archivedProjectsCount').textContent = archivedProjects;
            
            document.getElementById('chapterCount').textContent = totalChapters;
            document.getElementById('activeChaptersCount').textContent = activeChapters;
            document.getElementById('archivedChaptersCount').textContent = archivedChapters;
            
            // Update activity-based counts
            document.getElementById('activeYearCount').textContent = activeWithinYear;
            document.getElementById('inactive1yrCount').textContent = olderThan1Year;
            document.getElementById('inactive3yrCount').textContent = olderThan3Years;
        }}
        
        // Event listeners
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            searchTerm = e.target.value;
            renderRepos();
        }});
        
        // Sort button event listeners
        document.querySelectorAll('.sort-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                currentSort = e.target.dataset.sort;
                renderRepos();
            }});
        }});
        
        // Initial render
        updateStats();
        renderRepos();
    </script>
</body>
</html>
"""
    
    return html

def main():
    org = os.environ.get('GITHUB_ORG', 'owasp')
    token = os.environ.get('GITHUB_TOKEN', '')
    output_file = os.environ.get('OUTPUT_FILE', 'index.html')
    fetch_sparklines = os.environ.get('FETCH_SPARKLINES', 'true').lower() == 'true'
    
    print(f"Fetching repositories for organization: {org}")
    repos = fetch_repos(org, token)
    print(f"Found {len(repos)} repositories")
    
    # Fetch participation stats for sparklines (if enabled)
    if fetch_sparklines and token:
        print("Fetching activity sparklines for repositories...")
        total = len(repos)
        for i, repo in enumerate(repos):
            if (i + 1) % 50 == 0 or i == 0:
                print(f"  Fetching sparkline data: {i + 1}/{total}")
            
            owner = repo.get("owner", {}).get("login", org)
            repo_name = repo.get("name", "")
            
            if repo_name:
                sparkline_data = fetch_participation_stats(owner, repo_name, token)
                repo["sparkline"] = sparkline_data if sparkline_data else []
                
                # Small delay to avoid rate limiting
                if (i + 1) % 100 == 0:
                    time.sleep(1)
        
        print(f"  Completed fetching sparkline data for {total} repositories")
    else:
        print("Skipping sparkline data fetch (FETCH_SPARKLINES=false or no token)")
        for repo in repos:
            repo["sparkline"] = []
    
    print(f"Generating HTML page...")
    html = generate_html(repos, org.upper())
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML page generated: {output_file}")

if __name__ == "__main__":
    main()
