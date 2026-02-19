"""
Z.AI Quota Checker Skill
Check Z.AI GLM Coding Plan usage statistics with real-time quota monitoring,
model usage tracking, and MCP tool usage.
"""

from .zai_quota import (
    check_quota,
    check_endpoint_query,
    format_whatsapp,
    format_terminal,
    QuotaResult,
)

__version__ = "1.0.0"
__all__ = [
    "check_quota",
    "check_endpoint_query",
    "format_whatsapp",
    "format_terminal",
    "QuotaResult",
]
