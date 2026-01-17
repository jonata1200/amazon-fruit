// tests/integration/helpers/render-with-providers.tsx
import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAppStore } from '@/store';

// Criar QueryClient para testes de integração
const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
  });

interface RenderWithProvidersOptions extends Omit<RenderOptions, 'wrapper'> {
  initialStoreState?: Partial<ReturnType<typeof useAppStore.getState>>;
  queryClient?: QueryClient;
}

export function renderWithProviders(
  ui: ReactElement,
  options: RenderWithProvidersOptions = {}
) {
  const { initialStoreState, queryClient, ...renderOptions } = options;
  const testQueryClient = queryClient || createTestQueryClient();

  // Reset store state se necessário
  if (initialStoreState) {
    const store = useAppStore.getState();
    if (initialStoreState.theme !== undefined) {
      store.setTheme(initialStoreState.theme);
    }
    if (initialStoreState.sidebarOpen !== undefined) {
      store.setSidebarOpen(initialStoreState.sidebarOpen);
    }
    if (initialStoreState.alertsOpen !== undefined) {
      store.setAlertsOpen(initialStoreState.alertsOpen);
    }
    if (initialStoreState.searchOpen !== undefined) {
      store.setSearchOpen(initialStoreState.searchOpen);
    }
    if (initialStoreState.comparisonMode !== undefined) {
      store.setComparisonMode(initialStoreState.comparisonMode);
    }
    if (initialStoreState.dateRange !== undefined) {
      store.setDateRange(initialStoreState.dateRange.start, initialStoreState.dateRange.end);
    }
    if (initialStoreState.currentDashboard !== undefined) {
      store.setCurrentDashboard(initialStoreState.currentDashboard);
    }
  }

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={testQueryClient}>
        {children}
      </QueryClientProvider>
    );
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}

// Re-exportar utilities do testing-library
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';
