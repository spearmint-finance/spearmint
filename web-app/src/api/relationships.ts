/**
 * API client for Transaction Relationships
 */

import apiClient from "./client";
import type {
  DividendReinvestmentPairsResponse,
  TransferPairsResponse,
  CreditCardPairsResponse,
  ReimbursementPairsResponse,
  DetectAllRelationshipsResponse,
  DetectRelationshipsParams,
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

  const response = await apiClient.post<DividendReinvestmentPairsResponse>(
    "/relationships/detect/dividend-reinvestments",
    null,
    {
      params: {
        date_tolerance_days,
        amount_tolerance,
        auto_link,
      },
    }
  );
  return response.data;
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

  const response = await apiClient.post<TransferPairsResponse>(
    "/relationships/detect/transfers",
    null,
    {
      params: {
        date_tolerance_days,
        amount_tolerance,
        auto_link,
      },
    }
  );
  return response.data;
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

  const response = await apiClient.post<CreditCardPairsResponse>(
    "/relationships/detect/credit-cards",
    null,
    {
      params: {
        date_tolerance_days,
        amount_tolerance,
        auto_link,
      },
    }
  );
  return response.data;
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

  const response = await apiClient.post<ReimbursementPairsResponse>(
    "/relationships/detect/reimbursements",
    null,
    {
      params: {
        date_tolerance_days,
        amount_tolerance,
        auto_link,
      },
    }
  );
  return response.data;
};

/**
 * Detect all relationship types
 */
export const detectAllRelationships = async (
  params: DetectRelationshipsParams = {}
): Promise<DetectAllRelationshipsResponse> => {
  const { auto_link = true } = params;

  const response = await apiClient.post<DetectAllRelationshipsResponse>(
    "/relationships/detect/all",
    null,
    {
      params: {
        auto_link,
      },
    }
  );
  return response.data;
};

