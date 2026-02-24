# Contributing to nanobot-skills

Thank you for your interest in contributing to nanobot-skills!

## Adding a New Skill

1. **Create the skill directory:**
   ```bash
   mkdir <skill-name>
   cd <skill-name>
   ```

2. **Create SKILL.md** (required):
   ```markdown
   # Skill Name
   
   Brief description of what this skill does.
   
   ## Usage
   
   ```bash
   ./scripts/my_script.py [args]
   ```
   
   ## Commands
   
   - `command1` - Description
   - `command2` - Description
   
   ## Dependencies
   
   List any external dependencies (CLI tools, APIs, etc.)
   ```

3. **Create scripts/** directory:
   ```bash
   mkdir scripts
   ```
   - Place Python scripts here
   - Make them executable: `chmod +x scripts/*.py`
   - Add `--help` support

4. **Create assets/** directory (optional):
   ```bash
   mkdir assets
   ```
   - Place data files here (JSON, text, etc.)

## Skill Structure

```
<skill-name>/
├── SKILL.md           # Required documentation
├── scripts/           # Python scripts
│   └── script.py
└── assets/            # Optional data files
    └── data.txt
```

## Coding Standards

### Python

- Use Python 3.12+ syntax
- Follow PEP 8 style guide
- Add type hints where appropriate
- Use Google-style docstrings
- Handle errors with try/except

### Example Script

```python
#!/usr/bin/env python3
"""Script description."""

import sys
import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("arg", help="Argument description")
    args = parser.parse_args()
    
    # Your logic here
    print(f"Hello: {args.arg}")


if __name__ == "__main__":
    main()
```

## Testing

1. Test your skill locally:
   ```bash
   ./scripts/your_script.py --help
   ./scripts/your_script.py arg1 arg2
   ```

2. Ensure SKILL.md exists and is complete

3. Verify scripts are executable

## Submitting Changes

1. Create a branch: `git checkout -b my-skill`
2. Commit changes: `git add . && git commit -m "Add my-skill"`
3. Push: `git push origin my-skill`
4. Open a pull request

## CI/CD

The repository uses GitHub Actions to validate:
- All skills have SKILL.md files
- Python scripts are syntactically valid
- README.md has required sections

## Questions?

Open an issue or start a discussion.
