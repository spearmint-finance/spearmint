/**
 * React hook for AI Financial Assistant.
 *
 * Provides state management for chat messages, streaming responses,
 * and action handling.
 */

import { useState, useCallback, useRef, useEffect } from "react";
import { useLocation } from "react-router-dom";
import {
  streamChat,
  type ChatContext,
  type SSEEvent,
  type ActionCard,
  type ActionProposal,
} from "../api/assistant";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
  actionCard?: ActionCard;
  actionProposal?: ActionProposal;
  toolCalls?: Array<{
    id: string;
    name: string;
    arguments: Record<string, unknown>;
    result?: Record<string, unknown>;
  }>;
}

interface UseAssistantOptions {
  onError?: (error: Error) => void;
  onActionProposed?: (proposal: ActionProposal) => void;
}

interface UseAssistantReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  conversationId: string | null;
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
  startNewConversation: () => void;
}

/**
 * Generate a unique ID for messages.
 */
function generateId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Hook for interacting with the AI Financial Assistant.
 */
export function useAssistant(
  options: UseAssistantOptions = {}
): UseAssistantReturn {
  const { onError, onActionProposed } = options;
  const location = useLocation();

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);

  // Ref to track if we should abort streaming
  const abortRef = useRef(false);

  /**
   * Build context from current page state.
   */
  const buildContext = useCallback((): ChatContext => {
    const searchParams = new URLSearchParams(location.search);
    const activeFilters: Record<string, string> = {};

    searchParams.forEach((value, key) => {
      activeFilters[key] = value;
    });

    return {
      current_page: location.pathname,
      active_filters:
        Object.keys(activeFilters).length > 0 ? activeFilters : undefined,
    };
  }, [location]);

  /**
   * Send a message to the assistant.
   */
  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      setError(null);
      setIsLoading(true);
      abortRef.current = false;

      // Add user message
      const userMessage: ChatMessage = {
        id: generateId(),
        role: "user",
        content: content.trim(),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Create placeholder for assistant message
      const assistantMessageId = generateId();
      setMessages((prev) => [
        ...prev,
        {
          id: assistantMessageId,
          role: "assistant",
          content: "",
          timestamp: new Date(),
          isStreaming: true,
        },
      ]);

      try {
        const context = buildContext();

        for await (const event of streamChat({
          message: content.trim(),
          conversation_id: conversationId || undefined,
          context,
        })) {
          if (abortRef.current) break;

          handleSSEEvent(event, assistantMessageId);
        }
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "An error occurred";
        setError(errorMessage);
        onError?.(err instanceof Error ? err : new Error(errorMessage));

        // Update message to show error
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMessageId
              ? {
                  ...m,
                  content:
                    m.content ||
                    "Sorry, I encountered an error. Please try again.",
                  isStreaming: false,
                }
              : m
          )
        );
      } finally {
        setIsLoading(false);
        // Mark streaming as complete
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMessageId ? { ...m, isStreaming: false } : m
          )
        );
      }
    },
    [conversationId, isLoading, buildContext, onError]
  );

  /**
   * Handle SSE events from the stream.
   */
  const handleSSEEvent = useCallback(
    (event: SSEEvent, messageId: string) => {
      switch (event.event) {
        case "conversation_id":
          setConversationId(event.data.id as string);
          break;

        case "content_delta":
          setMessages((prev) =>
            prev.map((m) =>
              m.id === messageId
                ? { ...m, content: m.content + (event.data.delta as string) }
                : m
            )
          );
          break;

        case "tool_call":
          setMessages((prev) =>
            prev.map((m) =>
              m.id === messageId
                ? {
                    ...m,
                    toolCalls: [
                      ...(m.toolCalls || []),
                      {
                        id: event.data.id as string,
                        name: event.data.name as string,
                        arguments: event.data.arguments as Record<
                          string,
                          unknown
                        >,
                      },
                    ],
                  }
                : m
            )
          );
          break;

        case "tool_result":
          setMessages((prev) =>
            prev.map((m) => {
              if (m.id !== messageId || !m.toolCalls) return m;

              const updatedToolCalls = m.toolCalls.map((tc) =>
                tc.name === event.data.tool
                  ? {
                      ...tc,
                      result: event.data.result as Record<string, unknown>,
                    }
                  : tc
              );

              return { ...m, toolCalls: updatedToolCalls };
            })
          );
          break;

        case "action_card":
          setMessages((prev) =>
            prev.map((m) =>
              m.id === messageId
                ? { ...m, actionCard: event.data as unknown as ActionCard }
                : m
            )
          );
          break;

        case "action_proposal":
          const proposal = event.data as unknown as ActionProposal;
          setMessages((prev) =>
            prev.map((m) =>
              m.id === messageId ? { ...m, actionProposal: proposal } : m
            )
          );
          onActionProposed?.(proposal);
          break;

        case "error":
          setError(event.data.message as string);
          break;

        case "message_complete":
          // Message is complete, streaming will be marked false in finally block
          break;
      }
    },
    [onActionProposed]
  );

  /**
   * Clear all messages and start fresh.
   */
  const clearMessages = useCallback(() => {
    abortRef.current = true;
    setMessages([]);
    setError(null);
  }, []);

  /**
   * Start a new conversation.
   */
  const startNewConversation = useCallback(() => {
    clearMessages();
    setConversationId(null);
  }, [clearMessages]);

  return {
    messages,
    isLoading,
    error,
    conversationId,
    sendMessage,
    clearMessages,
    startNewConversation,
  };
}

export default useAssistant;
