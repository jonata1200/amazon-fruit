// src/lib/hooks/useDashboards.ts
import { useQuery } from '@tanstack/react-query';
import { dashboardService } from '@/lib/api/services';
import { useAppStore } from '@/store';
import type { DateRange } from '@/types/api';

export function useDashboardGeral(dateRange?: DateRange) {
  const defaultDateRange = useAppStore((state) => state.dateRange);
  const range = dateRange || defaultDateRange;

  return useQuery({
    queryKey: ['dashboard', 'geral', range.start, range.end],
    queryFn: () => dashboardService.getDashboardGeral(range),
    enabled: !!range.start && !!range.end,
  });
}

export function useDashboardFinancas(dateRange?: DateRange) {
  const defaultDateRange = useAppStore((state) => state.dateRange);
  const range = dateRange || defaultDateRange;

  return useQuery({
    queryKey: ['dashboard', 'financas', range.start, range.end],
    queryFn: () => dashboardService.getDashboardFinancas(range),
    enabled: !!range.start && !!range.end,
  });
}

export function useDashboardEstoque(dateRange?: DateRange) {
  const defaultDateRange = useAppStore((state) => state.dateRange);
  const range = dateRange || defaultDateRange;

  return useQuery({
    queryKey: ['dashboard', 'estoque', range.start, range.end],
    queryFn: () => dashboardService.getDashboardEstoque(range),
    enabled: !!range.start && !!range.end,
  });
}

export function useDashboardPublicoAlvo() {
  return useQuery({
    queryKey: ['dashboard', 'publico-alvo'],
    queryFn: () => dashboardService.getDashboardPublicoAlvo(),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}

export function useDashboardFornecedores() {
  return useQuery({
    queryKey: ['dashboard', 'fornecedores'],
    queryFn: () => dashboardService.getDashboardFornecedores(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useDashboardRecursosHumanos() {
  return useQuery({
    queryKey: ['dashboard', 'recursos-humanos'],
    queryFn: () => dashboardService.getDashboardRecursosHumanos(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useDateRange() {
  return useQuery({
    queryKey: ['dateRange'],
    queryFn: () => dashboardService.getDateRange(),
    staleTime: Infinity, // Data range não muda frequentemente
    retry: 1, // Tentar apenas 1 vez em caso de erro (evita muitas tentativas)
    retryDelay: 1000, // Esperar 1 segundo antes de retentar
    // Não bloquear renderização em caso de erro de rede
    throwOnError: false,
  });
}
