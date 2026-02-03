/**
 * Floating Action Button for AI Assistant.
 *
 * Persistent chat bubble in bottom-right corner that opens the chat panel.
 */

import { useState, useEffect } from "react";
import { Fab, Badge, Tooltip, Zoom, useTheme } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import ChatPanel from "./ChatPanel";
import { checkHealth } from "../../api/assistant";

interface AssistantFABProps {
  /** Number of pending insights to show as badge */
  insightCount?: number;
}

export function AssistantFAB({ insightCount = 0 }: AssistantFABProps) {
  const theme = useTheme();
  const [open, setOpen] = useState(false);
  const [isConfigured, setIsConfigured] = useState<boolean | null>(null);

  // Check if the assistant is configured on mount
  useEffect(() => {
    checkHealth()
      .then((health) => {
        setIsConfigured(health.llm_configured);
      })
      .catch(() => {
        setIsConfigured(false);
      });
  }, []);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  // Handle keyboard shortcut (Cmd+K or Ctrl+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setOpen((prev) => !prev);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Don't render if not configured (optional: show setup prompt instead)
  const tooltipTitle = isConfigured
    ? "Ask Minty (Cmd+K)"
    : "AI Assistant not configured. Set OPENAI_API_KEY to enable.";

  return (
    <>
      <Zoom in={!open}>
        <Tooltip title={tooltipTitle} placement="left">
          <Fab
            color="primary"
            onClick={handleOpen}
            disabled={isConfigured === false}
            sx={{
              position: "fixed",
              bottom: 24,
              right: 24,
              zIndex: theme.zIndex.drawer - 1,
              bgcolor: "success.main",
              "&:hover": {
                bgcolor: "success.dark",
              },
              "&.Mui-disabled": {
                bgcolor: "grey.400",
              },
            }}
          >
            <Badge
              badgeContent={insightCount}
              color="error"
              invisible={insightCount === 0}
            >
              <SmartToyIcon />
            </Badge>
          </Fab>
        </Tooltip>
      </Zoom>

      <ChatPanel open={open} onClose={handleClose} />
    </>
  );
}

export default AssistantFAB;
