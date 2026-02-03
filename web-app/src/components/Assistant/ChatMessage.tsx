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
import PersonIcon from "@mui/icons-material/Person";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import { useNavigate } from "react-router-dom";
import type { ChatMessage as ChatMessageType } from "../../hooks/useAssistant";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const navigate = useNavigate();
  const isUser = message.role === "user";

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
        {/* Avatar */}
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
            flexShrink: 0,
          }}
        >
          {isUser ? (
            <PersonIcon fontSize="small" />
          ) : (
            <SmartToyIcon fontSize="small" />
          )}
        </Box>

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

          {/* Tool calls indicator */}
          {message.toolCalls && message.toolCalls.length > 0 && (
            <Stack direction="row" spacing={0.5} sx={{ mt: 1 }} flexWrap="wrap">
              {message.toolCalls.map((tc) => (
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
