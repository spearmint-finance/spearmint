import { useState } from "react";
import {
  Box,
  Stack,
  Typography,
  TextField,
  Button,
  MenuItem,
  Paper,
  Divider,
} from "@mui/material";
import { previewScenario, type ScenarioAdjusterIn, type ScenarioPreviewResponse } from "../../api/scenarios";
import ScenarioResults from "./ScenarioResults";

export default function ScenarioBuilder() {
  const [startingBalance, setStartingBalance] = useState<number>(1000);
  const [horizon, setHorizon] = useState<number>(6);
  const [adjusterType, setAdjusterType] = useState<string>("");
  const [percent, setPercent] = useState<number>(20);
  const [months, setMonths] = useState<number>(3);
  const [personId, setPersonId] = useState<number | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScenarioPreviewResponse | null>(null);

  const buildAdjuster = (): ScenarioAdjusterIn[] => {
    if (!adjusterType) return [];
    if (adjusterType === "income_reduction") {
      return [{ type: "income_reduction", params: { percent, months } }];
    }
    if (adjusterType === "job_loss") {
      return [{ type: "job_loss", target_person_id: personId ?? null }];
    }
    return [];
  };

  const onPreview = async () => {
    setLoading(true);
    try {
      const data = await previewScenario({
        adjusters: buildAdjuster(),
        horizon_months: horizon,
        starting_balance: startingBalance,
        shared_expense_strategy: "equal_split",
      });
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Scenarios (Preview)
      </Typography>
      <Paper sx={{ p: 2 }}>
        <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
          <TextField
            type="number"
            label="Starting Balance"
            value={startingBalance}
            onChange={(e) => setStartingBalance(parseFloat(e.target.value))}
            inputProps={{ step: 100 }}
          />
          <TextField
            type="number"
            label="Horizon (months)"
            value={horizon}
            onChange={(e) => setHorizon(parseInt(e.target.value || "0", 10))}
          />
          <TextField
            select
            label="Adjuster"
            value={adjusterType}
            onChange={(e) => setAdjusterType(e.target.value)}
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="">None</MenuItem>
            <MenuItem value="income_reduction">Income Reduction</MenuItem>
            <MenuItem value="job_loss">Job Loss (person)</MenuItem>
          </TextField>
          {adjusterType === "income_reduction" && (
            <>
              <TextField
                type="number"
                label="Percent %"
                value={percent}
                onChange={(e) => setPercent(parseFloat(e.target.value))}
              />
              <TextField
                type="number"
                label="Months"
                value={months}
                onChange={(e) => setMonths(parseInt(e.target.value || "0", 10))}
              />
            </>
          )}
          {adjusterType === "job_loss" && (
            <TextField
              type="number"
              label="Person ID"
              value={personId ?? ""}
              onChange={(e) => setPersonId(parseInt(e.target.value || "0", 10))}
            />
          )}
          <Button variant="contained" onClick={onPreview} disabled={loading}>
            {loading ? "Previewing..." : "Preview"}
          </Button>
        </Stack>
      </Paper>

      <Divider sx={{ my: 3 }} />

      {result && <ScenarioResults result={result} />}
    </Box>
  );
}

