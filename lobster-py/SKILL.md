# Lobster-Py

Python implementation of Lobster workflow system for nanobot - resumable pipelines with approval gates using a pipeline string syntax.

## Overview

Lobster-Py enables you to define multi-step workflows that can:
- **Pause and resume** at any point (via resume tokens)
- **Require approval** before proceeding with critical steps
- **Handle failures** gracefully with async generators
- **Pass data** between workflow stages
- **Extend with custom commands** via decorator registration

## Usage

### Define a Pipeline (String Syntax)

```python
from lobster import run

# Simple pipeline
result = run("exec ls -la | table")

# Pipeline with approval gate
result = run("exec echo 'Before gate' | approve | exec echo 'After gate'")

# Complex pipeline
result = run("exec cat data.json | json pick name email | table")
```

### Pause and Resume

```python
from lobster import run, resume

# Run a pipeline with approval gate
pipeline = "exec ls -la | approve | table"
result = run(pipeline)

# When paused at approval gate, result contains:
# {"status": "paused", "token": "...", "output": "...", "stage_index": 1}

# Resume using the token
resume_token = result["token"]
resumed = resume(resume_token)
```

### Run from Command Line

```bash
cd ~/.nanobot/workspace/skills/lobster-py

# Execute a pipeline
python scripts/exec.py "exec ls -la | table"

# Resume a paused workflow
python scripts/resume.py <token>
```

## Pipeline Syntax

### Format

Pipelines use the pipe syntax: `command | command | command`

Each command can have arguments separated by spaces:
```
exec ls -la | json pick name | table
```

### Stages

When a pipeline is executed, it is split into stages by the pipe (`|`) operator:

| Stage | Example |
|-------|---------|
| Stage 0 | `exec ls -la` |
| Stage 1 | `json pick name` |
| Stage 2 | `table` |

Each stage consumes the output of the previous stage.

---

## Built-in Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| **exec** | Execute shell command | Command and arguments (e.g., `ls -la`) |
| **approve** | Pause for user approval | None (requires user to resume) |
| **json** | Process JSON data | Subcommands: `pick`, `keys`, `values` |
| **table** | Display output as table | None (formats array of objects) |

### Command Details

#### exec
Execute a shell command and return the output.

```
exec ls -la
exec cat data.json
exec curl -s https://api.example.com/data
```

#### approve
Pause the workflow and require manual resume. Used as an approval gate.

```
exec npm publish | approve | exec git push
```

When reached, the workflow pauses and returns a resume token.

#### json
Process JSON data from previous stage.

```
exec cat data.json | json pick name email
exec cat config.json | json keys
exec cat data.json | json values
```

Subcommands:
- `pick <field1> <field2>...` - Extract specific fields from objects
- `keys` - Extract object keys
- `values` - Extract object values

#### table
Display output as a formatted table. Works best with array of objects.

```
exec cat users.json | json pick name email | table
```

---

## Adding Custom Commands

### Register a Command

Use the `@register_command` decorator to add custom commands:

```python
from lobster.commands.registry import register_command

@register_command("where")
async def where_command(args, input_stream):
    """Filter input based on conditions."""
    async for item in input_stream:
        # Your filtering logic here
        if meets_condition(item):
            yield item
```

### Command Interface

All commands receive:
- `args: list[str]` - Command arguments (split by spaces)
- `input_stream: AsyncGenerator[any, None]` - Output from previous stage

Commands should yield items to the output stream.

### Example: Custom Command

```python
@register_command("map")
async def map_command(args, input_stream):
    """Transform each item using a Python expression."""
    expression = " ".join(args)
    async for item in input_stream:
        yield eval(expression, {"x": item, "item": item})
```

Usage:
```
exec cat data.json | map x['name'].upper() | table
```

---

## Resume Mechanism

### How It Works

1. Workflow pauses at an `approve` gate
2. Runtime returns a **resume token** (base64url encoded)
3. Store the token somewhere (database, file, memory)
4. Call `resume(token)` to continue from that point

### Token Format

Tokens are base64url encoded JSON containing:
- Pipeline string
- Stage index (where to resume from)
- Intermediate state (if needed)

```python
import base64
import json

# Decode a token to see its contents
decoded = base64.urlsafe_b64decode(token + "==")
data = json.loads(decoded)
print(data)
# {"pipeline": "exec ls | approve | table", "stage_index": 1}
```

---

## Project Structure

```
lobster-python/
├── lobster/
│   ├── __init__.py       # Package exports (run, resume)
│   ├── cli.py            # CLI entry point
│   ├── parser.py         # Pipeline string parser
│   ├── runtime.py        # Pipeline executor
│   ├── token.py          # Token encode/decode
│   ├── state.py          # State persistence
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── registry.py   # Command registration
│   │   └── core/
│   │       ├── exec.py
│   │       ├── approve.py
│   │       ├── json.py
│   │       └── table.py
│   └── workflows/        # YAML workflow loader (planned)
├── tests/
│   └── test_basic.py      # Core functionality tests
├── requirements.txt      # Python dependencies
├── setup.py              # Package configuration
└── README.md
```

---

## Requirements

- Python 3.9+
- No external dependencies for core functionality

## Installation

The skill is located at:
```
~/.nanobot/workspace/skills/lobster-py/
~/.nanobot/workspace/skills/lobster-py/lobster/  # Symlink to ~/lobster-python/
```

### Quick Start

```bash
cd ~/.nanobot/workspace/skills/lobster-py

# Test basic pipeline
python scripts/exec.py "exec ls -la | table"

# Test with approval gate
python scripts/exec.py "exec echo 'Hello' | approve | exec echo 'World'"
```

---

## Examples

### Example 1: List Files
```python
from lobster import run

result = run("exec ls -la | table")
print(result["output"])
```

### Example 2: Process JSON
```python
from lobster import run

# Extract specific fields from JSON
result = run("""
exec cat ~/data/users.json |
json pick name email age |
table
""")
```

### Example 3: Approval Gate
```python
from lobster import run, resume

# Deploy workflow with approval
pipeline = """
exec npm test |
approve |
exec npm publish |
exec git push
"""

result = run(pipeline)

if result["status"] == "paused":
    print(f"Paused at approval gate. Token: {result['token']}")
    # User manually approves by calling resume(token)
    final = resume(result["token"])
```

---

## Planned Features

| Feature | Status | ETA |
|---------|--------|-----|
| State file persistence | ✅ Implemented | Available now |
| YAML workflow files | 🟢 Planned | Future |
| Built-in data commands (where, head, map, sort) | 🟢 Planned | Future |
| Nanobot tool integration | 🟢 Planned | Future |
| Workflow templates | 🟢 Planned | Future |

---

## API Reference

### Main Functions

```python
from lobster import run, resume

async def run(pipeline: str) -> dict:
    """
    Execute a pipeline string.
    
    Returns:
        dict: {"status": "complete"|"paused"|"error",
               "output": "...",
               "token": "...",  # Only if paused
               "error": "..."}  # Only if error
    """

async def resume(token: str) -> dict:
    """
    Resume a paused workflow using a token.
    
    Returns:
        dict: Same format as run()
    """
```

### Command Registration

```python
from lobster.commands.registry import register_command

@register_command("command_name")
async def my_command(args: list[str], input_stream):
    """Custom command implementation."""
    async for item in input_stream:
        # Process item
        yield processed_item
```

---

## License

Ported from OpenClaw Lobster workflow system (TypeScript → Python).
