#!/usr/bin/env python3
"""Remove a GitHub repository from the watched list."""

import os
import sys

# Path to watched repos file
WATCHED_REPOS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets",
    "watched-repos.txt"
)

def remove_repo(repo):
    """Remove a repo from the watched list."""
    try:
        with open(WATCHED_REPOS_FILE, "r") as f:
            repos = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return False, f"Watched list not found"

    if repo not in repos:
        return False, f"Repository {repo} not found in watched list"

    # Remove repo
    repos.remove(repo)

    # Write back
    with open(WATCHED_REPOS_FILE, "w") as f:
        f.write("\n".join(repos) + "\n")

    return True, f"Removed {repo} from watched list"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_repo.py <owner/repo>")
        sys.exit(1)

    repo = sys.argv[1]
    success, message = remove_repo(repo)
    print(message)
    sys.exit(0 if success else 1)
