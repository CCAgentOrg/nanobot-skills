#!/usr/bin/env python3
"""List watched GitHub repositories with latest release, version, and star count."""

import os
import sys
import json
import subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError

# Path to watched repos file
WATCHED_REPOS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets",
    "watched-repos.txt"
)

def fetch_gh_cli(repo):
    """Fetch repo info using gh CLI."""
    try:
        # Try to get repo info with stargazer count and latest release
        result = subprocess.run(
            ['gh', 'repo', 'view', repo, '--json', 'stargazerCount,latestRelease,name,owner'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            stars = data.get('stargazerCount', 0)
            release = data.get('latestRelease')
            if release:
                version = release.get('tagName', 'N/A')
            else:
                version = 'No release'
            return {
                'stars': stars,
                'version': version,
                'source': 'gh'
            }
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError, Exception):
        pass
    return None

def fetch_github_api(repo):
    """Fetch repo info using GitHub REST API (fallback)."""
    owner, name = repo.split('/')

    stars = 0
    version = 'No release'

    try:
        # Fetch repo info (includes stargazer count)
        req = Request(
            f"https://api.github.com/repos/{owner}/{name}",
            headers={'User-Agent': 'nanobot-github-watcher'}
        )
        with urlopen(req, timeout=10) as response:
            repo_data = json.loads(response.read().decode())
            stars = repo_data.get('stargazers_count', 0)

        # Fetch latest release
        req = Request(
            f"https://api.github.com/repos/{owner}/{name}/releases/latest",
            headers={'User-Agent': 'nanobot-github-watcher'}
        )
        with urlopen(req, timeout=10) as response:
            release_data = json.loads(response.read().decode())
            version = release_data.get('tag_name', 'N/A')
    except URLError:
        version = 'No release'

    return {
        'stars': stars,
        'version': version,
        'source': 'api'
    }

def fetch_repo_info(repo):
    """Fetch repo info with gh CLI fallback to GitHub API."""
    # Try gh CLI first
    info = fetch_gh_cli(repo)
    if info:
        return info

    # Fall back to GitHub API
    info = fetch_github_api(repo)
    return info

def format_table_ascii(repos_data):
    """Format repos data as ASCII table (for terminal)."""
    if not repos_data:
        return "No repositories watched."

    # Calculate column widths
    max_repo = max(len(r) for r in repos_data.keys()) if repos_data else 20
    max_repo = max(max_repo, 10)

    header = f"{'Repository':<{max_repo}} | {'Version':^15} | {'Stars':>10}"
    separator = "-" * (len(header))

    lines = [header, separator]

    for repo, data in repos_data.items():
        stars_str = f"{data['stars']:,}" if isinstance(data['stars'], int) else str(data['stars'])
        lines.append(f"{repo:<{max_repo}} | {data['version']:^15} | {stars_str:>10}")

    return "\n".join(lines)

def format_whatsapp(repos_data):
    """Format repos data for WhatsApp/Telegram with emojis."""
    if not repos_data:
        return "📭 No repositories watched."

    lines = ["📊 *Watched Repositories*\n"]

    for repo, data in repos_data.items():
        stars_str = f"{data['stars']:,}" if isinstance(data['stars'], int) else str(data['stars'])
        version = data['version']
        version_emoji = "🏷️" if version != "No release" and version != "Error" else "❌"
        lines.append(f"━━━━━━━━━━━━━━━━━")
        lines.append(f"📁 *{repo}*")
        lines.append(f"{version_emoji} Version: `{version}`")
        lines.append(f"⭐ Stars: `{stars_str}`")
        lines.append("")

    lines.append(f"_Total: {len(repos_data)} repo(s)_")
    return "\n".join(lines)

def format_table_markdown(repos_data):
    """Format repos data as Markdown table (for chat)."""
    if not repos_data:
        return "No repositories watched."

    lines = [
        "| Repository | Version | Stars |",
        "|------------|---------|-------|"
    ]

    for repo, data in repos_data.items():
        stars_str = f"{data['stars']:,}" if isinstance(data['stars'], int) else str(data['stars'])
        lines.append(f"| {repo} | {data['version']} | {stars_str} |")

    return "\n".join(lines)

def list_repos(format='auto'):
    """List all watched repos with their info."""
    # Read repos
    try:
        with open(WATCHED_REPOS_FILE, "r") as f:
            repos = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        repos = []

    if not repos:
        return "No repositories watched. Add one with 'add owner/repo'"

    # Fetch info for each repo
    repos_data = {}
    for repo in repos:
        info = fetch_repo_info(repo)
        if info:
            repos_data[repo] = info
        else:
            repos_data[repo] = {'stars': 'N/A', 'version': 'Error', 'source': 'error'}

    # Format based on context
    if format == 'auto':
        # Try to detect if running in chat context
        # If stdout is a terminal, use ASCII; otherwise use WhatsApp
        if sys.stdout.isatty():
            table = format_table_ascii(repos_data)
        else:
            table = format_whatsapp(repos_data)
    elif format == 'ascii':
        table = format_table_ascii(repos_data)
    elif format == 'whatsapp':
        table = format_whatsapp(repos_data)
    elif format == 'markdown':
        table = format_table_markdown(repos_data)
    else:
        table = format_table_ascii(repos_data)

    return table

if __name__ == "__main__":
    format_type = 'auto'
    if len(sys.argv) > 1:
        format_type = sys.argv[1]

    print(list_repos(format=format_type))
