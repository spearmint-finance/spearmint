/**
 * Test data fixtures for E2E tests
 */

export const testTransactions = {
  income: {
    description: 'Test Salary Payment',
    amount: 5000,
    transaction_type: 'Income' as const,
    date: '2025-10-01',
    notes: 'Monthly salary for testing',
  },
  expense: {
    description: 'Test Grocery Shopping',
    amount: 150.50,
    transaction_type: 'Expense' as const,
    date: '2025-10-02',
    notes: 'Weekly groceries',
  },
  largeExpense: {
    description: 'Test Rent Payment',
    amount: 1500,
    transaction_type: 'Expense' as const,
    date: '2025-10-01',
    notes: 'Monthly rent',
  },
};

export const invalidTransactions = {
  emptyDescription: {
    description: '',
    amount: 100,
    transaction_type: 'Expense' as const,
    date: '2025-10-01',
  },
  shortDescription: {
    description: 'AB',
    amount: 100,
    transaction_type: 'Expense' as const,
    date: '2025-10-01',
  },
  zeroAmount: {
    description: 'Test Transaction',
    amount: 0,
    transaction_type: 'Expense' as const,
    date: '2025-10-01',
  },
  negativeAmount: {
    description: 'Test Transaction',
    amount: -50,
    transaction_type: 'Expense' as const,
    date: '2025-10-01',
  },
};

export const searchQueries = {
  salary: 'Salary',
  grocery: 'Grocery',
  rent: 'Rent',
  nonExistent: 'XYZ123NonExistent',
};

export const expectedValidationMessages = {
  descriptionRequired: 'Description is required',
  descriptionTooShort: 'Description must be at least 3 characters',
  amountRequired: 'Amount is required',
  amountTooSmall: 'Amount must be greater than 0',
};

/**
 * Generate a unique transaction description for testing
 */
export function generateUniqueDescription(prefix: string = 'Test'): string {
  const timestamp = Date.now();
  return `${prefix} Transaction ${timestamp}`;
}

/**
 * Generate test transaction with unique description
 */
export function generateTestTransaction(type: 'Income' | 'Expense' = 'Expense') {
  return {
    description: generateUniqueDescription(type),
    amount: Math.floor(Math.random() * 1000) + 50,
    transaction_type: type,
    date: new Date().toISOString().split('T')[0],
    notes: `Auto-generated test ${type.toLowerCase()}`,
  };
}

