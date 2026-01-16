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
  const lastSetRangeRef = useRef<string>('');

  useEffect(() => {
    // Obter estado atual do store dentro do effect para evitar dependências
    const storeRange = useAppStore.getState().dateRange;
    const hasCurrentRange = !!storeRange.start && !!storeRange.end;
    const currentRangeKey = `${storeRange.start}-${storeRange.end}`;

    // Se já foi inicializado e os valores já estão corretos, não fazer nada
    if (hasInitializedRef.current && hasCurrentRange) {
      return;
    }

    // Se conseguir dados da API e ainda não foram definidos, usar eles
    if (dateRangeData) {
      const apiRangeKey = `${dateRangeData.min_date}-${dateRangeData.max_date}`;
      if (lastSetRangeRef.current !== apiRangeKey) {
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
          timeoutRef.current = null;
        }
        // Só atualizar se o valor for diferente
        if (storeRange.start !== dateRangeData.min_date || storeRange.end !== dateRangeData.max_date) {
          setDateRange(dateRangeData.min_date, dateRangeData.max_date);
        }
        lastSetRangeRef.current = apiRangeKey;
        hasInitializedRef.current = true;
      }
      return;
    }

    // Se houver erro na API e não tiver dateRange no store, usar valores padrão
    if (isError && !hasCurrentRange) {
      const defaultRange = getDefaultDateRange();
      const defaultRangeKey = `${defaultRange.min_date}-${defaultRange.max_date}`;
      if (lastSetRangeRef.current !== defaultRangeKey) {
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
          timeoutRef.current = null;
        }
        setDateRange(defaultRange.min_date, defaultRange.max_date);
        lastSetRangeRef.current = defaultRangeKey;
        hasInitializedRef.current = true;
      }
      return;
    }

    // Timeout de 3 segundos: se a API não responder, usar valores padrão
    if (!hasCurrentRange && !timeoutRef.current && !hasInitializedRef.current) {
      timeoutRef.current = setTimeout(() => {
        const storeRangeAfterTimeout = useAppStore.getState().dateRange;
        if (!storeRangeAfterTimeout.start && !storeRangeAfterTimeout.end) {
          const defaultRange = getDefaultDateRange();
          const defaultRangeKey = `${defaultRange.min_date}-${defaultRange.max_date}`;
          if (lastSetRangeRef.current !== defaultRangeKey) {
            setDateRange(defaultRange.min_date, defaultRange.max_date);
            lastSetRangeRef.current = defaultRangeKey;
            hasInitializedRef.current = true;
          }
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
  }, [dateRangeData, isError, setDateRange]);

  // Está pronto se tem valores no store
  const hasDateRange = !!currentDateRange.start && !!currentDateRange.end;
  
  return {
    isReady: hasDateRange,
  };
}
