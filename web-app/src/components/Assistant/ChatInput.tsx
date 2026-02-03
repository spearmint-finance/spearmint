/**
 * Chat input component for AI Assistant.
 *
 * Text input with send button and suggested prompts.
 */

import { useState, KeyboardEvent } from "react";
import {
  Box,
  TextField,
  IconButton,
  Chip,
  Stack,
  InputAdornment,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

const SUGGESTED_PROMPTS = [
  "How much did I spend this month?",
  "What are my top expenses?",
  "Show uncategorized transactions",
  "Compare to last month",
];

export function ChatInput({
  onSend,
  disabled = false,
  placeholder = "Ask Minty anything...",
}: ChatInputProps) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestedPrompt = (prompt: string) => {
    if (!disabled) {
      onSend(prompt);
    }
  };

  return (
    <Box>
      {/* Suggested prompts */}
      <Stack
        direction="row"
        spacing={0.5}
        sx={{
          mb: 1,
          flexWrap: "wrap",
          gap: 0.5,
        }}
      >
        {SUGGESTED_PROMPTS.slice(0, 2).map((prompt) => (
          <Chip
            key={prompt}
            label={prompt}
            size="small"
            variant="outlined"
            onClick={() => handleSuggestedPrompt(prompt)}
            disabled={disabled}
            sx={{
              fontSize: "0.7rem",
              height: 24,
              cursor: "pointer",
              "&:hover": {
                bgcolor: "action.hover",
              },
            }}
          />
        ))}
      </Stack>

      {/* Input field */}
      <TextField
        fullWidth
        multiline
        maxRows={4}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        size="small"
        sx={{
          "& .MuiOutlinedInput-root": {
            borderRadius: 2,
            bgcolor: "background.paper",
          },
        }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                onClick={handleSend}
                disabled={disabled || !input.trim()}
                color="primary"
                size="small"
              >
                <SendIcon fontSize="small" />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    </Box>
  );
}

export default ChatInput;
