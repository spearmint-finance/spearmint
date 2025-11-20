// Analysis types based on backend API schemas

export interface AnalysisSummary {
  total_income: number
  total_expenses: number
  net_cash_flow: number
  transaction_count: number
  average_transaction: number
  income_to_expense_ratio?: number
  savings_rate?: number
}

export interface TrendData {
  period: string
  income: number
  expenses: number
  net_cash_flow: number
  transaction_count: number
}

export interface AnalysisResponse {
  summary: AnalysisSummary
  trends: TrendData[]
  start_date: string
  end_date: string
  period: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly'
  mode: 'analysis' | 'complete'
}

export interface AnalysisRequest {
  start_date?: string
  end_date?: string
  period?: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly'
  mode?: 'analysis' | 'complete'
}

