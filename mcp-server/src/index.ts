/**
 * MCP Server Entry Point
 *
 * Starts the MCP server with HTTP/SSE transport for remote connections,
 * or stdio for local Claude Desktop integration.
 */

import express, { Request, Response } from "express";
import cors from "cors";
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

  // SSE endpoint for MCP connections
  app.get("/sse", authMiddleware, (req: AuthenticatedRequest, res: Response) => {
    console.log(`MCP SSE connection from key: ${req.apiKeyName}`);

    // Set SSE headers
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    res.setHeader("X-Accel-Buffering", "no");

    // Send initial connection event
    res.write(
      `data: ${JSON.stringify({
        type: "connection",
        status: "connected",
        server: "spearmint-finance",
        version: "0.0.1",
      })}\n\n`
    );

    // Keep connection alive
    const keepAlive = setInterval(() => {
      res.write(": keepalive\n\n");
    }, 30000);

    // Handle client disconnect
    req.on("close", () => {
      console.log(`MCP SSE connection closed for key: ${req.apiKeyName}`);
      clearInterval(keepAlive);
    });
  });

  // MCP message endpoint
  app.post(
    "/message",
    authMiddleware,
    async (req: AuthenticatedRequest, res: Response) => {
      console.log(`MCP message from key: ${req.apiKeyName}`);

      try {
        // For now, return tools list as a basic response
        // Full MCP protocol handling would go here
        const server = createMCPServer();

        res.json({
          success: true,
          message: "MCP message received",
          // In a full implementation, this would process the MCP protocol message
        });
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Unknown error";
        res.status(500).json({ error: errorMessage });
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
