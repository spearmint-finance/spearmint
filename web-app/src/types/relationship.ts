/**
 * TypeScript types for Transaction Relationships
 */

export interface TransactionSummary {
  transaction_id: number;
  transaction_date: string;
  amount: number;
  transaction_type: "Income" | "Expense";
  description?: string;
  source?: string;
  category_name?: string;
}

export interface DividendReinvestmentPairDetection {
  dividend: TransactionSummary;
  reinvestment: TransactionSummary;
  confidence: number;
  amount_difference: number;
  date_difference_days: number;
  relationship_type: string;
}

export interface DividendReinvestmentPairsResponse {
  count: number;
  high_confidence: number;
  pairs: DividendReinvestmentPairDetection[];
}

export interface TransferPairDetection {
  source_transaction: TransactionSummary;
  destination_transaction: TransactionSummary;
  confidence: number;
  amount_difference: number;
  date_difference_days: number;
  relationship_type: string;
}

export interface TransferPairsResponse {
  count: number;
  high_confidence: number;
  pairs: TransferPairDetection[];
}

export interface CreditCardPairDetection {
  payment: TransactionSummary;
  receipt: TransactionSummary;
  confidence: number;
  amount_difference: number;
  date_difference_days: number;
  relationship_type: string;
}

export interface CreditCardPairsResponse {
  count: number;
  high_confidence: number;
  pairs: CreditCardPairDetection[];
}

export interface ReimbursementPairDetection {
  expense: TransactionSummary;
  reimbursement: TransactionSummary;
  confidence: number;
  amount_difference: number;
  date_difference_days: number;
  relationship_type: string;
}

export interface ReimbursementPairsResponse {
  count: number;
  high_confidence: number;
  pairs: ReimbursementPairDetection[];
}

export interface DetectAllRelationshipsResponse {
  transfer_pairs: TransferPairsResponse;
  credit_card_pairs: CreditCardPairsResponse;
  reimbursement_pairs: ReimbursementPairsResponse;
  dividend_reinvestment_pairs: DividendReinvestmentPairsResponse;
  total_detected: number;
  auto_linked: boolean;
}

export interface DetectRelationshipsParams {
  date_tolerance_days?: number;
  amount_tolerance?: number;
  auto_link?: boolean;
}

