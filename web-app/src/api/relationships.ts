/**
 * API client for Transaction Relationships
 */

import { relationshipsApi } from "./sdk";
import type {
  DividendReinvestmentPairsResponse,
  TransferPairsResponse,
  CreditCardPairsResponse,
  ReimbursementPairsResponse,
  DetectAllRelationshipsResponse,
  DetectRelationshipsParams,
  TransactionSummary,
} from "../types/relationship";

// ============================================================================
// Relationship Detection Operations
// ============================================================================

/**
 * Detect dividend reinvestment pairs
 */
export const detectDividendReinvestments = async (
  params: DetectRelationshipsParams = {}
): Promise<DividendReinvestmentPairsResponse> => {
  const {
    date_tolerance_days = 1,
    amount_tolerance = 0.01,
    auto_link = true,
  } = params;

  const response =
    await relationshipsApi.detectDividendReinvestmentPairs(
      {
        dateToleranceDays: date_tolerance_days,
        amountTolerance: amount_tolerance,
        autoLink: auto_link,
      }
    );
  return response.data as unknown as DividendReinvestmentPairsResponse;
};

/**
 * Detect transfer pairs
 */
export const detectTransfers = async (
  params: DetectRelationshipsParams = {}
): Promise<TransferPairsResponse> => {
  const {
    date_tolerance_days = 3,
    amount_tolerance = 0.01,
    auto_link = true,
  } = params;

  const response =
    await relationshipsApi.detectTransferPairs(
      {
        dateToleranceDays: date_tolerance_days,
        amountTolerance: amount_tolerance,
        autoLink: auto_link,
      }
    );
  return response.data as unknown as TransferPairsResponse;
};

/**
 * Detect credit card payment/receipt pairs
 */
export const detectCreditCardPairs = async (
  params: DetectRelationshipsParams = {}
): Promise<CreditCardPairsResponse> => {
  const {
    date_tolerance_days = 3,
    amount_tolerance = 0.01,
    auto_link = true,
  } = params;

  const response =
    await relationshipsApi.detectCreditCardPairs(
      {
        dateToleranceDays: date_tolerance_days,
        amountTolerance: amount_tolerance,
        autoLink: auto_link,
      }
    );
  return response.data as unknown as CreditCardPairsResponse;
};

/**
 * Detect reimbursement pairs
 */
export const detectReimbursements = async (
  params: DetectRelationshipsParams = {}
): Promise<ReimbursementPairsResponse> => {
  const {
    date_tolerance_days = 30,
    amount_tolerance = 0.01,
    auto_link = true,
  } = params;

  const response =
    await relationshipsApi.detectReimbursementPairs(
      {
        dateToleranceDays: date_tolerance_days,
        amountTolerance: amount_tolerance,
        autoLink: auto_link,
      }
    );
  return response.data as unknown as ReimbursementPairsResponse;
};

/**
 * Detect all relationship types
 */
export const detectAllRelationships = async (
  params: DetectRelationshipsParams = {}
): Promise<DetectAllRelationshipsResponse> => {
  const { auto_link = true } = params;

  const response =
    await relationshipsApi.detectAllRelationships({
      autoLink: auto_link,
    });
  return response.data as unknown as DetectAllRelationshipsResponse;
};


// ============================================================================
// Related Transaction Lookup
// ============================================================================

export interface RelatedTransactionInfo {
  transaction: TransactionSummary;
  relationship_type: string;
  relationship_description?: string;
}

export interface RelatedTransactionsResponse {
  transaction_id: number;
  related_transactions: RelatedTransactionInfo[];
  count: number;
}

/**
 * Get related transactions for a given transaction ID
 */
export const getRelatedTransactions = async (
  transactionId: number
): Promise<RelatedTransactionsResponse> => {
  const response = await fetch(`/api/transactions/${transactionId}/relationships`);
  if (!response.ok) {
    throw new Error(`Failed to fetch related transactions: ${response.statusText}`);
  }
  return response.json();
};
