import apiClient from "./client";

export type ScenarioAdjusterIn = {
  type: "job_loss" | "income_reduction" | "expense_change" | "one_time";
  target_person_id?: number | null;
  params?: Record<string, any>;
  start_date?: string | null; // YYYY-MM-DD
  end_date?: string | null;   // YYYY-MM-DD
};

export type ScenarioPreviewRequest = {
  adjusters: ScenarioAdjusterIn[];
  horizon_months: number;
  starting_balance?: number;
  shared_expense_strategy?: "equal_split" | "household";
};

export type SeriesPoint = {
  date: string;
  income: number;
  expenses: number;
  net_cf: number;
};

export type ScenarioKPIs = {
  runway_months: number | null;
  min_balance: number;
  coverage_by_person: Record<string, number>;
};

export type ScenarioPreviewResponse = {
  baseline_series: SeriesPoint[];
  scenario_series: SeriesPoint[];
  kpis: ScenarioKPIs;
  deltas: { income: number; expenses: number; net_cf: number };
  generated_at: string;
};

export async function previewScenario(payload: ScenarioPreviewRequest) {
  const { data } = await apiClient.post<ScenarioPreviewResponse>(
    "/scenarios/preview",
    payload
  );
  return data;
}

