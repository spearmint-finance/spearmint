/**
 * Chat message component for AI Assistant.
 *
 * Displays user and assistant messages with appropriate styling,
 * action cards, and loading indicators.
 */

import {
  Box,
  Typography,
  Paper,
  Button,
  CircularProgress,
  Chip,
  Stack,
} from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import SavingsIcon from "@mui/icons-material/Savings";
import PersonIcon from "@mui/icons-material/Person";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import Tooltip from "@mui/material/Tooltip";
import { useNavigate } from "react-router-dom";
import type { ChatMessage as ChatMessageType } from "../../hooks/useAssistant";

// Map of agent tool names to their display metadata
const AGENT_TOOLS: Record<string, { label: string; color: string }> = {
  get_budget_advice: { label: "Budget Advisor", color: "#7b1fa2" },
};

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const navigate = useNavigate();
  const isUser = message.role === "user";

  // Check if any tool calls used an agent
  const agentCalls = message.toolCalls?.filter((tc) => tc.name in AGENT_TOOLS) || [];
  const usedAgent = !isUser && agentCalls.length > 0;

  const handleNavigate = (url: string) => {
    navigate(url);
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        mb: 2,
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: isUser ? "row-reverse" : "row",
          alignItems: "flex-start",
          maxWidth: "85%",
          gap: 1,
        }}
      >
        {/* Avatars */}
        <Stack direction="column" spacing={0.5} sx={{ flexShrink: 0 }}>
          {/* Primary avatar */}
          <Tooltip title={isUser ? "You" : "Minty"} placement="left">
            <Box
              sx={{
                width: 32,
                height: 32,
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                bgcolor: isUser ? "primary.main" : "success.main",
                color: "white",
              }}
            >
              {isUser ? (
                <PersonIcon fontSize="small" />
              ) : (
                <SmartToyIcon fontSize="small" />
              )}
            </Box>
          </Tooltip>

          {/* Agent avatar — shown when a specialized agent contributed */}
          {usedAgent &&
            agentCalls.map((tc) => {
              const agent = AGENT_TOOLS[tc.name];
              return (
                <Tooltip key={tc.id} title={agent.label} placement="left">
                  <Box
                    sx={{
                      width: 28,
                      height: 28,
                      borderRadius: "50%",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      bgcolor: agent.color,
                      color: "white",
                      border: "2px solid",
                      borderColor: "background.paper",
                    }}
                  >
                    <SavingsIcon sx={{ fontSize: 16 }} />
                  </Box>
                </Tooltip>
              );
            })}
        </Stack>

        {/* Message content */}
        <Paper
          elevation={1}
          sx={{
            p: 1.5,
            bgcolor: isUser ? "primary.main" : "background.paper",
            color: isUser ? "primary.contrastText" : "text.primary",
            borderRadius: 2,
            borderTopRightRadius: isUser ? 0 : 2,
            borderTopLeftRadius: isUser ? 2 : 0,
          }}
        >
          {/* Agent attribution banner */}
          {usedAgent && (
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 0.75,
                mb: 1,
                pb: 0.75,
                borderBottom: "1px solid",
                borderColor: "divider",
              }}
            >
              <SavingsIcon sx={{ fontSize: 14, color: "#7b1fa2" }} />
              <Typography
                variant="caption"
                sx={{ fontWeight: 600, color: "#7b1fa2", fontStyle: "italic" }}
              >
                Buddy the Budget Advisor says...
              </Typography>
            </Box>
          )}

          {/* Message text */}
          {message.content ? (
            <Typography
              variant="body2"
              sx={{
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
              }}
            >
              {message.content}
            </Typography>
          ) : message.isStreaming ? (
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <CircularProgress size={16} />
              <Typography variant="body2" color="text.secondary">
                Thinking...
              </Typography>
            </Box>
          ) : null}

          {/* Tool calls indicator (non-agent tools only — agents show as avatars) */}
          {message.toolCalls && message.toolCalls.filter((tc) => !(tc.name in AGENT_TOOLS)).length > 0 && (
            <Stack direction="row" spacing={0.5} sx={{ mt: 1 }} flexWrap="wrap" useFlexGap>
              {message.toolCalls
                .filter((tc) => !(tc.name in AGENT_TOOLS))
                .map((tc) => (
                  <Chip
                    key={tc.id}
                    label={tc.name.replace(/_/g, " ")}
                    size="small"
                    variant="outlined"
                    sx={{ fontSize: "0.7rem" }}
                  />
                ))}
            </Stack>
          )}

          {/* Action card */}
          {message.actionCard && (
            <Box sx={{ mt: 1.5 }}>
              <Button
                variant="outlined"
                size="small"
                endIcon={<OpenInNewIcon fontSize="small" />}
                onClick={() =>
                  message.actionCard?.url &&
                  handleNavigate(message.actionCard.url)
                }
                sx={{
                  textTransform: "none",
                  borderColor: isUser
                    ? "rgba(255,255,255,0.5)"
                    : "primary.main",
                  color: isUser ? "inherit" : "primary.main",
                }}
              >
                {message.actionCard.label}
              </Button>
            </Box>
          )}

          {/* Action proposal */}
          {message.actionProposal && (
            <Box
              sx={{
                mt: 1.5,
                p: 1.5,
                bgcolor: "action.hover",
                borderRadius: 1,
              }}
            >
              <Typography variant="subtitle2" gutterBottom>
                Proposed Action: {message.actionProposal.action}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {message.actionProposal.preview?.transaction_count && (
                  <>
                    {message.actionProposal.preview.transaction_count as number}{" "}
                    transactions will be affected
                  </>
                )}
              </Typography>
              <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                <Button variant="contained" size="small" color="primary">
                  Confirm
                </Button>
                <Button variant="outlined" size="small">
                  Cancel
                </Button>
              </Stack>
            </Box>
          )}

          {/* Timestamp */}
          <Typography
            variant="caption"
            sx={{
              display: "block",
              mt: 0.5,
              opacity: 0.7,
              fontSize: "0.65rem",
            }}
          >
            {message.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
}

export default ChatMessage;
