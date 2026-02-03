/**
 * MCP Server Configuration
 *
 * Configures and initializes the Model Context Protocol server
 * with all available tools for AI agent integration.
 *
 * Tools are auto-generated from the OpenAPI spec.
 * Run `npm run generate:tools` to regenerate after API changes.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Import generated tools
import {
  getFinancialSummaryTool,
  executeGetFinancialSummary,
  getExpenseBreakdownTool,
  executeGetExpenseBreakdown,
  searchTransactionsTool,
  executeSearchTransactions,
  getAccountBalancesTool,
  executeGetAccountBalances,
  getCashflowTrendTool,
  executeGetCashflowTrend,
  getIncomeBreakdownTool,
  executeGetIncomeBreakdown,
  getSpendingTrendTool,
  executeGetSpendingTrend,
  getFinancialHealthTool,
  executeGetFinancialHealth,
  GENERATED_TOOL_NAMES,
} from "./tools/generated/index.js";

// All available tools
const ALL_TOOLS = [
  getFinancialSummaryTool,
  getExpenseBreakdownTool,
  searchTransactionsTool,
  getAccountBalancesTool,
  getCashflowTrendTool,
  getIncomeBreakdownTool,
  getSpendingTrendTool,
  getFinancialHealthTool,
];

// Tool executor map for cleaner dispatch
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const TOOL_EXECUTORS: Record<string, (args: any) => Promise<unknown>> = {
  [GENERATED_TOOL_NAMES.GET_FINANCIAL_SUMMARY]: executeGetFinancialSummary,
  [GENERATED_TOOL_NAMES.GET_EXPENSE_BREAKDOWN]: executeGetExpenseBreakdown,
  [GENERATED_TOOL_NAMES.SEARCH_TRANSACTIONS]: executeSearchTransactions,
  [GENERATED_TOOL_NAMES.GET_ACCOUNT_BALANCES]: executeGetAccountBalances,
  [GENERATED_TOOL_NAMES.GET_CASHFLOW_TREND]: executeGetCashflowTrend,
  [GENERATED_TOOL_NAMES.GET_INCOME_BREAKDOWN]: executeGetIncomeBreakdown,
  [GENERATED_TOOL_NAMES.GET_SPENDING_TREND]: executeGetSpendingTrend,
  [GENERATED_TOOL_NAMES.GET_FINANCIAL_HEALTH]: executeGetFinancialHealth,
};

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
      tools: ALL_TOOLS,
    };
  });

  // Register tool execution handler
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      const executor = TOOL_EXECUTORS[name];

      if (!executor) {
        throw new Error(`Unknown tool: ${name}`);
      }

      const result = await executor(args || {});

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

// Re-export for backward compatibility
export { GENERATED_TOOL_NAMES as TOOL_NAMES };
