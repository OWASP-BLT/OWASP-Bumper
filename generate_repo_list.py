#!/usr/bin/env python3
"""
Generate an HTML page listing all repositories in the OWASP GitHub organization.
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict
import urllib.request
import urllib.error

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
            "is_chapter": "www-chapter" in repo.get("name", "").lower()
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
        
        button, select {{
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
        
        button:hover, select:hover {{
            background: #3498db;
            color: white;
        }}
        
        button.active {{
            background: #3498db;
            color: white;
        }}
        
        select {{
            cursor: pointer;
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
            
            button, select {{
                flex: 1;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{org} Repositories</h1>
        <div class="subtitle">Comprehensive listing of all GitHub repositories</div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search repositories by name or description...">
            </div>
            <div class="btn-group">
                <select id="sortSelect">
                    <option value="updated-desc">Sort by: Updated (Newest)</option>
                    <option value="updated-asc">Sort by: Updated (Oldest)</option>
                    <option value="name-asc">Sort by: Name (A-Z)</option>
                    <option value="name-desc">Sort by: Name (Z-A)</option>
                    <option value="stars-desc">Sort by: Stars (Most)</option>
                    <option value="stars-asc">Sort by: Stars (Fewest)</option>
                    <option value="forks-desc">Sort by: Forks (Most)</option>
                    <option value="forks-asc">Sort by: Forks (Fewest)</option>
                    <option value="created-desc">Sort by: Created (Newest)</option>
                    <option value="created-asc">Sort by: Created (Oldest)</option>
                </select>
                <button id="filterAll" class="active" onclick="setFilter('all')">All</button>
                <button id="filterProject" onclick="setFilter('project')">Projects</button>
                <button id="filterChapter" onclick="setFilter('chapter')">Chapters</button>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat">
                <strong id="totalCount">0</strong> Total Repositories
            </div>
            <div class="stat">
                <strong id="visibleCount">0</strong> Visible
            </div>
            <div class="stat">
                <strong id="projectCount">0</strong> Projects
            </div>
            <div class="stat">
                <strong id="chapterCount">0</strong> Chapters
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
        
        function formatDate(dateStr) {{
            if (!dateStr) return 'N/A';
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', {{ year: 'numeric', month: 'short', day: 'numeric' }});
        }}
        
        function setFilter(filter) {{
            currentFilter = filter;
            
            // Update button states
            document.querySelectorAll('.btn-group button').forEach(btn => btn.classList.remove('active'));
            document.getElementById('filter' + filter.charAt(0).toUpperCase() + filter.slice(1)).classList.add('active');
            
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
            
            // Apply filter
            if (currentFilter === 'project') {{
                filtered = filtered.filter(repo => repo.is_project);
            }} else if (currentFilter === 'chapter') {{
                filtered = filtered.filter(repo => repo.is_chapter);
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
                
                return `
                    <div class="repo-item ${{repo.archived ? 'archived' : ''}}">
                        <div class="repo-header">
                            <div class="repo-name">
                                <a href="${{repo.html_url}}" target="_blank">${{repo.name}}</a>
                            </div>
                            <div class="repo-badges">
                                ${{badges.join('')}}
                            </div>
                        </div>
                        <div class="repo-description">${{repo.description || 'No description provided'}}</div>
                        <div class="repo-meta">
                            <span class="meta-item">⭐ ${{repo.stargazers_count}} stars</span>
                            <span class="meta-item">🔱 ${{repo.forks_count}} forks</span>
                            <span class="meta-item">📝 ${{repo.open_issues_count}} issues</span>
                            <span class="meta-item">📅 Updated: ${{formatDate(repo.updated_at)}}</span>
                        </div>
                    </div>
                `;
            }}).join('');
            
            document.getElementById('visibleCount').textContent = filtered.length;
        }}
        
        function updateStats() {{
            document.getElementById('totalCount').textContent = repos.length;
            document.getElementById('visibleCount').textContent = repos.length;
            document.getElementById('projectCount').textContent = repos.filter(r => r.is_project).length;
            document.getElementById('chapterCount').textContent = repos.filter(r => r.is_chapter).length;
        }}
        
        // Event listeners
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            searchTerm = e.target.value;
            renderRepos();
        }});
        
        document.getElementById('sortSelect').addEventListener('change', (e) => {{
            currentSort = e.target.value;
            renderRepos();
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
    
    print(f"Fetching repositories for organization: {org}")
    repos = fetch_repos(org, token)
    print(f"Found {len(repos)} repositories")
    
    print(f"Generating HTML page...")
    html = generate_html(repos, org.upper())
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML page generated: {output_file}")

if __name__ == "__main__":
    main()
