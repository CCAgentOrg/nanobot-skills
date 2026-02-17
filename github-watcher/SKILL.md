---
name: github-watcher
description: Track and monitor GitHub repositories with latest release, version number, and star count. Fetch and summarize release notes for any repo. Use when the user wants to view a tabular summary of watched repos, add new repos to track, remove repos from the watchlist, or get release notes. WhatsApp format with emojis is default for chat channels (WhatsApp, Telegram, etc.). ASCII table format is used for terminal output.
---

# GitHub Watcher

Monitor GitHub repositories for latest releases, versions, and star counts. Fetch and summarize release notes for any repository.

## Quick Start

### List Watched Repositories

List all watched repos:
```
python scripts/list_repos.py
```

Force a specific format:
```
python scripts/list_repos.py ascii      # Terminal table format
python scripts/list_repos.py whatsapp   # WhatsApp/Telegram format with emojis
python scripts/list_repos.py markdown   # Markdown table format
```

### Manage Watched Repositories

Add a repo to watch:
```
python scripts/add_repo.py owner/repo
```

Remove a repo:
```
python scripts/remove_repo.py owner/repo
```

### Get Release Notes

Fetch and summarize the latest release notes:
```
python scripts/release_notes.py owner/repo
```

With format specification:
```
python scripts/release_notes.py owner/repo whatsapp   # WhatsApp format (default for chat)
python scripts/release_notes.py owner/repo terminal    # Terminal format
```

## Output Format

The skill automatically detects the environment and formats output accordingly:

### Chat Channels (WhatsApp, Telegram, etc.)
**WhatsApp format is default** - clean text layout with emojis:
- 📊 Repository cards with icons
- 🏷️ Version tags
- ⭐ Star counts
- Clean separation lines

### Terminal
ASCII table format with aligned columns.

You can force a specific format using the format argument.

## Commands

### `list_repos` - List Watched Repositories
Displays all watched repositories with their latest version and star count.

**Usage:**
```
python scripts/list_repos.py [format]
```

**Arguments:**
- `format` (optional): `auto` (default), `ascii`, `whatsapp`, `markdown`

**Examples:**
```
python scripts/list_repos.py
python scripts/list_repos.py whatsapp
python scripts/list_repos.py ascii
```

### `add_repo` - Add Repository to Watchlist
Add a repository to the watched list.

**Usage:**
```
python scripts/add_repo.py owner/repo
```

**Examples:**
```
python scripts/add_repo.py facebook/react
python scripts/add_repo.py python/cpython
```

### `remove_repo` - Remove Repository from Watchlist
Remove a repository from the watched list.

**Usage:**
```
python scripts/remove_repo.py owner/repo
```

**Examples:**
```
python scripts/remove_repo.py facebook/react
```

### `release_notes` - Get Latest Release Notes
Fetch and summarize the latest release notes for a specified repository.

**Usage:**
```
python scripts/release_notes.py owner/repo [format]
```

**Arguments:**
- `owner/repo`: Repository in owner/repo format (required)
- `format` (optional): `auto` (default), `whatsapp`, `terminal`

**Features:**
- Uses `gh` CLI first, falls back to GitHub REST API
- Automatically summarizes long release notes using the summarize skill
- Handles cases where no releases exist or repo is invalid
- Provides direct link to full release notes on GitHub

**Examples:**
```
python scripts/release_notes.py facebook/react
python scripts/release_notes.py vercel/next.js whatsapp
python scripts/release_notes.py python/cpython terminal
```

## Data Sources

The skill uses a dual fetch strategy:
1. **First**: Try `gh` CLI (faster, authenticated)
2. **Fallback**: GitHub REST API (no auth required, rate limited)

## Watched Repos List

The list of watched repos is stored in `assets/watched-repos.txt` (one repo per line). Edit this file directly or use the add/remove scripts.

## WhatsApp Format Examples

### List Repos Output
```
📊 *Watched Repositories*

━━━━━━━━━━━━━━━━━
📁 *facebook/react*
🏷️ Version: `18.3.1`
⭐ Stars: `220,000`

━━━━━━━━━━━━━━━━━
📁 *vercel/next.js*
🏷️ Version: `14.2.0`
⭐ Stars: `125,000`

_Total: 2 repo(s)_
```

### Release Notes Output
```
🚀 *Latest Release*
📁 `facebook/react`
━━━━━━━━━━━━━━━━━
🏷️ *Tag:* `18.3.1`
📛 *Name:* React 18.3.1
👤 *By:* @acdlite
📅 *Published:* 2024-06-10

📝 *Release Notes:*
━━━━━━━━━━━━━━━━━
📋 *Summary:*
This release includes bug fixes for React 18.3.0,
including improvements to useTransition and
concurrent rendering features.

🔗 *Full notes:*
## Bug Fixes
- Fixed issue with useTransition...

🔗 *View on GitHub:* https://github.com/facebook/react/releases/tag/18.3.1
```
