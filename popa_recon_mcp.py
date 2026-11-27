"""Zero-dependency STDIO-to-Streamable-HTTP bridge for the POPA Recon MCP server."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_MCP_URL = "https://poparecon.com/mcp"


def _emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _error_response(msg_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def _iter_sse_json(body: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    data_lines: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.rstrip("\r")
        if line == "":
            if data_lines:
                payload = "\n".join(data_lines).strip()
                data_lines.clear()
                if payload:
                    events.append(json.loads(payload))
        elif line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
    if data_lines:
        payload = "\n".join(data_lines).strip()
        if payload:
            events.append(json.loads(payload))
    return events


def _forward_message(
    url: str,
    raw_line: str,
    session_id: str | None,
    timeout: float,
) -> tuple[list[dict[str, Any]], str | None]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "popa-recon-mcp/0.1.0",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id

    req = urllib.request.Request(
        url,
        data=raw_line.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        next_session = resp.headers.get("Mcp-Session-Id") or session_id
        status = getattr(resp, "status", 200)
        raw_body = resp.read().decode("utf-8", errors="replace").strip()
        if status in (202, 204) or not raw_body:
            return [], next_session
        content_type = resp.headers.get("Content-Type", "").lower()
        if "text/event-stream" in content_type:
            return _iter_sse_json(raw_body), next_session
        parsed = json.loads(raw_body)
        if isinstance(parsed, list):
            return [item for item in parsed if isinstance(item, dict)], next_session
        if isinstance(parsed, dict):
            return [parsed], next_session
        return [], next_session


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bridge MCP JSON-RPC over STDIO to the POPA Recon Streamable HTTP endpoint."
    )
    parser.add_argument(
        "--url",
        default=os.environ.get("POPA_RECON_MCP_URL", DEFAULT_MCP_URL),
        help=f"Remote MCP endpoint URL (default: {DEFAULT_MCP_URL})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=65.0,
        help="HTTP request timeout in seconds (default: 65)",
    )
    args = parser.parse_args(argv)

    session_id: str | None = None
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        msg_id: Any = None
        try:
            decoded = json.loads(line)
            if isinstance(decoded, dict):
                msg_id = decoded.get("id")
        except json.JSONDecodeError as exc:
            _emit(_error_response(None, -32700, f"Invalid JSON: {exc}"))
            continue

        try:
            responses, session_id = _forward_message(args.url, line, session_id, args.timeout)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace").strip()
            if msg_id is not None:
                _emit(_error_response(msg_id, -32603, f"HTTP {exc.code}: {detail or exc.reason}"))
            continue
        except Exception as exc:
            if msg_id is not None:
                _emit(_error_response(msg_id, -32603, f"Bridge request failed: {exc}"))
            continue

        for item in responses:
            _emit(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
