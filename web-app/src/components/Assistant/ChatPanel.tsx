/**
 * Chat panel component for AI Assistant.
 *
 * Slide-in drawer containing the chat interface.
 */

import { useRef, useEffect } from "react";
import {
  Box,
  Drawer,
  Typography,
  IconButton,
  Divider,
  Alert,
  Stack,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import MinimizeIcon from "@mui/icons-material/Remove";
import AddIcon from "@mui/icons-material/Add";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import { useAssistant } from "../../hooks/useAssistant";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

interface ChatPanelProps {
  open: boolean;
  onClose: () => void;
  onMinimize?: () => void;
}

const DRAWER_WIDTH = 400;

export function ChatPanel({ open, onClose, onMinimize }: ChatPanelProps) {
  const {
    messages,
    isLoading,
    error,
    sendMessage,
    confirmAction,
    dismissAction,
    startNewConversation,
  } = useAssistant();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      sx={{
        "& .MuiDrawer-paper": {
          width: { xs: "100%", sm: DRAWER_WIDTH },
          maxWidth: "100%",
        },
      }}
    >
      <Box
        sx={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Header */}
        <Box
          sx={{
            p: 2,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            bgcolor: "success.main",
            color: "success.contrastText",
          }}
        >
          <Stack direction="row" alignItems="center" spacing={1}>
            <SmartToyIcon />
            <Typography variant="h6" fontWeight="bold">
              Minty
            </Typography>
          </Stack>
          <Stack direction="row" spacing={0.5}>
            <IconButton
              size="small"
              onClick={startNewConversation}
              sx={{ color: "inherit" }}
              title="New conversation"
            >
              <AddIcon fontSize="small" />
            </IconButton>
            {onMinimize && (
              <IconButton
                size="small"
                onClick={onMinimize}
                sx={{ color: "inherit" }}
                title="Minimize"
              >
                <MinimizeIcon fontSize="small" />
              </IconButton>
            )}
            <IconButton
              size="small"
              onClick={onClose}
              sx={{ color: "inherit" }}
              title="Close"
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Stack>
        </Box>

        <Divider />

        {/* Error alert */}
        {error && (
          <Alert severity="error" sx={{ m: 1 }}>
            {error}
          </Alert>
        )}

        {/* Messages area */}
        <Box
          sx={{
            flexGrow: 1,
            overflowY: "auto",
            p: 2,
            bgcolor: "grey.50",
          }}
        >
          {messages.length === 0 ? (
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                height: "100%",
                textAlign: "center",
                p: 3,
              }}
            >
              <SmartToyIcon
                sx={{ fontSize: 64, color: "success.main", mb: 2 }}
              />
              <Typography variant="h6" gutterBottom>
                Hi! I'm Minty
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Your AI financial assistant. Ask me anything about your
                finances, spending patterns, or let me help you categorize
                transactions.
              </Typography>
            </Box>
          ) : (
            <>
              {messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  message={message}
                  onConfirmAction={confirmAction}
                  onDismissAction={dismissAction}
                />
              ))}
              <div ref={messagesEndRef} />
            </>
          )}
        </Box>

        <Divider />

        {/* Input area */}
        <Box sx={{ p: 2, bgcolor: "background.paper" }}>
          <ChatInput onSend={sendMessage} disabled={isLoading} />
        </Box>
      </Box>
    </Drawer>
  );
}

export default ChatPanel;
