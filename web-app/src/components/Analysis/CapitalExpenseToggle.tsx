import { ToggleButton, ToggleButtonGroup, Tooltip } from "@mui/material";
import { BusinessCenter, ShoppingCart } from "@mui/icons-material";

interface CapitalExpenseToggleProps {
  value: "exclude" | "include";
  onChange: (value: "exclude" | "include") => void;
}

function CapitalExpenseToggle({ value, onChange }: CapitalExpenseToggleProps) {
  const handleChange = (
    _event: React.MouseEvent<HTMLElement>,
    newValue: "exclude" | "include" | null
  ) => {
    if (newValue !== null) {
      onChange(newValue);
    }
  };

  return (
    <ToggleButtonGroup
      value={value}
      exclusive
      onChange={handleChange}
      aria-label="capital expense filter"
      size="small"
    >
      <Tooltip title="Show only operating expenses (exclude capital expenses like vehicles, equipment, property)">
        <ToggleButton value="exclude" aria-label="exclude capital expenses">
          <ShoppingCart sx={{ mr: 1, fontSize: 18 }} />
          Operating Only
        </ToggleButton>
      </Tooltip>
      <Tooltip title="Show all expenses including capital expenses (vehicles, equipment, property)">
        <ToggleButton value="include" aria-label="include capital expenses">
          <BusinessCenter sx={{ mr: 1, fontSize: 18 }} />
          All Expenses
        </ToggleButton>
      </Tooltip>
    </ToggleButtonGroup>
  );
}

export default CapitalExpenseToggle;
