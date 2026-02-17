"""
State management for lobster-py workflows.

Handles loading, saving, and resetting workflow state.
"""

import json
from pathlib import Path
from typing import Dict, Optional


class StateManager:
    """Manages workflow state persistence."""

    def __init__(self, workflow_id: str, state_dir: Path):
        """
        Initialize state manager.

        Args:
            workflow_id: Unique identifier for the workflow
            state_dir: Directory where state files are stored
        """
        self.workflow_id = workflow_id
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / f"{workflow_id}.json"

    def load(self) -> Dict:
        """
        Load workflow state from disk.

        Returns:
            State dictionary, or empty dict if no state exists
        """
        if not self.state_file.exists():
            return {}

        try:
            with open(self.state_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load state file: {e}")
            return {}

    def save(self, state: Dict) -> None:
        """
        Save workflow state to disk.

        Args:
            state: State dictionary to save
        """
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def reset(self) -> None:
        """Delete saved workflow state."""
        if self.state_file.exists():
            self.state_file.unlink()

    def exists(self) -> bool:
        """Check if saved state exists."""
        return self.state_file.exists()
