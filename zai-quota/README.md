# zai-quota Skill

Check your Z.AI GLM Coding Plan usage statistics with real-time quota monitoring.

## Features

- 📊 Real-time quota monitoring from official Z.AI API
- 🌱 Plan tier detection (Lite/Pro/Max)
- 💰 Token usage tracking with 5hr rolling window
- ⏱️ Time-based quota for MCP tools (monthly)
- 📱 WhatsApp-friendly output with emojis
- 💻 Terminal-friendly ASCII table output
- 🔍 Query specific endpoints (quota, model, tool)

## Plan Tiers & Limits

### Time-based Quota (MCP Tools)
Monthly quota for MCP tool usage
- **Lite:** 100 hours/month
- **Pro:** 300 hours/month
- **Max:** 800 hours/month

### Token-based Quota (5hr Rolling Window)
Token limits reset every 5 hours
- **Lite:** 40M tokens / 5hr
- **Pro:** 160M tokens / 5hr (4x Lite)
- **Max:** 800M tokens / 5hr (20x Lite)

## Installation

Copy the skill to your nanobot skills directory:

```bash
cp -r zai-quota ~/.nanobot/workspace/skills/
```

Restart nanobot to load the skill:
```bash
pm2 restart nanobot-gateway
```

## Usage

### In nanobot (WhatsApp/Telegram):

```
/zai-quota
```

### Standalone CLI:

```bash
# Check all quota
zai-quota

# Check specific endpoint
zai-quota --endpoint quota
zai-quota --endpoint model
zai-quota --endpoint tool

# Use custom API key
zai-quota --api-key your-key-here

# Force terminal output
zai-quota --format terminal
```

## Environment Variables

- `ZAI_API_KEY` - Your Z.AI API key (required)
- `CHANNEL` - Auto-detects output format (whatsapp/telegram/discord = WhatsApp, others = terminal)

## API Endpoints

This skill queries the following Z.AI monitoring endpoints:

- `https://api.z.ai/api/monitor/usage/quota/limit` - Total quota and remaining
- `https://api.z.ai/api/monitor/usage/model-usage` - Model usage by GLM version
- `https://api.z.ai/api/monitor/usage/tool-usage` - MCP tool usage

## Example Output (WhatsApp)

```
📊 Z.AI GLM Coding Plan Usage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌱 Plan: LITE

🎯 Quota Limits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Time-based quota (MCP tools, 5h used / 100h monthly): 5% ░░░░░░░░░░░░░░░░░█░░░░
  Resets in: 183h 59m
  Used: 5/100

Token usage (5hr rolling window): 31% ████████████████░░░░░░░░░░░░
  Resets in: 2h 13m
  Used: 12,400,000/40,000,000

📈 Model Usage (24h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No model usage data

🔧 Tool/MCP Usage (24h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No tool usage data
```

## Important Notes

- **Model & Tool Usage** data only populates when you use Z.AI through supported tools (OpenCode, Claude Code, Cline)
- Direct API calls do NOT populate model/tool usage statistics - this is a Z.AI API limitation
- Token usage is estimated from the API percentage based on your plan tier

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Based On

This skill is based on the [opencode-glm-quota](https://github.com/guyinwonder168/opencode-glm-quota) OpenCode plugin, with additional plan tier detection and token usage estimation.
