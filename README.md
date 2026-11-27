# POPA Recon MCP Server

[![POPA Recon MCP connector](https://glama.ai/mcp/connectors/com.poparecon/popa-recon/badges/score.svg)](https://glama.ai/mcp/connectors/com.poparecon/popa-recon)

Public Web3, on-chain, and crypto market **deep research** over the [Model Context Protocol](https://modelcontextprotocol.io/).

Connect your AI assistant directly to **`https://poparecon.com/mcp`** (Streamable HTTP, no API key required on the public tier) to investigate wallets, tokens, protocols, exploits, governance votes, SEC filings, and live crypto news with cited primary sources.

- **Website:** [https://poparecon.com](https://poparecon.com)
- **Hosted MCP Endpoint:** `https://poparecon.com/mcp`
- **Glama Connector:** [com.poparecon/popa-recon](https://glama.ai/mcp/connectors/com.poparecon/popa-recon)
- **How It Investigates:** [https://poparecon.com/how](https://poparecon.com/how)
- **Guides & Token Index:** [Guides](https://poparecon.com/guides) · [Tokens](https://poparecon.com/token)

---

## Capabilities

POPA Recon runs multi-step investigations and deep research reports across on-chain explorers and primary web sources, returning structured prose with inline clickable citations:

- **On-chain & wallet intelligence:** entity attribution, labels, balances, token flows, and transaction traces (Arkham Intelligence, DeBank, OKLink).
- **DeFi & market metrics:** TVL, protocol fees/revenue, yields, market cap, and liquidity data (DefiLlama, CoinMarketCap).
- **Primary & community sources:** SEC EDGAR filings, GitHub repositories, crypto news wires, X, and public Telegram crypto channels.
- **Deep research mode:** complex multi-step investigations, hack/exploit post-mortems, and tokenomics breakdowns run an extended research notebook before synthesis.
- **Multilingual answers:** answers in the language of your question (English, Russian, Ukrainian, and more).
- **Read-only & factual:** research only — no investment advice, no price predictions, no wallet custody, no trades or transfers.

---

## Quick Connect (Hosted Remote Server)

No local build or API key is required for the public anonymous tier.

### Claude Code

```bash
claude mcp add --transport http popa-recon https://poparecon.com/mcp
```

### Cursor / VS Code / Windsurf (`mcp.json`)

Add to your project `.cursor/mcp.json` or editor MCP configuration (or use [`mcp.json`](./mcp.json) from this repository):

```json
{
  "mcpServers": {
    "popa-recon": {
      "url": "https://poparecon.com/mcp"
    }
  }
}
```

> Using Cursor's plugin manifest format? See [`lightsmite/popa-recon-plugin`](https://github.com/lightsmite/popa-recon-plugin).

### ChatGPT / Claude.ai

In **Settings → Connectors** (or Custom MCP Connectors), add a new remote MCP server pointing to:

```text
https://poparecon.com/mcp
```

### STDIO-Only Clients (Claude Desktop, Local Tools)

For clients that only spawn local `stdio` servers:

**Option A — `mcp-remote` (Node.js):**

```json
{
  "mcpServers": {
    "popa-recon": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://poparecon.com/mcp"]
    }
  }
}
```

**Option B — Included zero-dependency Python 3.10+ bridge ([`popa_recon_mcp.py`](./popa_recon_mcp.py)):**

```bash
git clone https://github.com/lightsmite/popa-recon-mcp.git
cd popa-recon-mcp
pip install .
```

```json
{
  "mcpServers": {
    "popa-recon": {
      "command": "popa-recon-mcp"
    }
  }
}
```

Or run `python3 /path/to/popa_recon_mcp.py` directly with no install step. To point at a personal paid-credit endpoint instead of the anonymous tier, set `POPA_RECON_MCP_URL=https://poparecon.com/mcp/u/<your-token>` (or pass `--url`).

---

## MCP Tools

Protocol version: `2025-03-26` (Streamable HTTP). All tools also expose MCP Apps UI metadata (`ui://popa-recon/research-*.html`) for rich live progress cards in supporting clients.

| Tool | Description | Inputs | Read-only |
|---|---|---|---|
| `research` | Starts a saved factual Web3 research request in the language of the question. Waits up to 40s and returns the sourced answer + steps, or a `pending` `request_id` receipt for longer deep-research runs. | `question` (`string`, 1–1000 chars) | No |
| `answer` | Reads the status, progress steps, finished answer, and cited `sources` for a `request_id` returned by `research`. Starts no new research and consumes no quota. | `request_id` (`string`, 43-char receipt) | Yes |
| `account_status` | Reports remaining free daily questions, credits, active plan, products on sale, and `buy_url`. Costs nothing and starts no research. | `{}` | Yes |

### Example Prompts

- *"Research the security model, fee mechanics, and validator structure of Hyperliquid with primary sources."*
- *"Trace the treasury wallets and recent protocol revenue trends of Aave DAO over the past quarter."*
- *"What happened in the most recent cross-chain bridge exploit this week, including attacker addresses and post-mortem links?"*
- *"Summarize SEC disclosures, token unlock schedule, and DefiLlama TVL breakdown for Ondo Finance."*

---

## Privacy, Limits & Links

- Public queries are processed on their own without your chat history. Do not submit secrets or private personal data.
- **How POPA Recon investigates:** [https://poparecon.com/how](https://poparecon.com/how)
- **Guides:** [https://poparecon.com/guides](https://poparecon.com/guides)
- **Token directory:** [https://poparecon.com/token](https://poparecon.com/token)
- **Privacy Policy:** [https://poparecon.com/policy](https://poparecon.com/policy)
- **Terms of Service:** [https://poparecon.com/terms](https://poparecon.com/terms)
- **Support:** [https://poparecon.com/support](https://poparecon.com/support)

## License

[MIT](./LICENSE)
