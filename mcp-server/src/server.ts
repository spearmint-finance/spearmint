/**
 * MCP Server Configuration
 *
 * Configures and initializes the Model Context Protocol server
 * with all available tools for AI agent integration.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

import {
  getFinancialSummaryTool,
  getExpenseBreakdownTool,
  searchTransactionsTool,
  getAccountBalancesTool,
  getCashflowTrendTool,
  TOOL_NAMES,
} from "./tools/index.js";

import { executeFinancialSummary } from "./tools/financial.js";
import { executeExpenseBreakdown } from "./tools/expenses.js";
import { executeSearchTransactions } from "./tools/transactions.js";
import { executeGetAccountBalances } from "./tools/accounts.js";
import { executeGetCashflowTrend } from "./tools/cashflow.js";

/**
 * Create and configure the MCP server
 */
export function createMCPServer(): Server {
  const server = new Server(
    {
      name: "spearmint-finance",
      version: "0.0.1",
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // Register tool listing handler
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        getFinancialSummaryTool,
        getExpenseBreakdownTool,
        searchTransactionsTool,
        getAccountBalancesTool,
        getCashflowTrendTool,
      ],
    };
  });

  // Register tool execution handler
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      let result: unknown;

      switch (name) {
        case TOOL_NAMES.FINANCIAL_SUMMARY:
          result = await executeFinancialSummary(args || {});
          break;

        case TOOL_NAMES.EXPENSE_BREAKDOWN:
          result = await executeExpenseBreakdown(args || {});
          break;

        case TOOL_NAMES.SEARCH_TRANSACTIONS:
          result = await executeSearchTransactions(args || {});
          break;

        case TOOL_NAMES.ACCOUNT_BALANCES:
          result = await executeGetAccountBalances(args || {});
          break;

        case TOOL_NAMES.CASHFLOW_TREND:
          result = await executeGetCashflowTrend(args || {});
          break;

        default:
          throw new Error(`Unknown tool: ${name}`);
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error occurred";

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: errorMessage }),
          },
        ],
        isError: true,
      };
    }
  });

  return server;
}

/**
 * Run the MCP server with stdio transport
 */
export async function runStdioServer(): Promise<void> {
  const server = createMCPServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Spearmint MCP server running on stdio");
}
