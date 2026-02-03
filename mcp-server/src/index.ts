/**
 * MCP Server Entry Point
 *
 * Starts the MCP server with HTTP/SSE transport for remote connections,
 * or stdio for local Claude Desktop integration.
 *
 * Tools are auto-generated from the OpenAPI spec.
 * Run `npm run generate:tools` to regenerate after API changes.
 */

import express, { Request, Response } from "express";
import cors from "cors";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { createMCPServer, runStdioServer } from "./server.js";
import { authMiddleware, AuthenticatedRequest } from "./middleware/auth.js";

// Import all generated tools
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

const PORT = parseInt(process.env.MCP_PORT || "3001", 10);
const MODE = process.env.MCP_MODE || "http"; // "http" or "stdio"

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
 * Start HTTP/SSE server for remote MCP connections
 */
async function runHttpServer(): Promise<void> {
  const app = express();

  // Middleware
  app.use(cors());
  // Note: Don't use express.json() globally - /message needs raw body for MCP transport

  // Health check endpoint (no auth required)
  app.get("/health", (_req: Request, res: Response) => {
    res.json({
      status: "healthy",
      service: "spearmint-mcp-server",
      version: "0.0.1",
      tools: ALL_TOOLS.length,
    });
  });

  // Store active transports for message routing
  const transports = new Map<string, SSEServerTransport>();

  // SSE endpoint for MCP connections
  app.get("/sse", authMiddleware, async (req: AuthenticatedRequest, res: Response) => {
    console.log(`MCP SSE connection from key: ${req.apiKeyName}`);

    // Create SSE transport for this connection
    const transport = new SSEServerTransport("/message", res);
    const sessionId = `session-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    transports.set(sessionId, transport);

    // Create and connect MCP server for this session
    const server = createMCPServer();

    // Handle client disconnect
    req.on("close", () => {
      console.log(`MCP SSE connection closed for key: ${req.apiKeyName}`);
      transports.delete(sessionId);
    });

    try {
      await server.connect(transport);
    } catch (error) {
      console.error("Error connecting MCP server:", error);
      transports.delete(sessionId);
    }
  });

  // MCP message endpoint - handles incoming JSON-RPC messages from clients
  app.post(
    "/message",
    authMiddleware,
    async (req: AuthenticatedRequest, res: Response) => {
      console.log(`MCP message from key: ${req.apiKeyName}`);

      // Find an active transport to handle this message
      // In a production setup, you'd want to route to the correct session
      const activeTransports = Array.from(transports.values());
      if (activeTransports.length === 0) {
        res.status(503).json({ error: "No active MCP sessions" });
        return;
      }

      // Use the most recent transport
      const transport = activeTransports[activeTransports.length - 1];

      try {
        // Let the transport handle the incoming message
        await transport.handlePostMessage(req, res);
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Unknown error";
        console.error("Error handling MCP message:", errorMessage);
        if (!res.headersSent) {
          res.status(500).json({ error: errorMessage });
        }
      }
    }
  );

  // List available tools
  app.get(
    "/tools",
    authMiddleware,
    async (_req: AuthenticatedRequest, res: Response) => {
      res.json({ tools: ALL_TOOLS });
    }
  );

  // Execute a tool directly (REST API fallback)
  app.post(
    "/tools/:toolName",
    express.json(),
    authMiddleware,
    async (req: AuthenticatedRequest, res: Response) => {
      const { toolName } = req.params;
      const args = req.body;

      const executor = TOOL_EXECUTORS[toolName];

      if (!executor) {
        res.status(404).json({
          error: `Unknown tool: ${toolName}`,
          availableTools: Object.keys(TOOL_EXECUTORS),
        });
        return;
      }

      try {
        const result = await executor(args);
        res.json(result);
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Unknown error";
        res.status(500).json({ error: errorMessage });
      }
    }
  );

  // Start server
  app.listen(PORT, () => {
    console.log(`Spearmint MCP server running on http://localhost:${PORT}`);
    console.log(`  - Health check: http://localhost:${PORT}/health`);
    console.log(`  - SSE endpoint: http://localhost:${PORT}/sse`);
    console.log(`  - Tools list:   http://localhost:${PORT}/tools`);
    console.log(`  - Available tools: ${ALL_TOOLS.length}`);
  });
}

/**
 * Main entry point
 */
async function main(): Promise<void> {
  if (MODE === "stdio") {
    await runStdioServer();
  } else {
    await runHttpServer();
  }
}

main().catch((error) => {
  console.error("Failed to start MCP server:", error);
  process.exit(1);
});
