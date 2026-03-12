import { Card, CardContent, Typography, Grid, Stack } from "@mui/material";
import type { ScenarioPreviewResponse } from "../../api/scenarios";

type Props = {
  result: ScenarioPreviewResponse;
};

export default function ScenarioResults({ result }: Props) {
  const k = result.kpis;
  const series = result.scenario_series ?? [];
  const totalNet = series.reduce(
    (acc, p) => acc + parseFloat(p.net_cf || "0"),
    0
  );
  const minBalance = parseFloat(k.min_balance || "0");
  const coverageByPerson = k.coverage_by_person ?? {};

  return (
    <Grid container spacing={2} sx={{ mt: 1 }}>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="subtitle2" color="text.secondary">
              Runway (months)
            </Typography>
            <Typography variant="h5">{k.runway_months ?? "—"}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="subtitle2" color="text.secondary">
              Min Balance
            </Typography>
            <Typography variant="h5">${minBalance.toFixed(2)}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="subtitle2" color="text.secondary">
              Total Net (horizon)
            </Typography>
            <Typography variant="h5">${totalNet.toFixed(2)}</Typography>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>
              Coverage by Person
            </Typography>
            <Stack direction="row" spacing={3}>
              {Object.entries(coverageByPerson).length === 0 && (
                <Typography color="text.secondary">No per-person data yet</Typography>
              )}
              {Object.entries(coverageByPerson).map(([pid, cov]) => (
                <Stack key={pid}>
                  <Typography variant="body2" color="text.secondary">
                    Person {pid}
                  </Typography>
                  <Typography variant="h6">{Number(cov).toFixed(2)}x</Typography>
                </Stack>
              ))}
            </Stack>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
