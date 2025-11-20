import { test, expect } from '@playwright/test';

test.describe('Expense Analysis - Capital Expense Exclusion', () => {

  test('should exclude capital expenses in analysis mode', async ({ request }) => {
    console.log('\n=== Testing Expense Analysis API ===');

    const startDate = '2025-07-03';
    const endDate = '2025-10-03';

    // Test ANALYSIS mode (should exclude capital expenses)
    console.log('\n--- ANALYSIS Mode (should exclude capital expenses) ---');
    const analysisResponse = await request.get('http://localhost:8000/api/analysis/expenses', {
      params: {
        start_date: startDate,
        end_date: endDate,
        mode: 'analysis'
      }
    });

    const analysisData = await analysisResponse.json();
    console.log(`Total Expenses: $${analysisData.total_expenses}`);
    console.log(`Transaction Count: ${analysisData.transaction_count}`);
    console.log(`Top Categories:`);
    analysisData.breakdown_by_category && Object.entries(analysisData.breakdown_by_category)
      .slice(0, 5)
      .forEach(([cat, data]: [string, any]) => {
        console.log(`  - ${cat}: $${data.total}`);
      });

    // Test COMPLETE mode (should include everything)
    console.log('\n--- COMPLETE Mode (should include all expenses) ---');
    const completeResponse = await request.get('http://localhost:8000/api/analysis/expenses', {
      params: {
        start_date: startDate,
        end_date: endDate,
        mode: 'complete'
      }
    });

    const completeData = await completeResponse.json();
    console.log(`Total Expenses: $${completeData.total_expenses}`);
    console.log(`Transaction Count: ${completeData.transaction_count}`);

    // Calculate difference
    const difference = Math.abs(completeData.total_expenses) - Math.abs(analysisData.total_expenses);
    console.log(`\nDifference (Capital Expenses): $${difference.toFixed(2)}`);

    // Get actual capital expenses for this period
    console.log('\n--- Checking Actual Capital Expenses ---');
    const transactionsResponse = await request.get('http://localhost:8000/api/transactions', {
      params: {
        start_date: startDate,
        end_date: endDate,
        transaction_type: 'Expense',
        classification_id: 22, // Capital Expense
        limit: 100
      }
    });

    const capitalExpenses = await transactionsResponse.json();
    const capitalTotal = capitalExpenses.transactions.reduce((sum: number, t: any) => sum + Number(t.amount), 0);

    console.log(`Capital Expenses Found: ${capitalExpenses.total}`);
    console.log(`Total Capital Expense Amount: $${Number(capitalTotal).toFixed(2)}`);
    console.log(`Examples:`);
    capitalExpenses.transactions.slice(0, 5).forEach((t: any) => {
      console.log(`  - ${t.transaction_date}: $${t.amount} (${t.category?.category_name})`);
    });

    // Verify the difference matches
    console.log(`\n--- Verification ---`);
    console.log(`Expected capital expenses to exclude: $${Math.abs(capitalTotal).toFixed(2)}`);
    console.log(`Actual difference in totals: $${difference.toFixed(2)}`);

    const tolerance = 0.01; // Allow small rounding differences
    const isCorrect = Math.abs(difference - Math.abs(capitalTotal)) < tolerance;

    if (isCorrect) {
      console.log(`✓ PASS: Analysis mode correctly excludes capital expenses`);
    } else {
      console.log(`✗ FAIL: Capital expenses are not being excluded correctly`);
      console.log(`   Difference should be $${Math.abs(capitalTotal).toFixed(2)} but is $${difference.toFixed(2)}`);
    }

    expect(isCorrect).toBe(true);
  });
});
