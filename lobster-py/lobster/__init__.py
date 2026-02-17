"""
lobster-py: Python workflow engine for nanobot

A lightweight workflow system inspired by OpenClaw's Lobster.
Features:
- YAML/JSON workflow definitions
- Resumable execution with state persistence
- Approval gates for human intervention
- Built-in actions (shell, HTTP, echo, sleep)
"""

__version__ = "0.1.0"
__author__ = "nanobot"

from lobster.workflow import Workflow
from lobster.state import StateManager
from lobster.gate import ApprovalGate

__all__ = ["Workflow", "StateManager", "ApprovalGate"]
