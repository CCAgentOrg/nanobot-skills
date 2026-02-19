---
name: zai-quota
description: Check Z.AI GLM Coding Plan quota statistics with real-time monitoring.
author: nanobot-ai
version: "1.1.0"
---

# Z.AI Quota Checker

Check your Z.AI GLM Coding Plan quota statistics in real-time, including token usage and time-based quotas.

## Features
- Real-time quota monitoring - Query official Z.AI monitoring API endpoints
- Token usage tracking - 5hr rolling window with progress bar
- Time-based quota - Monthly MCP tool usage hours
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

### 1. Token-based Quota (5hr Rolling Window)
Token limits reset every 5 hours based on real usage
- **Lite:** 40M tokens / 5hr
- **Pro:** 160M tokens / 5hr (4x Lite)
- **Max:** 800M tokens / 5hr (20x Lite)

### 2. Time-based Quota (Monthly)
Monthly quota for MCP tool usage
- **Lite:** 100 hours/month
- **Pro:** 300 hours/month
- **Max:** 800 hours/month

## Notes

- Token usage is estimated from the API percentage based on your plan tier
- Quota data comes directly from Z.AI's monitoring endpoints
