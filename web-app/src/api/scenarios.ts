export type ScenarioAdjusterIn = {
  type: "job_loss" | "income_reduction" | "expense_change" | "one_time";
  target_person_id?: number | null;
  params?: Record<string, any>;
  start_date?: string | null; // YYYY-MM-DD
  end_date?: string | null; // YYYY-MM-DD
};

export type ScenarioPreviewRequest = {
  adjusters: ScenarioAdjusterIn[];
  horizon_months: number;
  starting_balance?: number;
  shared_expense_strategy?: "equal_split" | "household";
};

export type SeriesPoint = {
  date: string;
  income: string;
  expenses: string;
  net_cf: string;
  by_person?: Record<string, Record<string, string>> | null;
};

export type ScenarioKPIs = {
  runway_months: number | null;
  min_balance: string;
  coverage_by_person: Record<string, number>;
  monthly_shortfall_by_person?: Record<string, string> | null;
};

export type ScenarioPreviewResponse = {
  baseline_series: SeriesPoint[];
  scenario_series: SeriesPoint[];
  kpis: ScenarioKPIs;
  deltas: Record<string, string>;
  generated_at: string;
};

export async function previewScenario(payload: ScenarioPreviewRequest): Promise<ScenarioPreviewResponse> {
  const resp = await fetch("/api/scenarios/preview", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!resp.ok) {
    throw new Error(`Scenario preview failed: ${resp.status}`);
  }
  return resp.json();
}
