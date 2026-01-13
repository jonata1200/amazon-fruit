// src/lib/hooks/useComparison.ts
export function useComparison<T = unknown>(currentData: T, previousData: T) {
  const calculateChange = (current: number, previous: number) => {
    if (previous === 0) return 0;
    return ((current - previous) / previous) * 100;
  };

  const getChangeType = (change: number): 'increase' | 'decrease' | 'neutral' => {
    if (change > 0) return 'increase';
    if (change < 0) return 'decrease';
    return 'neutral';
  };

  return {
    calculateChange,
    getChangeType,
    currentData,
    previousData,
  };
}
