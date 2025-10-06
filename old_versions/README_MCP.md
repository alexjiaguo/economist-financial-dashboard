## Finance MCP setup (Cursor)

This workspace includes a `.cursor/mcp.json` with a confirmed Alpha Vantage MCP server and placeholders for other providers referenced in the InsightBig article.

### 1) Environment variables

Export these before starting Cursor so `${...}` placeholders resolve:

```bash
export ALPHAVANTAGE_API_KEY="your_alpha_vantage_key"
export FINANCIAL_DATASETS_MCP_URL="https://<provider>/mcp"            # placeholder
export FINANCIAL_DATASETS_API_KEY="your_financialdatasets_key"        # placeholder
export ALPACA_MCP_URL="https://<provider>/mcp"                        # placeholder
export ALPACA_API_KEY="your_alpaca_key"                               # placeholder
export ALPACA_API_SECRET="your_alpaca_secret"                         # placeholder
export OCTAGONAI_MCP_URL="https://<provider>/mcp"                     # placeholder
export OCTAGONAI_API_KEY="your_octagonai_key"                         # placeholder
export YAHOO_FINANCE_MCP_URL="https://<provider>/mcp"                 # placeholder
```

Notes:
- Alpha Vantage supports a first‑party remote URL: `https://mcp.alphavantage.co/mcp?apikey=...`.
- The other four are placeholders until you have a verified MCP server URL or command for each.

### 2) Cursor MCP config

` .cursor/mcp.json` currently contains:

```json
{
  "mcpServers": {
    "alphavantage": {
      "url": "https://mcp.alphavantage.co/mcp?apikey=${ALPHAVANTAGE_API_KEY}"
    },
    "financialdatasets": {
      "url": "${FINANCIAL_DATASETS_MCP_URL}",
      "headers": {
        "Authorization": "Bearer ${FINANCIAL_DATASETS_API_KEY}"
      }
    },
    "alpaca": {
      "url": "${ALPACA_MCP_URL}",
      "headers": {
        "APCA-API-KEY-ID": "${ALPACA_API_KEY}",
        "APCA-API-SECRET-KEY": "${ALPACA_API_SECRET}"
      }
    },
    "octagonai": {
      "url": "${OCTAGONAI_MCP_URL}",
      "headers": {
        "Authorization": "Bearer ${OCTAGONAI_API_KEY}"
      }
    },
    "yahoofinance": {
      "url": "${YAHOO_FINANCE_MCP_URL}"
    }
  }
}
```

### 3) Quick tests in Cursor

After setting env vars, restart Cursor. Then try prompts like:

- "Use `alphavantage` MCP to get the last daily close for AAPL."
- "Call `alphavantage` technical indicator RSI for MSFT." 

If the other servers are wired up with real URLs, you can try analogous prompts.

### 4) Notes on verification

- Only Alpha Vantage is confirmed with an official remote MCP URL and works without local install.
- For Financial Datasets, Alpaca, Octagon AI, and Yahoo Finance, use their verified MCP URLs or local commands if/when provided by each vendor.
- If you have official endpoints, set the `*_MCP_URL` variables above accordingly. If you need help validating, share the links and I’ll update the config.


