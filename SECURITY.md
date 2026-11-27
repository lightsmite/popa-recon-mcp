# Security Policy

## Reporting a Vulnerability

Please report security issues privately through GitHub Security Advisories for this repository or via [https://poparecon.com](https://poparecon.com).

## Design Notes

- The STDIO bridge in `popa_recon_mcp.py` has zero third-party runtime dependencies and forwards standard MCP JSON-RPC requests over HTTPS to `https://poparecon.com/mcp`.
- Public requests require no API keys and never read private chats or credentials.
