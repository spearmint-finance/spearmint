// Transaction types based on backend API schemas

export interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number;
  transaction_type: "Income" | "Expense";
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
