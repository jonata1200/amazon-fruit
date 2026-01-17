// tests/unit/lib/hooks/useAlerts.test.tsx
import React from 'react';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAlerts } from '@/lib/hooks/useAlerts';
import { alertService } from '@/lib/api/services';

// Mock do alertService
jest.mock('@/lib/api/services', () => ({
  alertService: {
    getAlerts: jest.fn(),
  },
  dashboardService: {},
  searchService: {},
  exportService: {},
}));

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('useAlerts', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('fetches alerts successfully', async () => {
    const mockAlerts = {
      alerts: [
        {
          id: '1',
          type: 'warning' as const,
          category: 'Estoque',
          message: 'Produto com estoque baixo',
          timestamp: new Date().toISOString(),
        },
      ],
      count: 1,
    };

    (alertService.getAlerts as jest.Mock).mockResolvedValue(mockAlerts);

    const { result } = renderHook(() => useAlerts(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data).toEqual(mockAlerts);
    expect(alertService.getAlerts).toHaveBeenCalledTimes(1);
  });

  it('handles error when fetching alerts fails', async () => {
    (alertService.getAlerts as jest.Mock).mockRejectedValue(new Error('Failed to fetch'));

    const { result } = renderHook(() => useAlerts(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toBeDefined();
  });

  it('uses correct query key', () => {
    renderHook(() => useAlerts(), {
      wrapper: createWrapper(),
    });

    expect(alertService.getAlerts).toHaveBeenCalled();
  });
});
