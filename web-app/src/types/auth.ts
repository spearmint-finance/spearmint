/**
 * TypeScript types for authentication and API key management
 */

export interface APIKey {
  key_id: number;
  name: string;
  key_prefix: string;
  is_active: boolean;
  last_used_at: string | null;
  created_at: string;
  expires_at: string | null;
}

export interface APIKeyCreate {
  name: string;
  expires_at?: string;
}

export interface APIKeyCreated extends APIKey {
  /** Full API key - only shown once at creation time */
  key: string;
}

export interface APIKeyListResponse {
  keys: APIKey[];
  total: number;
}

export interface APIKeyValidateRequest {
  key: string;
}

export interface APIKeyValidateResponse {
  valid: boolean;
  key_id?: number;
  name?: string;
  message?: string;
}

/**
 * MCP client configuration types for different AI agents
 */
export interface MCPClientConfig {
  type: "claude" | "gemini" | "chatgpt";
  displayName: string;
  configFormat: "json" | "env" | "yaml";
}

export const MCP_CLIENTS: MCPClientConfig[] = [
  { type: "claude", displayName: "Claude Desktop", configFormat: "json" },
  { type: "gemini", displayName: "Gemini CLI", configFormat: "env" },
  { type: "chatgpt", displayName: "ChatGPT", configFormat: "json" },
];

/**
 * Generate MCP client configuration for a given API key
 */
export const generateMCPConfig = (
  clientType: MCPClientConfig["type"],
  apiKey: string,
  serverUrl: string = "http://localhost:3001"
): string => {
  switch (clientType) {
    case "claude":
      return JSON.stringify(
        {
          mcpServers: {
            spearmint: {
              command: "npx",
              args: ["-y", "supergateway", "--sse", `${serverUrl}/sse`],
              env: {
                SPEARMINT_API_KEY: apiKey,
              },
            },
          },
        },
        null,
        2
      );

    case "gemini":
      return `# Add to your environment or .env file
SPEARMINT_API_KEY=${apiKey}
SPEARMINT_MCP_URL=${serverUrl}`;

    case "chatgpt":
      return JSON.stringify(
        {
          name: "Spearmint Finance",
          url: serverUrl,
          headers: {
            Authorization: `Bearer ${apiKey}`,
          },
        },
        null,
        2
      );

    default:
      return "";
  }
};
