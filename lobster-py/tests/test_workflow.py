"""
Unit tests for lobster-py workflow engine.
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from lobster.workflow import Workflow
from lobster.state import StateManager
from lobster.gate import ApprovalGate
from lobster.actions.core import ActionRegistry, EchoAction


class TestWorkflow(unittest.TestCase):
    """Test workflow loading and execution."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.workflow_file = Path(self.test_dir) / "test-workflow.yml"

        # Create test workflow
        self.workflow_file.write_text("""
id: test-workflow
name: Test Workflow
description: Workflow for testing

variables:
  test_var: "hello"

steps:
  - id: step1
    name: First step
    action: echo
    params:
      message: "${test_var} world"

  - id: step2
    name: Second step
    action: echo
    params:
      message: "test message 2"
""")

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_workflow_loading(self):
        """Test that workflow loads correctly."""
        workflow = Workflow(str(self.workflow_file), state_dir=self.test_dir)

        self.assertEqual(workflow.workflow_id, "test-workflow")
        self.assertEqual(workflow.description, "Workflow for testing")
        self.assertEqual(workflow.variables["test_var"], "hello")

    def test_workflow_execution(self):
        """Test that workflow executes all steps."""
        workflow = Workflow(str(self.workflow_file), state_dir=self.test_dir)

        result = workflow.run()

        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(result["completed_steps"]), 2)
        self.assertEqual(result["completed_steps"][0]["step_id"], "step1")
        self.assertEqual(result["completed_steps"][1]["step_id"], "step2")

    def test_variable_substitution(self):
        """Test that variables are substituted correctly."""
        workflow = Workflow(str(self.workflow_file), state_dir=self.test_dir)

        result = workflow.run()

        first_step = result["completed_steps"][0]
        self.assertIn("hello world", first_step["result"]["output"])


class TestStateManager(unittest.TestCase):
    """Test state management."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.state_manager = StateManager("test-workflow", self.test_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_and_load(self):
        """Test state persistence."""
        test_state = {"status": "running", "current_step": 2}

        self.state_manager.save(test_state)
        loaded = self.state_manager.load()

        self.assertEqual(loaded["status"], "running")
        self.assertEqual(loaded["current_step"], 2)

    def test_reset(self):
        """Test state reset."""
        test_state = {"status": "running", "current_step": 2}

        self.state_manager.save(test_state)
        self.state_manager.reset()

        loaded = self.state_manager.load()
        self.assertEqual(loaded, {})

    def test_exists(self):
        """Test state existence check."""
        self.assertFalse(self.state_manager.exists())

        self.state_manager.save({"status": "running"})
        self.assertTrue(self.state_manager.exists())


class TestApprovalGate(unittest.TestCase):
    """Test approval gate system."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        gate_config = {
            "id": "test-gate",
            "name": "Test Gate"
        }
        self.gate = ApprovalGate(gate_config, "test-workflow", self.test_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_initial_state(self):
        """Test initial gate state."""
        status = self.gate.get_status()
        self.assertEqual(status["status"], "pending")
        self.assertEqual(status["gate_id"], "test-gate")

    def test_check_approved_initially_false(self):
        """Test that gate is not approved initially."""
        self.assertFalse(self.gate.check_approved("step1"))

    def test_approve_gate(self):
        """Test gate approval."""
        self.gate.check_approved("step1")  # Initialize
        result = self.gate.approve("user", "Looks good")

        self.assertEqual(result["status"], "approved")
        self.assertEqual(result["approved_by"], "user")

    def test_reject_gate(self):
        """Test gate rejection."""
        self.gate.check_approved("step1")  # Initialize
        result = self.gate.reject("Not ready")

        self.assertEqual(result["status"], "rejected")

    def test_approved_after_approval(self):
        """Test that gate reports as approved after approval."""
        self.gate.check_approved("step1")
        self.assertFalse(self.gate.check_approved("step1"))

        self.gate.approve("user")
        self.assertTrue(self.gate.check_approved("step1"))

    def test_reset_gate(self):
        """Test gate reset."""
        self.gate.check_approved("step1")
        self.gate.approve("user")
        self.gate.reset()

        self.assertEqual(self.gate.state["status"], "pending")


class TestActions(unittest.TestCase):
    """Test action execution."""

    def test_echo_action(self):
        """Test echo action."""
        action = EchoAction()
        result = action.execute(message="test message")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["output"], "test message")

    def test_shell_action(self):
        """Test shell action."""
        from lobster.actions.core import ShellAction

        action = ShellAction()
        result = action.execute(command="echo 'hello world'")

        self.assertEqual(result["status"], "success")
        self.assertIn("hello world", result["output"])

    def test_sleep_action(self):
        """Test sleep action."""
        from lobster.actions.core import SleepAction

        action = SleepAction()
        result = action.execute(seconds=0)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duration"], 0)

    def test_action_registry(self):
        """Test action registry."""
        registry = ActionRegistry()

        self.assertIn("echo", registry.list_actions())
        self.assertIn("shell", registry.list_actions())

        echo_action = registry.get_action("echo")
        self.assertIsInstance(echo_action, EchoAction)

    def test_unknown_action(self):
        """Test unknown action raises error."""
        registry = ActionRegistry()

        with self.assertRaises(ValueError):
            registry.get_action("unknown_action")


if __name__ == "__main__":
    unittest.main()
