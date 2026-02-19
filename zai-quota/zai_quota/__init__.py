"""
Z.AI Quota Checker - Core Module
Queries Z.AI monitoring API endpoints for usage statistics.
"""

import os
import json
import time
from dataclasses import dataclass
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import urllib.request
import urllib.error

PLATFORMS = {
    "zai": {
        "model_usage": "https://api.z.ai/api/monitor/usage/model-usage",
        "tool_usage": "https://api.z.ai/api/monitor/usage/tool-usage",
        "quota_limit": "https://api.z.ai/api/monitor/usage/quota/limit",
    },
    "zhipu": {
        "model_usage": "https://open.bigmodel.cn/api/monitor/usage/model-usage",
        "tool_usage": "https://open.bigmodel.cn/api/monitor/usage/tool-usage",
        "quota_limit": "https://open.bigmodel.cn/api/monitor/usage/quota/limit",
    },
}

REQUEST_TIMEOUT = 10

@dataclass
class QuotaResult:
    """Result from querying Z.AI usage endpoints."""
    platform: str
    start_time: str
    end_time: str
    plan_level: str = "Unknown"
    quota_data: Optional[Dict[str, Any]] = None
    model_data: Optional[Dict[str, Any]] = None
    tool_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class LimitItem:
    """Single quota limit item."""
    type: str
    percentage: float
    current_value: Optional[int] = None
    total: Optional[int] = None
    usage_details: Optional[Dict[str, Any]] = None
    next_reset_time: Optional[int] = None

def get_api_key() -> Optional[str]:
    return os.environ.get("ZAI_API_KEY") or os.environ.get("ZHIPU_API_KEY")

def get_platform(platform: str) -> str:
    if not platform:
        if os.environ.get("ZHIPU_API_KEY"):
            return "zhipu"
        return "zai"
    return platform.lower()

def get_endpoints(platform: str) -> Dict[str, str]:
    return PLATFORMS.get(platform, PLATFORMS["zai"])

def get_time_window() -> tuple[str, str]:
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    start = now - datetime.timedelta(days=1)
    start = start.replace(minute=0, second=0, microsecond=0)
    end = now.replace(minute=59, second=59, microsecond=999999)
    return start.isoformat(), end.isoformat()

def make_request(url: str, api_key: str, params: Optional[str] = None) -> Dict[str, Any]:
    full_url = f"{url}?{params}" if params else url
    request = urllib.request.Request(
        full_url,
        method="GET",
        headers={
            "Authorization": api_key,
            "Accept-Language": "en-US,en",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            data = response.read().decode("utf-8")
            # Handle empty responses (some endpoints return HTTP 200 with empty body)
            if not data or not data.strip():
                return {}
            return json.loads(data)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        error_msg = f"HTTP {e.code}: {body}" if body else f"HTTP {e.code}"
        raise urllib.error.HTTPError(url, e.code, error_msg, e.headers, None) from e
    except urllib.error.URLError as e:
        error_msg = str(e.reason)
        raise urllib.error.URLError(error_msg) from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}") from e

def query_endpoint(endpoint: str, api_key: str, platform: str = "zai", use_time_window: bool = True) -> Dict[str, Any]:
    endpoints = get_endpoints(platform)
    endpoint_map = {
        "model": endpoints["model_usage"],
        "model_usage": endpoints["model_usage"],
        "tool": endpoints["tool_usage"],
        "tool_usage": endpoints["tool_usage"],
        "quota": endpoints["quota_limit"],
        "quota_limit": endpoints["quota_limit"],
    }
    url = endpoint_map.get(endpoint)
    if not url:
        raise ValueError(f"Invalid endpoint: {endpoint}")
    params = None
    if use_time_window and endpoint in ("model", "model_usage", "tool", "tool_usage"):
        start, end = get_time_window()
        params = urlencode({"startTime": start, "endTime": end})
    return make_request(url, api_key, params)

def check_quota(api_key: Optional[str] = None, platform: Optional[str] = None) -> QuotaResult:
    api_key = api_key or get_api_key()
    if not api_key:
        return QuotaResult(
            platform=platform or "zai",
            start_time="",
            end_time="",
            error="❌ Z.ai credentials not found. Set ZAI_API_KEY environment variable.",
        )
    platform = get_platform(platform or "")
    start, end = get_time_window()
    quota_data = None
    model_data = None
    tool_data = None
    error = None
    try:
        quota_data = query_endpoint("quota", api_key, platform, use_time_window=False)
    except Exception as e:
        error = f"Quota: {e}"
    try:
        model_data = query_endpoint("model", api_key, platform, use_time_window=True)
    except Exception as e:
        if not error:
            error = f"Model: {e}"
    try:
        tool_data = query_endpoint("tool", api_key, platform, use_time_window=True)
    except Exception as e:
        if not error:
            error = f"Tool: {e}"
    
    # Extract plan level
    plan_level = "Unknown"
    if quota_data:
        if "data" in quota_data and isinstance(quota_data["data"], dict):
            plan_level = quota_data["data"].get("level", "Unknown")
        elif "level" in quota_data:
            plan_level = quota_data.get("level", "Unknown")
    
    return QuotaResult(
        platform=platform,
        start_time=start,
        end_time=end,
        plan_level=plan_level,
        quota_data=quota_data,
        model_data=model_data,
        tool_data=tool_data,
        error=error,
    )

def check_endpoint_query(endpoint: str, api_key: Optional[str] = None, platform: Optional[str] = None) -> QuotaResult:
    api_key = api_key or get_api_key()
    if not api_key:
        return QuotaResult(
            platform=platform or "zai",
            start_time="",
            end_time="",
            error="❌ Z.ai credentials not found. Set ZAI_API_KEY environment variable.",
        )
    platform = get_platform(platform or "")
    start, end = get_time_window()
    use_time_window = endpoint in ("model", "model_usage", "tool", "tool_usage")
    data = None
    error = None
    try:
        data = query_endpoint(endpoint, api_key, platform, use_time_window=use_time_window)
    except Exception as e:
        error = str(e)
    result = QuotaResult(
        platform=platform,
        start_time=start,
        end_time=end,
        error=error,
    )
    if endpoint in ("quota", "quota_limit"):
        result.quota_data = data
    elif endpoint in ("model", "model_usage"):
        result.model_data = data
    elif endpoint in ("tool", "tool_usage"):
        result.tool_data = data
    return result

def format_number(num: int) -> str:
    return f"{num:,}"

def format_progress_bar(percentage: float, width: int = 20) -> str:
    filled = int(width * percentage / 100)
    empty = width - filled
    return "█" * filled + "░" * empty

def format_time_until_reset(reset_time_ms: int) -> str:
    now_ms = int(time.time() * 1000)
    diff_ms = reset_time_ms - now_ms
    if diff_ms <= 0:
        return "Resets now"
    diff_seconds = diff_ms // 1000
    hours = diff_seconds // 3600
    minutes = (diff_seconds % 3600) // 60
    if hours == 0:
        return f"{minutes}m"
    elif hours == 1:
        return f"{hours}h {minutes}m"
    else:
        return f"{hours}h {minutes}m"

def parse_limits(quota_data: Dict[str, Any]) -> tuple[list, str]:
    """Parse limits and return (limits, plan_level)."""
    limits = []
    plan_level = "Unknown"
    
    # Handle nested structure (data.limits) or direct (limits)
    limits_list = None
    if "data" in quota_data and isinstance(quota_data["data"], dict):
        if "limits" in quota_data["data"] and isinstance(quota_data["data"]["limits"], list):
            limits_list = quota_data["data"]["limits"]
        if "level" in quota_data["data"]:
            plan_level = quota_data["data"]["level"]
    elif "limits" in quota_data and isinstance(quota_data["limits"], list):
        limits_list = quota_data["limits"]
        if "level" in quota_data:
            plan_level = quota_data["level"]
    
    if not limits_list:
        return limits, plan_level
    
    # Plan token limits (5hr rolling window) - from Reddit user reports
    PLAN_TOKEN_LIMITS = {
        "lite": 40_000_000,      # 40M
        "pro": 160_000_000,      # 160M (4x)
        "max": 800_000_000,      # 800M (20x)
    }
    
    for item in limits_list:
        limit_type = item.get("type", "Unknown")
        percentage = float(item.get("percentage", 0))
        
        # Calculate token usage based on plan tier
        current_value = item.get("currentValue")
        total = item.get("total")
        
        if limit_type == "TOKENS_LIMIT":
            # Token usage: estimate from percentage since API doesn't provide absolute values
            plan_key = plan_level.lower()
            token_limit = PLAN_TOKEN_LIMITS.get(plan_key, 40_000_000)
            estimated_used = int((percentage / 100) * token_limit)
            limit = LimitItem(
                type="Token usage (5hr rolling window)",
                percentage=percentage,
                current_value=estimated_used,
                total=token_limit,
                usage_details=item.get("usageDetails"),
                next_reset_time=item.get("nextResetTime"),
            )
        elif limit_type == "TIME_LIMIT":
            # Time-based quota: monthly MCP quota (100 hours total)
            remaining = item.get("remaining", 0)
            total = current_value + remaining  # Should be ~100 hours
            limit = LimitItem(
                type=f"Time-based quota (MCP tools, {current_value}h used / {total}h monthly)",
                percentage=percentage,
                current_value=current_value,
                total=total,
                usage_details=item.get("usageDetails"),
                next_reset_time=item.get("nextResetTime"),
            )
        else:
            # Unknown limit type
            limit = LimitItem(
                type=limit_type,
                percentage=percentage,
                current_value=current_value,
                total=total,
                usage_details=item.get("usageDetails"),
                next_reset_time=item.get("nextResetTime"),
            )
        limits.append(limit)
    
    return limits, plan_level

def format_whatsapp(result: QuotaResult) -> str:
    lines = []
    lines.append("📊 Z.AI GLM Coding Plan Usage")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")
    
    # Show plan level if available
    if result.plan_level and result.plan_level != "Unknown":
        plan_emoji = {"lite": "🌱", "pro": "🚀", "max": "💎"}.get(result.plan_level.lower(), "📋")
        lines.append(f"{plan_emoji} Plan: {result.plan_level.upper()}")
        lines.append("")
    
    if result.error:
        lines.append(f"❌ Error: {result.error}")
        return "\n".join(lines)
    lines.append("🎯 Quota Limits")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if result.quota_data:
        limits, _ = parse_limits(result.quota_data)
        if not limits:
            lines.append("  No quota data available")
        else:
            for limit in limits:
                bar = format_progress_bar(limit.percentage)
                lines.append(f"{limit.type}: {limit.percentage}% {bar}")
                if limit.next_reset_time:
                    reset_msg = format_time_until_reset(limit.next_reset_time)
                    lines.append(f"  Resets in: {reset_msg}")
                if limit.current_value is not None and limit.total is not None:
                    lines.append(f"  Used: {limit.current_value}/{limit.total}")
                lines.append("")
    else:
        lines.append("  No quota data available")
        lines.append("")
    lines.append("📈 Model Usage (24h)")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if result.model_data and "totalUsage" in result.model_data:
        total_usage = result.model_data["totalUsage"]
        tokens = total_usage.get("totalTokensUsage")
        calls = total_usage.get("totalModelCallCount")
        token_limit = 40_000_000
        token_pct = 0
        if result.quota_data:
            limits = parse_limits(result.quota_data)
            for limit in limits:
                if "Token" in limit.type:
                    token_pct = limit.percentage
                    if limit.total:
                        token_limit = limit.total
                    break
        if tokens is not None:
            pct_24h = int((tokens / token_limit) * 100) if token_limit > 0 else 0
            lines.append(f"  Total Tokens (24h): {format_number(tokens)} ({pct_24h}% of 5h limit)")
            lines.append(f"  5h Window Usage: {token_pct}% of {format_number(token_limit)}")
        if calls is not None:
            lines.append(f"  Total Calls: {format_number(calls)}")
    else:
        lines.append("  No model usage data")
    lines.append("")
    lines.append("🔧 Tool/MCP Usage (24h)")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if result.tool_data and "totalUsage" in result.tool_data:
        total_usage = result.tool_data["totalUsage"]
        search = total_usage.get("totalNetworkSearchCount")
        web_read = total_usage.get("totalWebReadMcpCount")
        zread = total_usage.get("totalZreadMcpCount")
        if search is not None:
            lines.append(f"  Network Searches: {format_number(search)}")
        if web_read is not None:
            lines.append(f"  Web Reads: {format_number(web_read)}")
        if zread is not None:
            lines.append(f"  ZRead Calls: {format_number(zread)}")
        if result.quota_data:
            limits, _ = parse_limits(result.quota_data)
            for limit in limits:
                if "Time-based quota" in limit.type and limit.usage_details:
                    lines.append("  MCP Tool Details:")
                    for detail in limit.usage_details:
                        model_code = detail.get("modelCode", "Unknown")
                        usage = detail.get("usage", 0)
                        lines.append(f"    - {model_code}: {usage}")
                    break
    else:
        lines.append("  No tool usage data")
    return "\n".join(lines)

def format_terminal(result: QuotaResult) -> str:
    HORIZONTAL = "─"
    VERTICAL = "│"
    TL = "┌"
    TR = "┐"
    BL = "└"
    BR = "┘"
    CROSS_LEFT = "├"
    CROSS_RIGHT = "┤"
    BOX_WIDTH = 50
    def pad_line(content: str) -> str:
        return f"{VERTICAL}  {content.ljust(BOX_WIDTH - 4)}{VERTICAL}"
    def separator() -> str:
        return f"{CROSS_LEFT}{HORIZONTAL * BOX_WIDTH}{CROSS_RIGHT}"
    lines = []
    lines.append(f"{TL}{HORIZONTAL * BOX_WIDTH}{TR}")
    lines.append(f"{VERTICAL}{' ' * BOX_WIDTH}{VERTICAL}")
    lines.append(pad_line("Z.ai GLM Coding Plan Usage Statistics"))
    lines.append(f"{VERTICAL}{' ' * BOX_WIDTH}{VERTICAL}")
    lines.append(separator())
    lines.append(pad_line(f"Platform: {result.platform.upper()}"))
    lines.append(pad_line(f"Plan:     {result.plan_level.upper()}"))
    lines.append(pad_line(f"Period:   {result.start_time} → {result.end_time}"))
    lines.append(separator())
    if result.error:
        lines.append(pad_line(f"Error: {result.error}"))
        lines.append(f"{BL}{HORIZONTAL * BOX_WIDTH}{BR}")
        return "\n".join(lines)
    lines.append(pad_line("QUOTA LIMITS"))
    lines.append(f"{CROSS_LEFT}{HORIZONTAL * (BOX_WIDTH - 2)}┴{CROSS_RIGHT}")
    if result.quota_data:
        limits, _ = parse_limits(result.quota_data)
        if not limits:
            lines.append(pad_line("No quota data available"))
        else:
            for limit in limits:
                bar = format_progress_bar(limit.percentage, width=BOX_WIDTH - 20)
                lines.append(pad_line(f"{limit.type} [{bar}] {limit.percentage}%"))
                if limit.next_reset_time:
                    reset_msg = format_time_until_reset(limit.next_reset_time)
                    lines.append(pad_line(f"Resets in: {reset_msg}"))
                if limit.current_value is not None and limit.total is not None:
                    lines.append(pad_line(f"Used: {limit.current_value}/{limit.total}"))
    else:
        lines.append(pad_line("No quota data available"))
    lines.append(separator())
    lines.append(pad_line("MODEL USAGE (24h)"))
    lines.append(f"{CROSS_LEFT}{HORIZONTAL * (BOX_WIDTH - 2)}┴{CROSS_RIGHT}")
    if result.model_data and "totalUsage" in result.model_data:
        total_usage = result.model_data["totalUsage"]
        tokens = total_usage.get("totalTokensUsage")
        calls = total_usage.get("totalModelCallCount")
        token_limit = 40_000_000
        token_pct = 0
        if result.quota_data:
            limits = parse_limits(result.quota_data)
            for limit in limits:
                if "Token" in limit.type:
                    token_pct = limit.percentage
                    if limit.total:
                        token_limit = limit.total
                    break
        if tokens is not None:
            pct_24h = int((tokens / token_limit) * 100) if token_limit > 0 else 0
            lines.append(pad_line(f"Total Tokens (24h): {format_number(tokens)} ({pct_24h}% of 5h limit)"))
            lines.append(pad_line(f"5h Window Usage: {token_pct}% of {format_number(token_limit)}"))
        if calls is not None:
            lines.append(pad_line(f"Total Calls: {format_number(calls)}"))
    else:
        lines.append(pad_line("No model usage data"))
    lines.append(separator())
    lines.append(pad_line("TOOL/MCP USAGE (24h)"))
    lines.append(f"{CROSS_LEFT}{HORIZONTAL * (BOX_WIDTH - 2)}┴{CROSS_RIGHT}")
    if result.tool_data and "totalUsage" in result.tool_data:
        total_usage = result.tool_data["totalUsage"]
        search = total_usage.get("totalNetworkSearchCount")
        web_read = total_usage.get("totalWebReadMcpCount")
        zread = total_usage.get("totalZreadMcpCount")
        if search is not None:
            lines.append(pad_line(f"Network Searches: {format_number(search)}"))
        if web_read is not None:
            lines.append(pad_line(f"Web Reads: {format_number(web_read)}"))
        if zread is not None:
            lines.append(pad_line(f"ZRead Calls: {format_number(zread)}"))
    else:
        lines.append(pad_line("No tool usage data"))
    lines.append(f"{BL}{HORIZONTAL * BOX_WIDTH}{BR}")
    return "\n".join(lines)


def cli_main():
    """CLI entrypoint for zai-quota command."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Check Z.AI GLM Coding Plan usage and quota")
    parser.add_argument("--api-key", help="Z.AI API key (overrides ZAI_API_KEY env var)")
    parser.add_argument("--platform", choices=["zai", "zhipu"], default=None, help="Platform to query (zai or zhipu)")
    parser.add_argument("--endpoint", choices=["quota", "model", "tool", "quota_limit", "model_usage", "tool_usage"],
                       help="Query specific endpoint only")
    parser.add_argument("--format", choices=["whatsapp", "terminal"], default=None, help="Output format")
    
    args = parser.parse_args()
    
    # Detect format from environment if not specified
    output_format = args.format
    if not output_format:
        output_format = os.environ.get("CHANNEL", "terminal")
        if output_format in ["whatsapp", "telegram", "discord"]:
            output_format = "whatsapp"
        else:
            output_format = "terminal"
    
    # Query API
    if args.endpoint:
        result = check_endpoint_query(args.endpoint, args.api_key, args.platform)
    else:
        result = check_quota(args.api_key, args.platform)
    
    # Format output
    if output_format == "whatsapp":
        print(format_whatsapp(result))
    else:
        print(format_terminal(result))


if __name__ == "__main__":
    cli_main()
