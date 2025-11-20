import { test, expect } from '@playwright/test';

test.describe('Capital Expense Rule - Complete Test', () => {

  test('should verify and apply capital expense rule', async ({ request }) => {
    console.log('\n=== STEP 1: Test Rule via API ===');

    // Test the rule to see how many transactions match
    const testRuleResponse = await request.post('http://localhost:8000/api/classification-rules/test', {
      data: {
        category_pattern: '100 S Stratford Maint',
        amount_max: -2000,
        amount_min: null,
      }
    });

    const testResult = await testRuleResponse.json();
    console.log(`✓ Test Rule Result: ${testResult.matching_transactions} transactions match`);
    console.log(`  Sample IDs: ${testResult.sample_transaction_ids.slice(0, 5).join(', ')}...`);

    expect(testResult.matching_transactions).toBeGreaterThan(0);

    console.log('\n=== STEP 2: Get Transactions Before Classification ===');

    // Get all transactions with this category
    const beforeResponse = await request.get('http://localhost:8000/api/transactions', {
      params: {
        search_text: '100 S Stratford Maint',
        limit: 100
      }
    });

    const beforeData = await beforeResponse.json();
    console.log(`✓ Found ${beforeData.total} total transactions with "100 S Stratford Maint" category`);

    // Count unclassified transactions >= $2000
    const unclassifiedBefore = beforeData.transactions.filter((t: any) =>
      t.amount <= -2000 && (!t.classification || t.classification.classification_name !== 'Capital Expense')
    );
    console.log(`  Unclassified expenses >= $2000: ${unclassifiedBefore.length}`);
    console.log('  Examples:');
    unclassifiedBefore.slice(0, 5).forEach((t: any) => {
      console.log(`    - ${t.transaction_date}: $${t.amount} (${t.classification?.classification_name || 'Unclassified'})`);
    });

    console.log('\n=== STEP 3: Apply Classification Rules ===');

    // Apply the rule (dry run first)
    const dryRunResponse = await request.post('http://localhost:8000/api/classification-rules/apply', {
      data: {
        dry_run: true,
        rule_ids: [24] // The rule ID we just fixed
      }
    });

    const dryRunResult = await dryRunResponse.json();
    console.log(`✓ Dry Run Result:`);
    console.log(`  Rules Processed: ${dryRunResult.total_rules_processed}`);
    console.log(`  Transactions Would Be Updated: ${dryRunResult.total_transactions_updated}`);
    dryRunResult.rules_applied.forEach((rule: any) => {
      console.log(`  - ${rule.rule_name}: ${rule.transactions_matched} matched`);
    });

    expect(dryRunResult.total_transactions_updated).toBeGreaterThan(0);

    // Actually apply the rule
    console.log('\n=== STEP 4: Applying Rules (For Real) ===');
    const applyResponse = await request.post('http://localhost:8000/api/classification-rules/apply', {
      data: {
        dry_run: false,
        rule_ids: [24]
      }
    });

    const applyResult = await applyResponse.json();
    console.log(`✓ Apply Result:`);
    console.log(`  Total Transactions Updated: ${applyResult.total_transactions_updated}`);
    applyResult.rules_applied.forEach((rule: any) => {
      console.log(`  - ${rule.rule_name} (${rule.classification_name}): ${rule.transactions_matched} matched`);
    });

    console.log('\n=== STEP 5: Verify Transactions After Classification ===');

    // Get transactions again
    const afterResponse = await request.get('http://localhost:8000/api/transactions', {
      params: {
        search_text: '100 S Stratford Maint',
        limit: 100
      }
    });

    const afterData = await afterResponse.json();

    // Count classified transactions
    const classifiedAfter = afterData.transactions.filter((t: any) =>
      t.amount <= -2000 && t.classification?.classification_name === 'Capital Expense'
    );

    const unclassifiedAfter = afterData.transactions.filter((t: any) =>
      t.amount <= -2000 && (!t.classification || t.classification.classification_name !== 'Capital Expense')
    );

    console.log(`✓ After Classification:`);
    console.log(`  Total transactions: ${afterData.total}`);
    console.log(`  Expenses >= $2000 classified as Capital Expense: ${classifiedAfter.length}`);
    console.log(`  Expenses >= $2000 still unclassified: ${unclassifiedAfter.length}`);

    // Show the large transactions that should be classified
    console.log('\n  Large expenses now classified:');
    const largeClassified = classifiedAfter.filter((t: any) => t.amount <= -10000).slice(0, 10);
    largeClassified.forEach((t: any) => {
      console.log(`    ✓ ${t.transaction_date}: $${t.amount.toLocaleString()} - ${t.classification.classification_name}`);
    });

    if (unclassifiedAfter.length > 0) {
      console.log('\n  ⚠️  Large expenses still unclassified:');
      unclassifiedAfter.slice(0, 5).forEach((t: any) => {
        console.log(`    - ${t.transaction_date}: $${t.amount.toLocaleString()}`);
      });
    }

    // Verify success
    expect(classifiedAfter.length).toBeGreaterThan(unclassifiedBefore.length - 5);
    expect(unclassifiedAfter.length).toBeLessThan(unclassifiedBefore.length);

    console.log('\n=== TEST COMPLETE ===');
    console.log(`✓ Successfully classified ${applyResult.total_transactions_updated} transactions`);
  });
});
