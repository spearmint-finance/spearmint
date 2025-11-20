import { ToggleButton, ToggleButtonGroup, Tooltip, Box } from "@mui/material";
import { ShoppingCart, BusinessCenter, SwapHoriz } from "@mui/icons-material";

export type ExpenseView = "operating" | "with-capital" | "all";

interface ExpenseViewToggleProps {
  value: ExpenseView;
  onChange: (value: ExpenseView) => void;
}

function ExpenseViewToggle({ value, onChange }: ExpenseViewToggleProps) {
  const handleChange = (
    _event: React.MouseEvent<HTMLElement>,
    newValue: ExpenseView | null
  ) => {
    if (newValue !== null) {
      onChange(newValue);
    }
  };

  return (
    <Box>
      <ToggleButtonGroup
        value={value}
        exclusive
        onChange={handleChange}
        aria-label="expense view mode"
        size="small"
      >
        <Tooltip title="Operating expenses only - excludes capital expenses AND transfers">
          <ToggleButton value="operating" aria-label="operating expenses only">
            <ShoppingCart sx={{ mr: 0.5, fontSize: 18 }} />
            Operating
          </ToggleButton>
        </Tooltip>

        <Tooltip title="Operating + Capital expenses - excludes transfers but shows asset purchases">
          <ToggleButton value="with-capital" aria-label="with capital expenses">
            <BusinessCenter sx={{ mr: 0.5, fontSize: 18 }} />
            + Capital
          </ToggleButton>
        </Tooltip>

        <Tooltip title="All transactions including transfers">
          <ToggleButton value="all" aria-label="all transactions">
            <SwapHoriz sx={{ mr: 0.5, fontSize: 18 }} />
            All
          </ToggleButton>
        </Tooltip>
      </ToggleButtonGroup>
    </Box>
  );
}

export default ExpenseViewToggle;
