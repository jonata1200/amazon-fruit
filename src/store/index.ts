// src/store/index.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface AppState {
  // Theme
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;

  // Date Range
  dateRange: {
    start: string;
    end: string;
  };
  setDateRange: (start: string, end: string) => void;

  // Current Dashboard
  currentDashboard: string;
  setCurrentDashboard: (dashboard: string) => void;

  // Sidebar
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;

  // Alerts
  alertsOpen: boolean;
  setAlertsOpen: (open: boolean) => void;
  toggleAlerts: () => void;

  // Search
  searchOpen: boolean;
  setSearchOpen: (open: boolean) => void;
  toggleSearch: () => void;

  // Comparison Mode
  comparisonMode: boolean;
  setComparisonMode: (enabled: boolean) => void;
  toggleComparisonMode: () => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        // Theme
        theme: 'light',
        setTheme: (theme) => set({ theme }),
        toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),

        // Date Range
        dateRange: {
          start: '',
          end: '',
        },
        setDateRange: (start, end) => set({ dateRange: { start, end } }),

        // Current Dashboard
        currentDashboard: 'geral',
        setCurrentDashboard: (dashboard) => set({ currentDashboard: dashboard }),

        // Sidebar
        sidebarOpen: true,
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),

        // Alerts
        alertsOpen: false,
        setAlertsOpen: (open) => set({ alertsOpen: open }),
        toggleAlerts: () => set((state) => ({ alertsOpen: !state.alertsOpen })),

        // Search
        searchOpen: false,
        setSearchOpen: (open) => set({ searchOpen: open }),
        toggleSearch: () => set((state) => ({ searchOpen: !state.searchOpen })),

        // Comparison Mode
        comparisonMode: false,
        setComparisonMode: (enabled) => set({ comparisonMode: enabled }),
        toggleComparisonMode: () => set((state) => ({ comparisonMode: !state.comparisonMode })),
      }),
      {
        name: 'amazon-fruit-storage',
        partialize: (state) => ({
          theme: state.theme,
          sidebarOpen: state.sidebarOpen,
        }),
      }
    )
  )
);
