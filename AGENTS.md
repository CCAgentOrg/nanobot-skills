# Agent Instructions for nanobot-skills

## Project Overview

nanobot-skills is a collection of modular skills that extend nanobot's capabilities. Each skill is a self-contained Python package with its own documentation, scripts, and assets.

Skills are designed to be:
- **Modular**: Each skill is independent and can be added/removed
- **Well-documented**: SKILL.md explains purpose, usage, and APIs
- **Testable**: Each skill can be tested independently
- **Reusable**: Skills can be shared and versioned

---

## Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.12+ | Runtime environment |
| **nanobot** | Latest | Skills framework |
| **gh CLI** | 2.86.0+ | GitHub operations (github-watcher) |
| **requests** | Latest | HTTP client (youtube-recommender) |
| **subprocess** | Built-in | Script execution |

---

## File Structure

```
nanobot-skills/
├── github-watcher/              # GitHub repository monitoring skill
│   ├── SKILL.md                # Skill documentation (required)
│   ├── scripts/                # Python scripts
│   │   ├── add_repo.py        # Add repo to watchlist
│   │   ├── list_repos.py      # List all watched repos
│   │   ├── release_notes.py   # Fetch and summarize releases
│   │   └── remove_repo.py     # Remove repo from watchlist
│   └── assets/                 # Skill data files
│       └── watched-repos.txt  # List of watched repositories
│
└── youtube-recommender/         # YouTube video recommendation skill
    ├── SKILL.md               # Skill documentation (required)
    └── youtube_recommender.py # Main recommendation logic
```

### File Conventions

| File | Purpose | Format |
|------|---------|--------|
| **SKILL.md** | Skill documentation (required) | Markdown |
| **scripts/*.py** | Executable scripts | Python 3.12+ |
| **assets/** | Skill-specific data | Text/JSON |

---

## Coding Standards

### Python Style

- **PEP 8 compliant**: Use 4 spaces, max 79 chars per line
- **Type hints**: Add type annotations for functions
- **Docstrings**: Google-style docstrings for all functions
- **Error handling**: Wrap external API calls in try/except
- **Logging**: Use `print()` for CLI output, no logging library

### Example Function

```python
def get_repo_info(owner: str, repo: str) -> dict:
    """Fetch repository information from GitHub API.
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
        
    Returns:
        dict: Repository metadata (stars, releases, etc.)
        
    Raises:
        subprocess.CalledProcessError: If gh CLI fails
    """
    result = subprocess.run(
        ['gh', 'repo', 'view', f'{owner}/{repo}', '--json', 'stargazerCount'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)
```

### Skill Conventions

1. **SKILL.md must include:**
   - Skill description
   - Usage examples
   - Available commands
   - Dependencies

2. **Scripts must be:**
   - Executable (`chmod +x scripts/*.py`)
   - Callable from command line
   - Handle `--help` argument

3. **Assets:**
   - Use simple text/JSON formats
   - One file per data type
   - Document format in SKILL.md

---

## Testing

### Manual Testing

Test each skill independently:

```bash
# Test github-watcher
cd skills/github-watcher/scripts
./add_repo.py owner/repo
./list_repos.py
./remove_repo.py owner/repo

# Test youtube-recommender
cd skills/youtube-recommender
python youtube_recommender.py "topic" --duration short
```

### Testing Checklist

- [ ] Script runs without errors
- [ ] Help text displays correctly
- [ ] Invalid input is handled gracefully
- [ ] External API failures are caught
- [ ] Output is formatted correctly

---

## Build/Run

### Development Workflow

```bash
# Clone repository
git clone https://github.com/CCAgentOrg/nanobot-skills.git

# Add new skill
mkdir skills/new-skill
cd skills/new-skill
# Create SKILL.md and scripts/

# Test skill
./scripts/my_script.py --help

# Commit changes
git add .
git commit -m "Add new skill: new-skill"
git push
```

### Installing Skills in nanobot

Skills are typically linked or copied to nanobot's workspace:

```bash
# Link skill to nanobot workspace
ln -s ~/nanobot-skills/skills/github-watcher \
  ~/.nanobot/workspace/skills/github-watcher

# Restart nanobot to load new skill
pm2 restart nanobot
```

---

## Deployment

### Version Control

All skills are version-controlled in the main repo.

### Publishing

1. Update version in SKILL.md
2. Tag release: `git tag v1.0.0`
3. Push: `git push --tags`

---

## Known Issues & Gotchas

| Issue | Solution |
|-------|----------|
| **gh CLI authentication** | Run `gh auth login` before using github-watcher |
| **YouTube API quota** | youtube-recommender uses Invidious as fallback |
| **Path issues** | Always use absolute paths or `__file__` for assets |
| **Permission errors** | Ensure scripts are executable: `chmod +x scripts/*.py` |

---

## Adding New Skills

### Step-by-Step

1. Create skill directory:
   ```bash
   mkdir skills/my-skill
   cd skills/my-skill
   ```

2. Create SKILL.md:
   ```markdown
   # My Skill
   
   Description of what this skill does.
   
   ## Usage
   
   ```bash
   ./scripts/my_script.py [args]
   ```
   ```

3. Create scripts:
   ```python
   #!/usr/bin/env python3
   import sys
   
   def main():
       print("Hello from my skill!")
   
   if __name__ == "__main__":
       main()
   ```

4. Make executable:
   ```bash
   chmod +x scripts/my_script.py
   ```

5. Test and commit.

---

## Contact & Support

- Repository: https://github.com/CCAgentOrg/nanobot-skills
- Issues: Use GitHub Issues
- Documentation: See each skill's SKILL.md
