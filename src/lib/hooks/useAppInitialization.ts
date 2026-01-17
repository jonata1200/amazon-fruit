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
  const hasInitializedRef = useRef(false);
  const lastSetRangeRef = useRef<string>('');

  useEffect(() => {
    // Obter estado atual do store dentro do effect para evitar dependências
    const storeRange = useAppStore.getState().dateRange;
    const hasCurrentRange = !!storeRange.start && !!storeRange.end;

    // Se já foi inicializado e os valores já estão corretos, não fazer nada
    if (hasInitializedRef.current && hasCurrentRange) {
      return;
    }

    // Se não tiver dateRange inicial, definir valores padrão imediatamente
    // Isso evita bloquear a renderização esperando pela API
    if (!hasCurrentRange && !hasInitializedRef.current) {
      const defaultRange = getDefaultDateRange();
      const defaultRangeKey = `${defaultRange.min_date}-${defaultRange.max_date}`;
      setDateRange(defaultRange.min_date, defaultRange.max_date);
      lastSetRangeRef.current = defaultRangeKey;
      hasInitializedRef.current = true;
    }

    // Se conseguir dados da API e forem diferentes dos padrão, atualizar
    if (dateRangeData) {
      const apiRangeKey = `${dateRangeData.min_date}-${dateRangeData.max_date}`;
      if (lastSetRangeRef.current !== apiRangeKey) {
        // Só atualizar se o valor for diferente
        if (storeRange.start !== dateRangeData.min_date || storeRange.end !== dateRangeData.max_date) {
          setDateRange(dateRangeData.min_date, dateRangeData.max_date);
        }
        lastSetRangeRef.current = apiRangeKey;
      }
    }
  }, [dateRangeData, isError, setDateRange]);

  // Está pronto se tem valores no store (agora sempre inicializa com valores padrão)
  const hasDateRange = !!currentDateRange.start && !!currentDateRange.end;
  
  return {
    isReady: hasDateRange,
  };
}
