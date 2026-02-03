/**
 * MCP Server Entry Point
 *
 * Starts the MCP server with HTTP/SSE transport for remote connections,
 * or stdio for local Claude Desktop integration.
 */

import express, { Request, Response } from "express";
import cors from "cors";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { createMCPServer, runStdioServer } from "./server.js";
import { authMiddleware, AuthenticatedRequest } from "./middleware/auth.js";

const PORT = parseInt(process.env.MCP_PORT || "3001", 10);
const MODE = process.env.MCP_MODE || "http"; // "http" or "stdio"

/**
 * Start HTTP/SSE server for remote MCP connections
 */
async function runHttpServer(): Promise<void> {
  const app = express();

  // Middleware
  app.use(cors());
  app.use(express.json());

  // Health check endpoint (no auth required)
  app.get("/health", (_req: Request, res: Response) => {
    res.json({
      status: "healthy",
      service: "spearmint-mcp-server",
      version: "0.0.1",
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
      try {
        // Import tools directly for the listing
        const {
          getFinancialSummaryTool,
          getExpenseBreakdownTool,
          searchTransactionsTool,
          getAccountBalancesTool,
          getCashflowTrendTool,
        } = await import("./tools/index.js");

        res.json({
          tools: [
            getFinancialSummaryTool,
            getExpenseBreakdownTool,
            searchTransactionsTool,
            getAccountBalancesTool,
            getCashflowTrendTool,
          ],
        });
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Unknown error";
        res.status(500).json({ error: errorMessage });
      }
    }
  );

  // Execute a tool directly (REST API fallback)
  app.post(
    "/tools/:toolName",
    authMiddleware,
    async (req: AuthenticatedRequest, res: Response) => {
      const { toolName } = req.params;
      const args = req.body;

      try {
        let result: unknown;

        switch (toolName) {
          case "get_financial_summary": {
            const { executeFinancialSummary } = await import(
              "./tools/financial.js"
            );
            result = await executeFinancialSummary(args);
            break;
          }

          case "get_expense_breakdown": {
            const { executeExpenseBreakdown } = await import(
              "./tools/expenses.js"
            );
            result = await executeExpenseBreakdown(args);
            break;
          }

          case "search_transactions": {
            const { executeSearchTransactions } = await import(
              "./tools/transactions.js"
            );
            result = await executeSearchTransactions(args);
            break;
          }

          case "get_account_balances": {
            const { executeGetAccountBalances } = await import(
              "./tools/accounts.js"
            );
            result = await executeGetAccountBalances(args);
            break;
          }

          case "get_cashflow_trend": {
            const { executeGetCashflowTrend } = await import(
              "./tools/cashflow.js"
            );
            result = await executeGetCashflowTrend(args);
            break;
          }

          default:
            res.status(404).json({ error: `Unknown tool: ${toolName}` });
            return;
        }

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
