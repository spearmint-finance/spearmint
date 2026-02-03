# MCP Server Setup Guide

This guide explains how to configure AI assistants (Claude, Gemini, ChatGPT) to interact with your Spearmint Finance data using the Model Context Protocol (MCP) server.

## Overview

The MCP server enables AI assistants to:
- Query your financial summary
- Analyze expense breakdowns by category
- Search and filter transactions
- Check account balances
- View cash flow trends

## Prerequisites

1. Spearmint Finance running (either locally or via Docker)
2. An API key generated from Settings > API Keys

## Step 1: Generate an API Key

1. Open Spearmint Finance in your browser
2. Navigate to **Settings** > **API Keys**
3. Click **Generate New Key**
4. Enter a descriptive name (e.g., "Claude Desktop")
5. **Copy the API key immediately** - it won't be shown again
6. Optionally, copy the pre-generated configuration for your AI assistant

## Step 2: Configure Your AI Assistant

### Claude Desktop

1. Open Claude Desktop's configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the Spearmint MCP server configuration:

```json
{
  "mcpServers": {
    "spearmint": {
      "command": "npx",
      "args": ["-y", "supergateway", "--sse", "http://localhost:3001/sse"],
      "env": {
        "SPEARMINT_API_KEY": "smint_live_your_key_here"
      }
    }
  }
}
```

3. Restart Claude Desktop

4. Test by asking: "What's my financial summary for this month?"

### Gemini CLI

1. Set environment variables:

```bash
export SPEARMINT_API_KEY=smint_live_your_key_here
export SPEARMINT_MCP_URL=http://localhost:3001
```

2. Or add to your shell profile (`~/.bashrc`, `~/.zshrc`):

```bash
# Spearmint Finance MCP
export SPEARMINT_API_KEY=smint_live_your_key_here
export SPEARMINT_MCP_URL=http://localhost:3001
```

### ChatGPT (via Actions)

For ChatGPT with custom GPT actions:

1. Create a new GPT or edit an existing one
2. Add an action with the following configuration:

```json
{
  "name": "Spearmint Finance",
  "url": "http://localhost:3001",
  "headers": {
    "Authorization": "Bearer smint_live_your_key_here"
  }
}
```

**Note**: ChatGPT requires a publicly accessible URL. For local development, use a tunnel service like ngrok or Tailscale Funnel.

## Remote Access Options

### Option 1: ngrok (Quick Testing)

1. Install ngrok: https://ngrok.com/download

2. Start a tunnel:
```bash
ngrok http 3001
```

3. Use the provided ngrok URL (e.g., `https://abc123.ngrok.io`) in your configuration

### Option 2: Tailscale Funnel (Recommended for Personal Use)

1. Install Tailscale: https://tailscale.com/download

2. Enable Funnel:
```bash
tailscale funnel 3001
```

3. Use your Tailscale Funnel URL in configurations

### Option 3: Cloudflare Tunnel

1. Install cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/

2. Create a tunnel:
```bash
cloudflared tunnel --url http://localhost:3001
```

## Available MCP Tools

The following tools are available to AI assistants:

### `get_financial_summary`
Get a comprehensive financial summary including total income, expenses, and net cash flow.

**Parameters:**
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)

### `get_expense_breakdown`
Get expenses organized by category with percentages and averages.

**Parameters:**
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `limit` (optional): Maximum categories to return

### `search_transactions`
Search and filter transactions with various criteria.

**Parameters:**
- `start_date`, `end_date`: Date range
- `transaction_type`: "Income" or "Expense"
- `category_id`: Filter by category
- `search`: Text search in description
- `min_amount`, `max_amount`: Amount range
- `limit`, `offset`: Pagination

### `get_account_balances`
Get current balances for all financial accounts.

**Parameters:**
- `account_type` (optional): Filter by type (checking, savings, etc.)
- `active_only` (optional): Only active accounts (default: true)

### `get_cashflow_trend`
Get cash flow trends over time.

**Parameters:**
- `period`: "daily", "weekly", "monthly", "quarterly", "yearly"
- `start_date`, `end_date`: Date range

## Troubleshooting

### "Failed to validate API key"
- Ensure the API key is correct and hasn't been revoked
- Check that the Spearmint API is running on port 8000
- Verify the MCP server can reach the API (check SPEARMINT_API_URL)

### "Connection refused"
- Ensure the MCP server is running on port 3001
- Check Docker logs: `docker logs spearmint-mcp-server`
- Verify the port is not blocked by a firewall

### Claude Desktop doesn't show Spearmint tools
- Restart Claude Desktop after configuration changes
- Check the configuration file syntax (valid JSON)
- Look for errors in Claude Desktop's developer console

### SSE connection drops
- This is normal for long-running connections
- The AI assistant should reconnect automatically
- Consider using a more stable tunnel service

## Security Considerations

1. **Keep API keys secret** - Never commit them to version control
2. **Use HTTPS** for remote access - ngrok and Tailscale provide this automatically
3. **Revoke unused keys** - Remove keys that are no longer needed from Settings > API Keys
4. **Monitor usage** - Check "Last Used" dates in the API Keys list

## Docker Deployment

When running with Docker Compose:

```bash
docker-compose up -d
```

The MCP server will be available at `http://localhost:3001`.

For production deployments behind a reverse proxy, update `SPEARMINT_API_URL` to use the internal Docker network hostname:

```yaml
environment:
  - SPEARMINT_API_URL=http://core-api:8000
```

## Getting Help

- Check the [API documentation](/api/docs) for endpoint details
- Review logs: `docker logs spearmint-mcp-server`
- Report issues: https://github.com/spearmint-finance/spearmint/issues
