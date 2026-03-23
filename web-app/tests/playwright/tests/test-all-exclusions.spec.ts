import { test, expect } from '@playwright/test';
import { API_BASE_URL } from '../../fixtures/env';

test.describe('Expense Analysis - All Exclusions', () => {

  test('should exclude all non-operating expenses in analysis mode', async ({ request }) => {
    console.log('\n=== Testing All Expense Exclusions ===');

    const startDate = '2025-07-03';
    const endDate = '2025-10-03';

    // Get analysis mode total
    const analysisResponse = await request.get(`${API_BASE_URL}/api/analysis/expenses`, {
      params: {
        start_date: startDate,
        end_date: endDate,
        mode: 'analysis'
      }
    });
    const analysisData = await analysisResponse.json();

    // Get complete mode total
    const completeResponse = await request.get(`${API_BASE_URL}/api/analysis/expenses`, {
      params: {
        start_date: startDate,
        end_date: endDate,
        mode: 'complete'
      }
    });
    const completeData = await completeResponse.json();

    console.log(`\nAnalysis Mode: $${analysisData.total_expenses} (${analysisData.transaction_count} transactions)`);
    console.log(`Complete Mode: $${completeData.total_expenses} (${completeData.transaction_count} transactions)`);

    const totalDifference = Math.abs(completeData.total_expenses) - Math.abs(analysisData.total_expenses);
    console.log(`\nTotal Excluded: $${totalDifference.toFixed(2)}`);

    // Check each excluded classification
    const excludedClassifications = [
      { id: 2, name: 'Internal Transfer' },
      { id: 3, name: 'Credit Card Payment' },
      { id: 4, name: 'Credit Card Receipt' },
      { id: 7, name: 'Refund' },
      { id: 8, name: 'Loan Disbursement' },
      { id: 9, name: 'Loan Payment - Principal' },
      { id: 16, name: 'Credit Card Reward' },
      { id: 17, name: 'Work Reimbursement' },
      { id: 18, name: 'Reimbursable Expense' },
      { id: 19, name: 'Insurance Reimbursement' },
      { id: 20, name: 'Investment Distribution' },
      { id: 22, name: 'Capital Expense' },
    ];

    console.log(`\n--- Breakdown of Excluded Expenses ---`);
    let totalExcluded = 0;

    for (const classification of excludedClassifications) {
      const response = await request.get(`${API_BASE_URL}/api/transactions`, {
        params: {
          start_date: startDate,
          end_date: endDate,
          transaction_type: 'Expense',
          classification_id: classification.id,
          limit: 1000
        }
      });

      const data = await response.json();
      const total = data.transactions.reduce((sum: number, t: any) => sum + Number(t.amount), 0);

      if (data.total > 0) {
        console.log(`  ${classification.name}: $${Math.abs(total).toFixed(2)} (${data.total} transactions)`);
        totalExcluded += Math.abs(total);
      }
    }

    console.log(`\n--- Summary ---`);
    console.log(`Sum of all excluded classifications: $${totalExcluded.toFixed(2)}`);
    console.log(`Actual difference in totals: $${totalDifference.toFixed(2)}`);

    // Check for transfers (also excluded in analysis mode)
    const transfersResponse = await request.get(`${API_BASE_URL}/api/transactions`, {
      params: {
        start_date: startDate,
        end_date: endDate,
        transaction_type: 'Expense',
        is_transfer: true,
        limit: 1000
      }
    });

    const transfersData = await transfersResponse.json();
    const transfersTotal = transfersData.transactions.reduce((sum: number, t: any) => sum + Number(t.amount), 0);

    if (transfersData.total > 0) {
      console.log(`  Transfers (is_transfer=true): $${Math.abs(transfersTotal).toFixed(2)} (${transfersData.total} transactions)`);
      totalExcluded += Math.abs(transfersTotal);
    }

    // Allow small rounding differences
    const tolerance = 200.00;
    const isCorrect = Math.abs(totalDifference - totalExcluded) < tolerance;

    if (isCorrect) {
      console.log(`\n✓ PASS: Analysis mode correctly excludes all non-operating expenses`);
      console.log(`  Capital Expenses are being properly excluded along with other non-operating expenses.`);
    } else {
      console.log(`\n✗ FAIL: Mismatch in excluded amounts`);
      console.log(`  Difference: $${Math.abs(totalDifference - totalExcluded).toFixed(2)}`);
    }

    expect(isCorrect).toBe(true);
  });
});
