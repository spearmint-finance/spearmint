/**
 * Authentication middleware for MCP server
 *
 * Validates API keys against the Spearmint API backend
 */

import { Request, Response, NextFunction } from "express";

const SPEARMINT_API_URL =
  process.env.SPEARMINT_API_URL || "http://localhost:8000";

export interface AuthenticatedRequest extends Request {
  apiKeyId?: number;
  apiKeyName?: string;
}

interface ValidateResponse {
  valid: boolean;
  key_id?: number;
  name?: string;
  message?: string;
}

/**
 * Extract API key from request
 */
function extractApiKey(req: Request): string | null {
  // Check Authorization header (Bearer token)
  const authHeader = req.headers.authorization;
  if (authHeader?.startsWith("Bearer ")) {
    return authHeader.slice(7);
  }

  // Check X-API-Key header
  const apiKeyHeader = req.headers["x-api-key"];
  if (typeof apiKeyHeader === "string") {
    return apiKeyHeader;
  }

  // Check query parameter (for SSE connections)
  const apiKeyQuery = req.query.api_key;
  if (typeof apiKeyQuery === "string") {
    return apiKeyQuery;
  }

  return null;
}

/**
 * Validate API key against Spearmint API
 */
async function validateApiKey(
  key: string
): Promise<ValidateResponse> {
  try {
    const response = await fetch(
      `${SPEARMINT_API_URL}/api/auth/api-keys/validate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ key }),
      }
    );

    if (!response.ok) {
      return { valid: false, message: "Failed to validate API key" };
    }

    return (await response.json()) as ValidateResponse;
  } catch (error) {
    console.error("Error validating API key:", error);
    return { valid: false, message: "Authentication service unavailable" };
  }
}

/**
 * Authentication middleware
 *
 * Validates the API key and attaches key info to the request
 */
export async function authMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  const apiKey = extractApiKey(req);

  if (!apiKey) {
    res.status(401).json({
      error: "Unauthorized",
      message: "API key required. Provide via Authorization header, X-API-Key header, or api_key query parameter.",
    });
    return;
  }

  const validation = await validateApiKey(apiKey);

  if (!validation.valid) {
    res.status(401).json({
      error: "Unauthorized",
      message: validation.message || "Invalid API key",
    });
    return;
  }

  // Attach key info to request
  req.apiKeyId = validation.key_id;
  req.apiKeyName = validation.name;

  next();
}

/**
 * Optional auth middleware - doesn't fail if no key provided
 * Useful for health checks that should work without auth
 */
export async function optionalAuthMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  const apiKey = extractApiKey(req);

  if (apiKey) {
    const validation = await validateApiKey(apiKey);
    if (validation.valid) {
      req.apiKeyId = validation.key_id;
      req.apiKeyName = validation.name;
    }
  }

  next();
}
