#!/usr/bin/env python3
"""
Digest Tracker Skill - Wrapper for the digest CLI
"""

import os
import sys
import subprocess


def main():
    # Pass all arguments to the digest CLI
    cmd = ["digest"] + sys.argv[1:]
    
    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Output the result
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
