// src/lib/hooks/useAppInitialization.ts
import { useEffect } from 'react';
import { useAppStore } from '@/store';
import { useDateRange } from './useDashboards';

export function useAppInitialization() {
  const setDateRange = useAppStore((state) => state.setDateRange);
  const { data: dateRangeData } = useDateRange();

  useEffect(() => {
    if (dateRangeData) {
      setDateRange(dateRangeData.min_date, dateRangeData.max_date);
    }
  }, [dateRangeData, setDateRange]);

  return {
    isReady: !!dateRangeData,
  };
}
