"""
Workflow engine for lobster-py.

Handles workflow parsing, execution, and resumption from saved state.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from lobster.state import StateManager
from lobster.gate import ApprovalGate
from lobster.actions.core import ActionRegistry


class Workflow:
    """Main workflow engine class."""

    def __init__(self, workflow_path: str, state_dir: str = ".lobster"):
        """
        Initialize a workflow from a YAML or JSON file.

        Args:
            workflow_path: Path to workflow definition file
            state_dir: Directory for state persistence
        """
        self.workflow_path = Path(workflow_path)
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)

        # Load workflow definition
        self.definition = self._load_definition()
        self.workflow_id = self.definition.get("id", "workflow")
        self.description = self.definition.get("description", "")
        self.variables = self.definition.get("variables", {})

        # State management
        self.state_manager = StateManager(
            workflow_id=self.workflow_id,
            state_dir=self.state_dir
        )

        # Action registry
        self.actions = ActionRegistry()

        # Load or initialize state
        self.state = self.state_manager.load()

    def _load_definition(self) -> Dict:
        """Load workflow definition from YAML or JSON file."""
        content = self.workflow_path.read_text()

        if self.workflow_path.suffix in [".yml", ".yaml"]:
            return yaml.safe_load(content)
        elif self.workflow_path.suffix == ".json":
            return json.loads(content)
        else:
            raise ValueError(f"Unsupported file type: {self.workflow_path.suffix}")

    def run(self, resume: bool = False) -> Dict:
        """
        Execute the workflow.

        Args:
            resume: If True, resume from last saved state

        Returns:
            Final workflow state
        """
        if not resume:
            # Start fresh
            self.state = {
                "workflow_id": self.workflow_id,
                "status": "running",
                "started_at": datetime.now().isoformat(),
                "current_step": 0,
                "completed_steps": [],
                "variables": self.variables.copy(),
                "gate_states": {}
            }

        steps = self.definition.get("steps", [])
        start_index = self.state.get("current_step", 0) if resume else 0

        try:
            for i, step in enumerate(steps[start_index:], start=start_index):
                step_id = step.get("id", f"step_{i}")
                step_name = step.get("name", step_id)

                print(f"[Step {i+1}/{len(steps)}] {step_name}")

                # Check for approval gate
                if "gate" in step:
                    gate = ApprovalGate(step["gate"], self.workflow_id, self.state_dir)
                    if not gate.check_approved(step_id):
                        # Pause and wait for approval
                        self.state["status"] = "awaiting_approval"
                        self.state["current_step"] = i
                        self.state["paused_at"] = datetime.now().isoformat()
                        self.state_manager.save(self.state)
                        print(f"⏸️  Workflow paused at approval gate: {step['gate'].get('name', 'gate')}")
                        return self.state

                # Execute action
                result = self._execute_step(step)

                # Update state
                self.state["completed_steps"].append({
                    "step_id": step_id,
                    "name": step_name,
                    "completed_at": datetime.now().isoformat(),
                    "result": result
                })
                self.state["current_step"] = i + 1

                # Save state after each step
                self.state_manager.save(self.state)

            # Workflow complete
            self.state["status"] = "completed"
            self.state["completed_at"] = datetime.now().isoformat()
            self.state_manager.save(self.state)

            print(f"✅ Workflow completed successfully!")
            return self.state

        except Exception as e:
            self.state["status"] = "failed"
            self.state["error"] = str(e)
            self.state["failed_at"] = datetime.now().isoformat()
            self.state_manager.save(self.state)

            print(f"❌ Workflow failed: {e}")
            raise

    def _execute_step(self, step: Dict) -> Dict:
        """
        Execute a single workflow step.

        Args:
            step: Step definition from workflow

        Returns:
            Execution result
        """
        action_type = step.get("action", "echo")
        action_params = step.get("params", {})

        # Substitute variables
        action_params = self._substitute_variables(action_params)

        # Get and execute action
        action = self.actions.get_action(action_type)
        result = action.execute(**action_params)

        return result

    def _substitute_variables(self, params: Dict) -> Dict:
        """Replace variable placeholders with actual values."""
        if not isinstance(params, dict):
            return params

        result = {}
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                # Extract variable name
                var_name = value[2:-1]

                # Check in step variables, then workflow variables, then state variables
                if var_name in self.variables:
                    result[key] = self.variables[var_name]
                elif var_name in self.state.get("variables", {}):
                    result[key] = self.state["variables"][var_name]
                else:
                    # Keep original value if variable not found
                    result[key] = value
            elif isinstance(value, dict):
                result[key] = self._substitute_variables(value)
            elif isinstance(value, list):
                result[key] = [self._substitute_variables(item) if isinstance(item, dict) else item for item in value]
            else:
                result[key] = value

        return result

    def resume(self) -> Dict:
        """Resume workflow from saved state."""
        return self.run(resume=True)

    def status(self) -> Dict:
        """Get current workflow status."""
        return self.state

    def reset(self) -> None:
        """Reset workflow state to start fresh."""
        self.state_manager.reset()
        self.state = {}
