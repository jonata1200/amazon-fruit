// tests/unit/store/index.test.ts
import { renderHook, act } from '@testing-library/react';
import { useAppStore } from '@/store';

describe('useAppStore', () => {
  beforeEach(() => {
    // Reset store state before each test
    const store = useAppStore.getState();
    store.setTheme('light');
    store.setSidebarOpen(true);
    store.setAlertsOpen(false);
    store.setSearchOpen(false);
    store.setDateRange('', '');
    store.setCurrentDashboard('geral');
    store.setComparisonMode(false);
  });

  describe('Theme', () => {
    it('has initial theme as light', () => {
      const { result } = renderHook(() => useAppStore((state) => state.theme));
      expect(result.current).toBe('light');
    });

    it('sets theme correctly', () => {
      const { result } = renderHook(() => useAppStore((state) => state.setTheme));
      
      act(() => {
        result.current('dark');
      });

      const theme = useAppStore.getState().theme;
      expect(theme).toBe('dark');
    });

    it('toggles theme', () => {
      const { result } = renderHook(() => useAppStore((state) => state.toggleTheme));
      
      act(() => {
        result.current();
      });

      expect(useAppStore.getState().theme).toBe('dark');

      act(() => {
        result.current();
      });

      expect(useAppStore.getState().theme).toBe('light');
    });
  });

  describe('Date Range', () => {
    it('has initial empty date range', () => {
      const { result } = renderHook(() => useAppStore((state) => state.dateRange));
      expect(result.current.start).toBe('');
      expect(result.current.end).toBe('');
    });

    it('sets date range correctly', () => {
      const { result } = renderHook(() => useAppStore((state) => state.setDateRange));
      
      act(() => {
        result.current('2024-01-01', '2024-12-31');
      });

      const dateRange = useAppStore.getState().dateRange;
      expect(dateRange.start).toBe('2024-01-01');
      expect(dateRange.end).toBe('2024-12-31');
    });
  });

  describe('Current Dashboard', () => {
    it('has initial dashboard as geral', () => {
      const { result } = renderHook(() => useAppStore((state) => state.currentDashboard));
      expect(result.current).toBe('geral');
    });

    it('sets current dashboard correctly', () => {
      const { result } = renderHook(() => useAppStore((state) => state.setCurrentDashboard));
      
      act(() => {
        result.current('financas');
      });

      expect(useAppStore.getState().currentDashboard).toBe('financas');
    });
  });

  describe('Sidebar', () => {
    it('has initial sidebar open', () => {
      const { result } = renderHook(() => useAppStore((state) => state.sidebarOpen));
      expect(result.current).toBe(true);
    });

    it('sets sidebar open state', () => {
      const { result } = renderHook(() => useAppStore((state) => state.setSidebarOpen));
      
      act(() => {
        result.current(false);
      });

      expect(useAppStore.getState().sidebarOpen).toBe(false);
    });

    it('toggles sidebar', () => {
      const { result } = renderHook(() => useAppStore((state) => state.toggleSidebar));
      
      act(() => {
        result.current();
      });

      expect(useAppStore.getState().sidebarOpen).toBe(false);

      act(() => {
        result.current();
      });

      expect(useAppStore.getState().sidebarOpen).toBe(true);
    });
  });

  describe('Alerts', () => {
    it('has initial alerts closed', () => {
      const { result } = renderHook(() => useAppStore((state) => state.alertsOpen));
      expect(result.current).toBe(false);
    });

    it('sets alerts open state', () => {
      const { result } = renderHook(() => useAppStore((state) => state.setAlertsOpen));
      
      act(() => {
        result.current(true);
      });

      expect(useAppStore.getState().alertsOpen).toBe(true);
    });

    it('toggles alerts', () => {
      const { result } = renderHook(() => useAppStore((state) => state.toggleAlerts));
      
      act(() => {
        result.current();
      });

      expect(useAppStore.getState().alertsOpen).toBe(true);

      act(() => {
        result.current();
      });

      expect(useAppStore.getState().alertsOpen).toBe(false);
    });
  });

  describe('Search', () => {
    it('has initial search closed', () => {
      const { result } = renderHook(() => useAppStore((state) => state.searchOpen));
      expect(result.current).toBe(false);
    });

    it('sets search open state', () => {
      const { result } = renderHook(() => useAppStore((state) => state.setSearchOpen));
      
      act(() => {
        result.current(true);
      });

      expect(useAppStore.getState().searchOpen).toBe(true);
    });

    it('toggles search', () => {
      const { result } = renderHook(() => useAppStore((state) => state.toggleSearch));
      
      act(() => {
        result.current();
      });

      expect(useAppStore.getState().searchOpen).toBe(true);

      act(() => {
        result.current();
      });

      expect(useAppStore.getState().searchOpen).toBe(false);
    });
  });

  describe('Comparison Mode', () => {
    it('has initial comparison mode disabled', () => {
      const { result } = renderHook(() => useAppStore((state) => state.comparisonMode));
      expect(result.current).toBe(false);
    });

    it('sets comparison mode', () => {
      const { result } = renderHook(() => useAppStore((state) => state.setComparisonMode));
      
      act(() => {
        result.current(true);
      });

      expect(useAppStore.getState().comparisonMode).toBe(true);
    });

    it('toggles comparison mode', () => {
      const { result } = renderHook(() => useAppStore((state) => state.toggleComparisonMode));
      
      act(() => {
        result.current();
      });

      expect(useAppStore.getState().comparisonMode).toBe(true);

      act(() => {
        result.current();
      });

      expect(useAppStore.getState().comparisonMode).toBe(false);
    });
  });
});
