#!/usr/bin/env python3
"""Add a GitHub repository to the watched list."""

import os
import sys

# Path to watched repos file
WATCHED_REPOS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets",
    "watched-repos.txt"
)

def validate_repo(repo):
    """Validate repo format (owner/repo)."""
    if not repo:
        return False, "Repository cannot be empty"
    if "/" not in repo:
        return False, "Repository must be in 'owner/repo' format"
    parts = repo.split("/")
    if len(parts) != 2 or not all(parts):
        return False, "Repository must be in 'owner/repo' format"
    return True, ""

def add_repo(repo):
    """Add a repo to the watched list."""
    # Validate repo format
    is_valid, error = validate_repo(repo)
    if not is_valid:
        return False, error

    # Read existing repos
    try:
        with open(WATCHED_REPOS_FILE, "r") as f:
            repos = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        repos = []

    # Check if already exists
    if repo in repos:
        return False, f"Repository {repo} is already in the watched list"

    # Add repo
    repos.append(repo)

    # Write back
    os.makedirs(os.path.dirname(WATCHED_REPOS_FILE), exist_ok=True)
    with open(WATCHED_REPOS_FILE, "w") as f:
        f.write("\n".join(repos) + "\n")

    return True, f"Added {repo} to watched list"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python add_repo.py <owner/repo>")
        sys.exit(1)

    repo = sys.argv[1]
    success, message = add_repo(repo)
    print(message)
    sys.exit(0 if success else 1)
