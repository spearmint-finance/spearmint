import { ToggleButton, ToggleButtonGroup, Tooltip } from "@mui/material";
import AssessmentIcon from "@mui/icons-material/Assessment";
import ListAltIcon from "@mui/icons-material/ListAlt";

interface ViewModeToggleProps {
  value: "analysis" | "complete";
  onChange: (mode: "analysis" | "complete") => void;
}

function ViewModeToggle({ value, onChange }: ViewModeToggleProps) {
  const handleChange = (
    _event: React.MouseEvent<HTMLElement>,
    newMode: "analysis" | "complete" | null
  ) => {
    if (newMode !== null) {
      onChange(newMode);
    }
  };

  return (
    <ToggleButtonGroup
      value={value}
      exclusive
      onChange={handleChange}
      aria-label="view mode"
      size="small"
    >
      <ToggleButton value="analysis" aria-label="analysis mode">
        <Tooltip title="Excludes transfers between accounts">
          <AssessmentIcon sx={{ mr: 1 }} fontSize="small" />
        </Tooltip>
        Analysis
      </ToggleButton>
      <ToggleButton value="complete" aria-label="complete mode">
        <Tooltip title="Shows all transactions including transfers">
          <ListAltIcon sx={{ mr: 1 }} fontSize="small" />
        </Tooltip>
        Complete
      </ToggleButton>
    </ToggleButtonGroup>
  );
}

export default ViewModeToggle;
