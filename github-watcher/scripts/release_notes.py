#!/usr/bin/env python3
"""Fetch and summarize the latest release notes for a GitHub repository."""

import os
import sys
import json
import subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError

def fetch_gh_cli_release(repo):
    """Fetch latest release using gh CLI."""
    try:
        result = subprocess.run(
            ['gh', 'release', 'view', repo, '--json', 'tagName,name,body,publishedAt,author'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            return {
                'tag_name': data.get('tagName', ''),
                'name': data.get('name', ''),
                'body': data.get('body', ''),
                'published_at': data.get('publishedAt', ''),
                'author': data.get('author', {}).get('login', 'Unknown'),
                'source': 'gh'
            }
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError, Exception):
        pass
    return None

def fetch_github_api_release(repo):
    """Fetch latest release using GitHub REST API (fallback)."""
    owner, name = repo.split('/')

    try:
        req = Request(
            f"https://api.github.com/repos/{owner}/{name}/releases/latest",
            headers={'User-Agent': 'nanobot-github-watcher'}
        )
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                'tag_name': data.get('tag_name', ''),
                'name': data.get('name', ''),
                'body': data.get('body', ''),
                'published_at': data.get('published_at', ''),
                'author': data.get('author', {}).get('login', 'Unknown'),
                'source': 'api'
            }
    except URLError as e:
        if hasattr(e, 'code') and e.code == 404:
            # Release not found, check if repo exists
            try:
                req = Request(
                    f"https://api.github.com/repos/{owner}/{name}",
                    headers={'User-Agent': 'nanobot-github-watcher'}
                )
                with urlopen(req, timeout=10) as response:
                    # Repo exists but no releases
                    return {'error': 'no_releases', 'repo_exists': True}
            except URLError:
                # Repo not found
                return {'error': 'not_found', 'repo': repo}
        else:
            return {'error': 'api_error', 'message': str(e)}
    except Exception as e:
        return {'error': 'api_error', 'message': str(e)}

def fetch_latest_release(repo):
    """Fetch latest release with gh CLI fallback to GitHub API."""
    # Validate repo format
    if '/' not in repo or len(repo.split('/')) != 2:
        return {'error': 'invalid_repo', 'message': 'Invalid repo format. Use owner/repo'}

    # Try gh CLI first
    release = fetch_gh_cli_release(repo)
    if release:
        return release

    # Fall back to GitHub API
    release = fetch_github_api_release(repo)
    return release

def summarize_release(body, repo):
    """Extract bullet points from release notes to create a quick summary."""
    try:
        # Split body into lines
        lines = body.strip().split('\n')
        bullet_points = []

        # Look for bullet points (various formats)
        bullet_prefixes = ['* ', '- ', '• ', '•', '✓ ', '✅ ', '- ']

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this is a bullet point
            for prefix in bullet_prefixes:
                if line.startswith(prefix):
                    # Remove the prefix and clean up
                    point = line[len(prefix):].strip()
                    # Remove markdown formatting
                    point = point.replace('**', '').replace('*', '').replace('`', '')
                    # Limit length
                    if len(point) > 80:
                        point = point[:77] + '...'
                    if point:
                        bullet_points.append(point)
                    break

            # Stop if we have enough points
            if len(bullet_points) >= 8:
                break

        # If we found bullet points, format them
        if bullet_points:
            return '\n'.join([f'• {point}' for point in bullet_points[:8]])

    except Exception:
        pass

    return None

def format_whatsapp_release(repo, release):
    """Format release notes for WhatsApp/Telegram with emojis."""
    if 'error' in release:
        if release['error'] == 'invalid_repo':
            return "❌ *Invalid repo format*\n\nPlease use `owner/repo` format (e.g., `facebook/react`)"
        elif release['error'] == 'no_releases':
            return f"📭 *No releases found*\n\n`{repo}` exists but has no releases yet."
        elif release['error'] == 'not_found':
            return f"❌ *Repository not found*\n\n`{repo}` could not be found on GitHub."
        else:
            return f"❌ *Error fetching release*\n\n{release.get('message', 'Unknown error')}"

    # Format successful release
    tag_name = release['tag_name'] or 'Unknown'
    release_name = release['name'] or tag_name
    body = release['body'] or 'No release notes provided.'
    author = release['author']
    published_at = release['published_at'] or 'Unknown date'

    lines = [
        f"🚀 *Latest Release*",
        f"📁 `{repo}`",
        f"━━━━━━━━━━━━━━━━━",
        f"🏷️ *Tag:* `{tag_name}`",
        f"📛 *Name:* {release_name}",
        f"👤 *By:* @{author}",
        f"📅 *Published:* {published_at.split('T')[0] if 'T' in published_at else published_at}",
        f"",
        f"📝 *Release Notes:*",
        f"━━━━━━━━━━━━━━━━━",
    ]

    # Try to get summary
    summary = summarize_release(body, repo)
    if summary:
        lines.append(f"📋 *Summary:*")
        lines.append(summary)
        lines.append("")
        lines.append(f"🔗 *Full notes:*")
    else:
        lines.append("")

    # Add body (truncated if very long)
    max_body_length = 2000
    if len(body) > max_body_length:
        body = body[:max_body_length] + "\n\n...(truncated, visit GitHub for full notes)"

    lines.append(body)

    lines.append("")
    lines.append(f"🔗 *View on GitHub:* https://github.com/{repo}/releases/tag/{tag_name}")

    return "\n".join(lines)

def format_terminal_release(repo, release):
    """Format release notes for terminal output."""
    if 'error' in release:
        if release['error'] == 'invalid_repo':
            return f"Error: Invalid repo format. Use owner/repo"
        elif release['error'] == 'no_releases':
            return f"No releases found for {repo}"
        elif release['error'] == 'not_found':
            return f"Repository not found: {repo}"
        else:
            return f"Error: {release.get('message', 'Unknown error')}"

    tag_name = release['tag_name'] or 'Unknown'
    release_name = release['name'] or tag_name
    body = release['body'] or 'No release notes provided.'
    author = release['author']
    published_at = release['published_at'] or 'Unknown date'

    lines = [
        f"Latest Release for {repo}",
        f"=" * 50,
        f"Tag:     {tag_name}",
        f"Name:    {release_name}",
        f"Author:  @{author}",
        f"Date:    {published_at.split('T')[0] if 'T' in published_at else published_at}",
        f"",
        f"Release Notes:",
        f"-" * 50,
        ""
    ]

    # Try to get summary
    summary = summarize_release(body, repo)
    if summary:
        lines.append(f"Summary:")
        lines.append(summary)
        lines.append("")

    lines.append(body)
    lines.append("")
    lines.append(f"URL: https://github.com/{repo}/releases/tag/{tag_name}")

    return "\n".join(lines)

def get_release_notes(repo, format='auto'):
    """Get release notes for a repository."""
    if not repo:
        return "Error: No repository specified. Usage: release_notes.py owner/repo"

    release = fetch_latest_release(repo)

    # Format based on context
    if format == 'auto':
        if sys.stdout.isatty():
            return format_terminal_release(repo, release)
        else:
            return format_whatsapp_release(repo, release)
    elif format == 'whatsapp':
        return format_whatsapp_release(repo, release)
    elif format == 'terminal':
        return format_terminal_release(repo, release)
    else:
        return format_whatsapp_release(repo, release)

if __name__ == "__main__":
    format_type = 'auto'
    repo = None

    # Parse arguments
    if len(sys.argv) > 1:
        # Check if first arg is format or repo
        if sys.argv[1] in ['auto', 'whatsapp', 'terminal']:
            format_type = sys.argv[1]
            if len(sys.argv) > 2:
                repo = sys.argv[2]
        else:
            repo = sys.argv[1]
            if len(sys.argv) > 2:
                format_type = sys.argv[2]

    result = get_release_notes(repo, format_type)
    print(result)
