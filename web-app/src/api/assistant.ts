/**
 * API client for AI Financial Assistant.
 *
 * Handles SSE streaming for chat and REST endpoints for conversations.
 */

const baseUrl =
  import.meta.env.VITE_API_URL ||
  (typeof window !== "undefined"
    ? window.location.origin
    : "http://localhost:8080");

// Types
export interface ChatContext {
  current_page?: string;
  selected_transaction_id?: number;
  active_filters?: Record<string, string>;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  context?: ChatContext;
}

export interface Conversation {
  id: string;
  title: string | null;
  message_count: number;
  total_tokens: number;
  created_at: string | null;
  updated_at: string | null;
  is_archived: boolean;
}

export interface Message {
  role: "user" | "assistant" | "system" | "tool";
  content: string;
  tool_calls?: ToolCall[];
  tool_call_id?: string;
}

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
}

export interface ActionCard {
  type: "navigation" | "action";
  url?: string;
  label: string;
}

export interface ActionProposal {
  type: "action_proposal";
  action: string;
  requires_confirmation: boolean;
  preview: Record<string, unknown>;
  payload: Record<string, unknown>;
}

export interface Insight {
  id: string;
  insight_type: string;
  priority: number;
  title: string;
  content: string;
  action_type?: string;
  action_payload?: Record<string, unknown>;
  created_at: string;
}

export interface HealthStatus {
  status: "ok" | "unconfigured";
  llm_configured: boolean;
  llm_provider: string;
  llm_model: string;
}

// SSE Event Types
export type SSEEventType =
  | "conversation_id"
  | "content_delta"
  | "tool_call"
  | "tool_result"
  | "action_proposal"
  | "action_card"
  | "message_complete"
  | "error";

export interface SSEEvent {
  event: SSEEventType;
  data: Record<string, unknown>;
}

/**
 * Stream chat response using Server-Sent Events.
 */
export async function* streamChat(
  request: ChatRequest
): AsyncGenerator<SSEEvent, void, unknown> {
  const response = await fetch(`${baseUrl}/api/assistant/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.statusText}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error("No response body");
  }

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    let currentEvent = "";
    let currentData = "";

    for (const line of lines) {
      if (line.startsWith("event: ")) {
        currentEvent = line.slice(7);
      } else if (line.startsWith("data: ")) {
        currentData = line.slice(6);
        if (currentEvent && currentData) {
          try {
            yield {
              event: currentEvent as SSEEventType,
              data: JSON.parse(currentData),
            };
          } catch {
            console.error("Failed to parse SSE data:", currentData);
          }
          currentEvent = "";
          currentData = "";
        }
      }
    }
  }
}

/**
 * List conversations.
 */
export async function listConversations(
  limit = 20,
  includeArchived = false
): Promise<Conversation[]> {
  const params = new URLSearchParams({
    limit: limit.toString(),
    include_archived: includeArchived.toString(),
  });

  const response = await fetch(
    `${baseUrl}/api/assistant/conversations?${params}`
  );

  if (!response.ok) {
    throw new Error(`Failed to list conversations: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get messages for a conversation.
 */
export async function getConversationMessages(
  conversationId: string,
  limit = 50
): Promise<{ conversation_id: string; messages: Message[] }> {
  const params = new URLSearchParams({ limit: limit.toString() });

  const response = await fetch(
    `${baseUrl}/api/assistant/conversations/${conversationId}/messages?${params}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get messages: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Archive a conversation.
 */
export async function archiveConversation(
  conversationId: string
): Promise<{ success: boolean; message: string }> {
  const response = await fetch(
    `${baseUrl}/api/assistant/conversations/${conversationId}/archive`,
    { method: "POST" }
  );

  if (!response.ok) {
    throw new Error(`Failed to archive conversation: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Delete a conversation.
 */
export async function deleteConversation(
  conversationId: string
): Promise<{ success: boolean; message: string }> {
  const response = await fetch(
    `${baseUrl}/api/assistant/conversations/${conversationId}`,
    { method: "DELETE" }
  );

  if (!response.ok) {
    throw new Error(`Failed to delete conversation: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Execute a confirmed action.
 */
export async function executeAction(
  messageId: string,
  actionType: string,
  payload: Record<string, unknown>
): Promise<{
  success: boolean;
  message: string;
  action_log_id: string;
  undo_available: boolean;
}> {
  const response = await fetch(`${baseUrl}/api/assistant/actions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message_id: messageId,
      action_type: actionType,
      confirmed: true,
      payload,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to execute action: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Undo an action.
 */
export async function undoAction(
  actionLogId: string
): Promise<{ success: boolean; message: string }> {
  const response = await fetch(`${baseUrl}/api/assistant/actions/undo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action_log_id: actionLogId }),
  });

  if (!response.ok) {
    throw new Error(`Failed to undo action: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get pending insights.
 */
export async function getInsights(limit = 10): Promise<Insight[]> {
  const params = new URLSearchParams({ limit: limit.toString() });

  const response = await fetch(`${baseUrl}/api/assistant/insights?${params}`);

  if (!response.ok) {
    throw new Error(`Failed to get insights: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Dismiss an insight.
 */
export async function dismissInsight(
  insightId: string
): Promise<{ success: boolean; message: string }> {
  const response = await fetch(
    `${baseUrl}/api/assistant/insights/${insightId}/dismiss`,
    { method: "POST" }
  );

  if (!response.ok) {
    throw new Error(`Failed to dismiss insight: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Check assistant health.
 */
export async function checkHealth(): Promise<HealthStatus> {
  const response = await fetch(`${baseUrl}/api/assistant/health`);

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }

  return response.json();
}
