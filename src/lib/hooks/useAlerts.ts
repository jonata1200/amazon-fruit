// src/lib/hooks/useAlerts.ts
import { useQuery } from '@tanstack/react-query';
import { alertService } from '@/lib/api/services';

export function useAlerts() {
  return useQuery({
    queryKey: ['alerts'],
    queryFn: () => alertService.getAlerts(),
    refetchInterval: 60000, // Refetch a cada 1 minuto
  });
}
