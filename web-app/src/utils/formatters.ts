/**
 * Format a number as currency
 */
export const formatCurrency = (
  amount: number | string,
  currency = "USD",
  decimals = 2
): string => {
  const numAmount = typeof amount === "string" ? parseFloat(amount) : amount;

  if (isNaN(numAmount)) {
    return decimals === 0 ? "$0" : "$0.00";
  }

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(numAmount);
};

/**
 * Format a number with commas
 */
export const formatNumber = (num: number | string, decimals = 0): string => {
  const numValue = typeof num === "string" ? parseFloat(num) : num;

  if (isNaN(numValue)) {
    return "0";
  }

  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(numValue);
};

/**
 * Format a percentage
 */
export const formatPercentage = (
  value: number | string,
  decimals = 1
): string => {
  const numValue = typeof value === "string" ? parseFloat(value) : value;

  if (isNaN(numValue)) {
    return "0%";
  }

  return `${numValue.toFixed(decimals)}%`;
};

/**
 * Format a date string
 */
export const formatDate = (
  dateString: string | Date | null | undefined,
  format: "short" | "long" = "short"
): string => {
  if (!dateString) {
    return "N/A";
  }

  const date =
    typeof dateString === "string" ? new Date(dateString) : dateString;

  if (isNaN(date.getTime())) {
    return "Invalid date";
  }

  if (format === "short") {
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }).format(date);
  }

  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(date);
};

/**
 * Format a compact number (e.g., 1.2K, 3.4M)
 */
export const formatCompactNumber = (num: number): string => {
  if (isNaN(num)) {
    return "0";
  }

  return new Intl.NumberFormat("en-US", {
    notation: "compact",
    compactDisplay: "short",
    maximumFractionDigits: 1,
  }).format(num);
};

/**
 * Get color for positive/negative values
 */
export const getValueColor = (
  value: number
): "success" | "error" | "default" => {
  if (value > 0) return "success";
  if (value < 0) return "error";
  return "default";
};

/**
 * Format transaction type
 */
export const formatTransactionType = (type: string): string => {
  return type.charAt(0).toUpperCase() + type.slice(1).toLowerCase();
};
