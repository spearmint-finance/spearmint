// Transaction types based on backend API schemas

export interface TransactionSplit {
  split_id: number;
  transaction_id: number;
  amount: number;
  category_id: number;
  category_name?: string;
  entity_id?: number | null;
  description?: string;
  notes?: string;
}

export interface TransactionSplitCreate {
  amount: number;
  category_id: number;
  entity_id?: number | null;
  description?: string;
  notes?: string;
}

export interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number;
  transaction_type: "Income" | "Expense" | "Transfer";
  is_transfer?: boolean;
  balance?: number;
  category_id?: number;
  category_name?: string;
  related_transaction_id?: number;
  account_id?: number;
  source?: string;
  payment_method?: string;
  transfer_account_from?: string;
  transfer_account_to?: string;
  notes?: string;
  tags?: string[];
  is_capital_expense?: boolean;
  is_tax_deductible?: boolean;
  is_recurring?: boolean;
  is_reimbursable?: boolean;
  exclude_from_income?: boolean;
  exclude_from_expenses?: boolean;
  entity_id?: number | null;
  splits?: TransactionSplit[];
  split_portion?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface TransactionCreate {
  date: string;
  description: string;
  amount: number;
  transaction_type: "Income" | "Expense";
  category_id: number; // Required field
  account_id?: number;
  balance?: number;
  notes?: string;
  tag_names?: string[];
  is_capital_expense?: boolean;
  is_tax_deductible?: boolean;
  is_recurring?: boolean;
  is_reimbursable?: boolean;
  exclude_from_income?: boolean;
  exclude_from_expenses?: boolean;
  entity_id?: number | null;
  splits?: TransactionSplitCreate[];
}

export interface TransactionUpdate {
  date?: string;
  description?: string;
  amount?: number;
  transaction_type?: "Income" | "Expense";
  balance?: number;
  category_id?: number;
  account_id?: number;
  notes?: string;
  tag_names?: string[];
  is_capital_expense?: boolean;
  is_tax_deductible?: boolean;
  is_recurring?: boolean;
  is_reimbursable?: boolean;
  exclude_from_income?: boolean;
  exclude_from_expenses?: boolean;
  entity_id?: number | null;
  splits?: TransactionSplitCreate[];
}

export interface TransactionFilter {
  start_date?: string;
  end_date?: string;
  category_id?: number;
  min_amount?: number;
  max_amount?: number;
  search?: string;
  skip?: number;
  limit?: number;
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  limit: number;
  offset: number;
  summary?: {
    total_income: number;
    total_expenses: number;
    net_income: number;
    transaction_count: number;
  };
}
