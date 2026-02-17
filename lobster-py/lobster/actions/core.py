"""
Core action implementations for lobster-py workflows.

Includes: echo, shell, sleep, and extensible action system.
"""

import subprocess
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class Action(ABC):
    """Base class for workflow actions."""

    @abstractmethod
    def execute(self, **kwargs) -> Dict:
        """
        Execute the action.

        Args:
            **kwargs: Action-specific parameters

        Returns:
            Execution result dictionary
        """
        pass


class EchoAction(Action):
    """Echo/print message action."""

    def execute(self, message: str = "", **kwargs) -> Dict:
        """
        Print a message to console.

        Args:
            message: Message to print
            **kwargs: Additional parameters (ignored)

        Returns:
            Result dictionary
        """
        print(message)
        return {
            "status": "success",
            "output": message
        }


class ShellAction(Action):
    """Execute shell command action."""

    def execute(self, command: str, capture_output: bool = True, **kwargs) -> Dict:
        """
        Execute a shell command.

        Args:
            command: Shell command to execute
            capture_output: Whether to capture stdout/stderr
            **kwargs: Additional parameters (ignored)

        Returns:
            Result dictionary with status and output
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture_output,
                text=True
            )

            if result.returncode == 0:
                return {
                    "status": "success",
                    "return_code": result.returncode,
                    "output": result.stdout if capture_output else "",
                    "error": result.stderr if capture_output else ""
                }
            else:
                return {
                    "status": "failed",
                    "return_code": result.returncode,
                    "output": result.stdout if capture_output else "",
                    "error": result.stderr if capture_output else ""
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


class SleepAction(Action):
    """Sleep/pause action."""

    def execute(self, seconds: int = 1, **kwargs) -> Dict:
        """
        Pause execution for specified duration.

        Args:
            seconds: Number of seconds to sleep
            **kwargs: Additional parameters (ignored)

        Returns:
            Result dictionary
        """
        print(f"Sleeping for {seconds} seconds...")
        time.sleep(seconds)
        return {
            "status": "success",
            "duration": seconds
        }


class HttpAction(Action):
    """HTTP request action (basic implementation)."""

    def execute(self, url: str, method: str = "GET", **kwargs) -> Dict:
        """
        Make an HTTP request.

        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional parameters (headers, data, etc.)

        Returns:
            Result dictionary with status and response
        """
        try:
            import requests
        except ImportError:
            return {
                "status": "error",
                "error": "requests library not installed. Install with: pip install requests"
            }

        try:
            method = method.upper()
            headers = kwargs.get("headers", {})
            data = kwargs.get("data", None)
            json_data = kwargs.get("json", None)

            response = requests.request(
                method,
                url,
                headers=headers,
                data=data,
                json=json_data
            )

            return {
                "status": "success",
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "text": response.text
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


class ManualApprovalAction(Action):
    """Manual approval action (simpler alternative to gates)."""

    def execute(self, prompt: str = "Please confirm to continue", **kwargs) -> Dict:
        """
        Prompt for manual approval.

        Args:
            prompt: Message to display to user
            **kwargs: Additional parameters (ignored)

        Returns:
            Result dictionary
        """
        print(f"\n⏸️  {prompt}")
        print("Press Enter to continue, or Ctrl+C to cancel...")

        try:
            input()
            return {
                "status": "approved",
                "prompt": prompt
            }
        except KeyboardInterrupt:
            return {
                "status": "cancelled",
                "prompt": prompt
            }


class SetVariableAction(Action):
    """Set/update workflow variable action."""

    def execute(self, name: str, value: Any, **kwargs) -> Dict:
        """
        Set a workflow variable.

        Args:
            name: Variable name
            value: Variable value
            **kwargs: Additional parameters (ignored)

        Returns:
            Result dictionary
        """
        return {
            "status": "success",
            "variable": name,
            "value": value
        }


class ActionRegistry:
    """Registry for available actions."""

    def __init__(self):
        """Initialize with built-in actions."""
        self.actions: Dict[str, Action] = {
            "echo": EchoAction(),
            "shell": ShellAction(),
            "sleep": SleepAction(),
            "http": HttpAction(),
            "manual_approval": ManualApprovalAction(),
            "set_variable": SetVariableAction(),
        }

    def get_action(self, action_type: str) -> Action:
        """
        Get an action instance by type.

        Args:
            action_type: Type of action

        Returns:
            Action instance

        Raises:
            ValueError: If action type not found
        """
        if action_type not in self.actions:
            raise ValueError(f"Unknown action type: {action_type}. Available: {list(self.actions.keys())}")

        return self.actions[action_type]

    def register_action(self, action_type: str, action: Action) -> None:
        """
        Register a custom action.

        Args:
            action_type: Type identifier for the action
            action: Action instance to register
        """
        self.actions[action_type] = action

    def list_actions(self) -> List[str]:
        """List all registered action types."""
        return list(self.actions.keys())
