---
name: zai-quota
description: Check Z.AI GLM Coding Plan usage statistics with real-time quota monitoring, model usage tracking, and MCP tool usage.
author: nanobot-ai
version: "1.0.0"
---

# Z.AI Quota Checker

Check your Z.AI GLM Coding Plan usage statistics in real-time, including quota limits, model usage, and MCP tool usage.

## Features
- Real-time quota monitoring - Query official Z.AI monitoring API endpoints
- Model usage tracking - Token usage and call counts by model
- Tool usage statistics - Network searches, web reads, zread calls
- WhatsApp-friendly output - Clean formatting with emojis
- Multiple platforms - Support for Z.AI (global) and Zhipu (China)

## Setup

### API Key

Get your Z.AI API key from: https://z.ai/manage-apikey/apikey-list

Set the environment variable:
```bash
export ZAI_API_KEY="your-api-key-here"
```

## Plan Tiers & Limits

The GLM Coding Plan uses two types of quotas:

### 1. Time-based Quota (MCP Tools)
Monthly quota for MCP tool usage (network searches, web reads, etc.)
- **Lite:** 100 hours/month
- **Pro:** 300 hours/month
- **Max:** 800 hours/month

### 2. Token-based Quota (5hr Rolling Window)
Token limits reset every 5 hours based on real usage
- **Lite:** 40M tokens / 5hr
- **Pro:** 160M tokens / 5hr (4x Lite)
- **Max:** 800M tokens / 5hr (20x Lite)

## Important Notes

- **Model & Tool Usage** data only populates when you use Z.AI through supported tools (OpenCode, Claude Code, Cline, OpenCode)
- Direct API calls do NOT populate model/tool usage statistics - this is a Z.AI API limitation
- Token usage is estimated from the API percentage based on your plan tier
