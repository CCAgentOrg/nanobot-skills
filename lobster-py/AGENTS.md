# AGENTS.md

 lobster-py - Coding Agent Integration Guide

This document helps AI coding agents (OpenCode, Claude Code, Cline, etc.) understand and work with lobster-py.

---

## Project Overview

**lobster-py** is a Python workflow engine for nanobot, inspired by OpenClaw's Lobster system. It enables:

- **YAML/JSON workflow definitions** - Declarative workflow configuration
- **Resumable execution** - State persistence for long-running workflows
- **Approval gates** - Pause workflows for manual approval
- **Built-in actions** - echo, shell, sleep, http, manual_approval, set_variable
- **Variable substitution** - `${variable}` syntax throughout workflows

---

## Project Structure

```
lobster-py/
├── lobster/
│   ├── __init__.py           # Package exports
│   ├── workflow.py           # Main Workflow class
│   ├── state.py              # StateManager for persistence
│   ├── gate.py               # ApprovalGate system
│   └── actions/
│       ├── __init__.py       # Action exports
│       └── core.py           # Built-in actions
├── examples/
│   └── basic-workflow.yml    # Example workflow
├── tests/
│   └── test_workflow.py      # Unit tests (17 tests)
├── SKILL.md                  # Skill documentation for nanobot
└── AGENTS.md                 # This file
```

---

## Core Components

### 1. Workflow (`lobster/workflow.py`)

Main class that loads and executes workflows.

**Key methods:**
- `Workflow(workflow_path, state_dir)` - Initialize from YAML/JSON file
- `run(resume=False)` - Execute workflow (optionally resume from state)
- `resume()` - Alias for `run(resume=True)`
- `status()` - Get current workflow state
- `reset()` - Clear workflow state

---

### 2. StateManager (`lobster/state.py`)

Handles JSON-based state persistence.

**Key methods:**
- `load()` - Load state from disk
- `save(state)` - Save state to disk
- `reset()` - Delete saved state
- `exists()` - Check if state exists

**State file location:** `{state_dir}/{workflow_id}.json`

---

### 3. ApprovalGate (`lobster/gate.py`)

Manages approval gates for workflow pauses.

**Key methods:**
- `check_approved(step_id)` - Check if gate is approved
- `approve(approved_by, reason)` - Approve the gate
- `reject(reason)` - Reject the gate
- `reset()` - Reset gate to pending
- `get_status()` - Get gate status

**Gate file location:** `{state_dir}/gate_{workflow_id}_{gate_id}.json`

---

### 4. Actions (`lobster/actions/core.py`)

Built-in actions for workflow steps.

**Available actions:**

| Action | Params | Description |
|--------|--------|-------------|
| `echo` | `message` | Print message to console |
| `shell` | `command`, `capture_output` | Execute shell command |
| `sleep` | `seconds` | Pause execution |
| `http` | `url`, `method`, `headers`, `data`, `json` | Make HTTP request |
| `manual_approval` | `prompt` | Wait for user confirmation |
| `set_variable` | `name`, `value` | Set workflow variable |

**Registering custom actions:**
```python
from lobster.actions.core import ActionRegistry

registry = ActionRegistry()
registry.register_action("my_action", MyActionInstance())
```

---

## Workflow Definition Format

### Basic Structure

```yaml
id: workflow-id
name: Workflow Name
description: Workflow description

variables:
  var_name: value

steps:
  - id: step-id
    name: Step Name
    action: echo
    params:
      message: "Hello ${var_name}!"
```

### Step Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Optional | Step identifier (auto-generated if missing) |
| `name` | Optional | Human-readable step name |
| `action` | Yes | Action type (echo, shell, sleep, etc.) |
| `params` | Varies | Action-specific parameters |
| `gate` | Optional | Approval gate configuration |

### Approval Gates

```yaml
steps:
  - id: deploy
    name: Deploy to production
    action: shell
    params:
      command: "./deploy.sh"
    gate:
      id: production-approval
      name: Production Deployment Approval
```

---

## Development Workflow

### Running Tests

```bash
cd /path/to/lobster-py
python -m pytest tests/test_workflow.py -v
```

### Running a Workflow

```python
from lobster import Workflow

# Create and run
workflow = Workflow("examples/basic-workflow.yml", state_dir=".lobster")
result = workflow.run()

# Resume from state
result = workflow.resume()

# Check status
status = workflow.status()

# Reset workflow
workflow.reset()
```

### Command Line Usage (when implemented)

```bash
# Run workflow
python -m lobster run examples/basic-workflow.yml

# Resume workflow
python -m lobster run examples/basic-workflow.yml --resume

# Check status
python -m lobster status examples/basic-workflow.yml

# Reset workflow
python -m lobster reset examples/basic-workflow.yml
```

---

## Adding New Features

### Adding a New Action

1. Create action class in `lobster/actions/core.py`:
```python
class MyAction(Action):
    def execute(self, **kwargs) -> Dict:
        # Your implementation
        return {"status": "success"}
```

2. Register it in `ActionRegistry.__init__()`:
```python
self.actions: Dict[str, Action] = {
    # ... existing actions
    "my_action": MyAction(),
}
```

3. Add tests in `tests/test_workflow.py`.

---

### Adding Workflow Features

- **Parallel execution:** Add `parallel: true` to step definition, implement in `Workflow.run()`
- **Conditional execution:** Add `if` field to step, implement with Jinja2 expressions
- **Loop steps:** Add `for_each` field, implement iteration logic
- **Step dependencies:** Add `depends_on` field, implement topological sort

---

## Dependencies

**Required:**
- Python 3.8+
- PyYAML (`pip install pyyaml`)

**Optional:**
- requests (`pip install requests`) - For `http` action

---

## Notes for Agents

1. **State files are stored in `.lobster/` directory** - Clean up when resetting
2. **Workflows are idempotent** - Running twice should produce same result (unless using shell with side effects)
3. **Approval gates create separate files** - One per gate per workflow
4. **Variable substitution is recursive** - Works in nested dicts and lists
5. **Tests use `tempfile`** - No cleanup needed after running tests

---

## License

MIT License (same as nanobot-skills)
