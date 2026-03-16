/**
 * TypeScript types for account-related data structures
 */

export type AccountType =
  | 'checking'
  | 'savings'
  | 'brokerage'
  | 'investment'
  | 'credit_card'
  | 'loan'
  | '401k'
  | 'ira'
  | 'other';

export type BalanceType = 'statement' | 'calculated' | 'reconciled';

export interface Account {
  account_id: number;
  account_name: string;
  account_type: AccountType;
  account_subtype?: string;
  institution_name?: string;
  account_number_last4?: string;
  currency: string;
  is_active: boolean;
  has_cash_component: boolean;
  has_investment_component: boolean;
  opening_balance: number;
  opening_balance_date?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  // Current balance info (if available)
  current_balance?: number;
  current_balance_date?: string;
  cash_balance?: number;
  investment_value?: number;
  // Linked provider info
  link_type?: 'manual' | 'plaid' | 'akoya';
  linked_provider_id?: number;
}

export interface AccountCreate {
  account_name: string;
  account_type: AccountType;
  account_subtype?: string;
  institution_name?: string;
  account_number_last4?: string;
  currency?: string;
  opening_balance?: number;
  opening_balance_date?: string;
  notes?: string;
}

export interface AccountUpdate {
  account_name?: string;
  account_subtype?: string;
  institution_name?: string;
  account_number_last4?: string;
  is_active?: boolean;
  notes?: string;
}

export interface AccountSummary {
  account_id: number;
  account_name: string;
  account_type: string;
  institution?: string;
  current_balance: number;
  balance_date?: string;
  has_cash: boolean;
  has_investments: boolean;
  cash_balance?: number;
  investment_value?: number;
}

export interface Balance {
  balance_id: number;
  account_id: number;
  balance_date: string;
  total_balance: number;
  balance_type: BalanceType;
  cash_balance?: number;
  investment_value?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface BalanceCreate {
  balance_date: string;
  total_balance: number;
  balance_type?: BalanceType;
  cash_balance?: number;
  investment_value?: number;
  notes?: string;
}

export interface BalanceHistory {
  account_id: number;
  account_name: string;
  balances: Balance[];
  start_date?: string;
  end_date?: string;
}

export interface InvestmentHolding {
  holding_id: number;
  account_id: number;
  symbol: string;
  description?: string;
  quantity: number;
  cost_basis?: number;
  current_value?: number;
  as_of_date: string;
  asset_class?: string;
  sector?: string;
  created_at: string;
  updated_at: string;
  // Calculated fields
  gain_loss?: number;
  gain_loss_percent?: number;
}

export interface HoldingCreate {
  symbol: string;
  quantity: number;
  as_of_date: string;
  description?: string;
  cost_basis?: number;
  current_value?: number;
  asset_class?: string;
  sector?: string;
}

export interface PortfolioSummary {
  account_id: number;
  account_name: string;
  total_value: number;
  total_cost_basis?: number;
  total_gain_loss?: number;
  holdings: InvestmentHolding[];
  as_of_date: string;
}

export interface Reconciliation {
  reconciliation_id: number;
  account_id: number;
  statement_date: string;
  statement_balance: number;
  calculated_balance: number;
  statement_cash_balance?: number;
  calculated_cash_balance?: number;
  statement_investment_value?: number;
  calculated_investment_value?: number;
  discrepancy_amount?: number;
  is_reconciled: boolean;
  reconciled_at?: string;
  reconciled_by?: string;
  transactions_cleared_count: number;
  transactions_pending_count: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface ReconciliationCreate {
  statement_date: string;
  statement_balance: number;
  statement_cash_balance?: number;
  statement_investment_value?: number;
  notes?: string;
}

export interface NetWorth {
  assets: number | string;
  liabilities: number | string;
  investments: number | string;
  // Support both snake_case (API) and camelCase (SDK) formats
  net_worth?: number | string;
  netWorth?: number | string;
  liquid_assets?: number | string;
  liquidAssets?: number | string;
  as_of_date?: string;
  asOfDate?: string;
  account_breakdown?: Record<string, number | string>;
  accountBreakdown?: Record<string, number | string>;
}

// Helper functions for account types
export const getAccountTypeLabel = (type: AccountType): string => {
  const labels: Record<AccountType, string> = {
    checking: 'Checking',
    savings: 'Savings',
    brokerage: 'Brokerage',
    investment: 'Investment',
    credit_card: 'Credit Card',
    loan: 'Loan',
    '401k': '401(k)',
    ira: 'IRA',
    other: 'Other',
  };
  return labels[type] || type;
};

export const getAccountTypeIcon = (type: AccountType): string => {
  const icons: Record<AccountType, string> = {
    checking: '🏦',
    savings: '💰',
    brokerage: '📈',
    investment: '📊',
    credit_card: '💳',
    loan: '🏠',
    '401k': '🏢',
    ira: '📋',
    other: '📁',
  };
  return icons[type] || '📁';
};

export const isAssetAccount = (type: AccountType): boolean => {
  return !['credit_card', 'loan'].includes(type);
};

export const isLiabilityAccount = (type: AccountType): boolean => {
  return ['credit_card', 'loan'].includes(type);
};