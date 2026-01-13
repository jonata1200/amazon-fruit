// src/lib/hooks/__tests__/useComparison.test.ts
import { renderHook } from '@testing-library/react';
import { useComparison } from '../useComparison';

describe('useComparison', () => {
  it('calculates percentage change correctly', () => {
    const { result } = renderHook(() => useComparison({ value: 100 }, { value: 80 }));

    const change = result.current.calculateChange(100, 80);
    expect(change).toBe(25);
  });

  it('handles zero previous value', () => {
    const { result } = renderHook(() => useComparison({ value: 100 }, { value: 0 }));

    const change = result.current.calculateChange(100, 0);
    expect(change).toBe(0);
  });

  it('returns correct change type for increase', () => {
    const { result } = renderHook(() => useComparison(null, null));

    expect(result.current.getChangeType(10)).toBe('increase');
  });

  it('returns correct change type for decrease', () => {
    const { result } = renderHook(() => useComparison(null, null));

    expect(result.current.getChangeType(-10)).toBe('decrease');
  });

  it('returns neutral for zero change', () => {
    const { result } = renderHook(() => useComparison(null, null));

    expect(result.current.getChangeType(0)).toBe('neutral');
  });

  it('stores current and previous data', () => {
    const currentData = { value: 100 };
    const previousData = { value: 80 };

    const { result } = renderHook(() => useComparison(currentData, previousData));

    expect(result.current.currentData).toBe(currentData);
    expect(result.current.previousData).toBe(previousData);
  });
});
