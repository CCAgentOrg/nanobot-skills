"""
Approval gate system for lobster-py.

Allows workflows to pause and wait for manual approval before proceeding.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime


class ApprovalGate:
    """Manages approval gates for workflow pauses."""

    def __init__(self, gate_config: Dict, workflow_id: str, state_dir: Path):
        """
        Initialize approval gate.

        Args:
            gate_config: Gate configuration from workflow
            workflow_id: Workflow identifier
            state_dir: Directory for gate state storage
        """
        self.config = gate_config
        self.workflow_id = workflow_id
        self.state_dir = Path(state_dir)
        self.gate_id = gate_config.get("id", "gate")
        self.gate_name = gate_config.get("name", self.gate_id)
        self.gate_file = self.state_dir / f"gate_{self.workflow_id}_{self.gate_id}.json"

        # Load or create gate state
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load gate state from disk."""
        if not self.gate_file.exists():
            return {
                "gate_id": self.gate_id,
                "workflow_id": self.workflow_id,
                "name": self.gate_name,
                "status": "pending",  # pending, approved, rejected
                "created_at": None,
                "approved_at": None,
                "approved_by": None,
                "reason": None
            }
        else:
            with open(self.gate_file, "r") as f:
                return json.load(f)

    def _save_state(self) -> None:
        """Save gate state to disk."""
        with open(self.gate_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def check_approved(self, step_id: str) -> bool:
        """
        Check if this gate has been approved.

        Args:
            step_id: The step ID this gate is associated with

        Returns:
            True if approved, False otherwise
        """
        # Initialize gate if first time seeing this step
        if self.state["created_at"] is None:
            self.state["created_at"] = datetime.now().isoformat()
            self.state["step_id"] = step_id
            self._save_state()
            return False

        return self.state["status"] == "approved"

    def approve(self, approved_by: str = "user", reason: Optional[str] = None) -> Dict:
        """
        Approve this gate.

        Args:
            approved_by: Identifier for who approved (user, agent name, etc.)
            reason: Optional reason for approval

        Returns:
            Updated gate state
        """
        self.state["status"] = "approved"
        self.state["approved_at"] = datetime.now().isoformat()
        self.state["approved_by"] = approved_by
        self.state["reason"] = reason
        self._save_state()

        print(f"✅ Gate '{self.gate_name}' approved by {approved_by}")
        return self.state

    def reject(self, reason: Optional[str] = None) -> Dict:
        """
        Reject this gate.

        Args:
            reason: Optional reason for rejection

        Returns:
            Updated gate state
        """
        self.state["status"] = "rejected"
        self.state["rejected_at"] = datetime.now().isoformat()
        self.state["reason"] = reason
        self._save_state()

        print(f"❌ Gate '{self.gate_name}' rejected: {reason or 'No reason provided'}")
        return self.state

    def reset(self) -> None:
        """Reset gate to pending state."""
        self.state = self._load_state()
        self.state["status"] = "pending"
        self.state["created_at"] = None
        self.state["approved_at"] = None
        self.state["approved_by"] = None
        self.state["rejected_at"] = None
        self.state["reason"] = None
        self._save_state()

    def get_status(self) -> Dict:
        """Get current gate status."""
        return self.state.copy()

    @classmethod
    def list_gates(cls, workflow_id: str, state_dir: Path) -> list:
        """
        List all gates for a workflow.

        Args:
            workflow_id: Workflow identifier
            state_dir: State directory

        Returns:
            List of gate states
        """
        state_dir = Path(state_dir)
        gates = []
        pattern = f"gate_{workflow_id}_*.json"

        for gate_file in state_dir.glob(pattern):
            with open(gate_file, "r") as f:
                gates.append(json.load(f))

        return gates
