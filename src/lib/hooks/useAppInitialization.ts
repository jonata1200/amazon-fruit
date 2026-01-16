// src/lib/hooks/useAppInitialization.ts
import { useEffect, useRef } from 'react';
import { useAppStore } from '@/store';
import { useDateRange } from './useDashboards';

// Função para obter valores padrão de data (últimos 30 dias)
function getDefaultDateRange() {
  const end = new Date();
  const start = new Date();
  start.setDate(start.getDate() - 30);

  return {
    min_date: start.toISOString().split('T')[0],
    max_date: end.toISOString().split('T')[0],
  };
}

export function useAppInitialization() {
  const setDateRange = useAppStore((state) => state.setDateRange);
  const currentDateRange = useAppStore((state) => state.dateRange);
  const { data: dateRangeData, isError } = useDateRange();
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const hasInitializedRef = useRef(false);

  useEffect(() => {
    // Se conseguir dados da API, usar eles
    if (dateRangeData) {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
      setDateRange(dateRangeData.min_date, dateRangeData.max_date);
      hasInitializedRef.current = true;
    } else if (isError && !hasInitializedRef.current) {
      // Se houver erro na API e não tiver dateRange no store, usar valores padrão
      if (!currentDateRange.start && !currentDateRange.end) {
        const defaultRange = getDefaultDateRange();
        setDateRange(defaultRange.min_date, defaultRange.max_date);
        hasInitializedRef.current = true;
      }
    } else if (!hasInitializedRef.current && !timeoutRef.current) {
      // Timeout de 3 segundos: se a API não responder, usar valores padrão
      timeoutRef.current = setTimeout(() => {
        if (!currentDateRange.start && !currentDateRange.end && !dateRangeData) {
          const defaultRange = getDefaultDateRange();
          setDateRange(defaultRange.min_date, defaultRange.max_date);
          hasInitializedRef.current = true;
        }
        timeoutRef.current = null;
      }, 3000);
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
    };
  }, [dateRangeData, isError, setDateRange, currentDateRange]);

  // Está pronto se tem valores no store (seja da API ou padrão definidos)
  // O Zustand atualiza o currentDateRange imediatamente após setDateRange
  const hasDateRange = !!currentDateRange.start && !!currentDateRange.end;
  
  return {
    isReady: hasDateRange,
  };
}
