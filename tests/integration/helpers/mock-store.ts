// tests/integration/helpers/mock-store.ts
import { useAppStore } from '@/store';

export const defaultStoreState = {
  theme: 'light' as const,
  sidebarOpen: true,
  alertsOpen: false,
  searchOpen: false,
  comparisonMode: false,
  dateRange: {
    start: '',
    end: '',
  },
  currentDashboard: 'geral',
};

export function resetStore() {
  const store = useAppStore.getState();
  
  // Reset para estado padrão
  store.setTheme('light');
  store.setSidebarOpen(true);
  store.setAlertsOpen(false);
  store.setSearchOpen(false);
  store.setComparisonMode(false);
  store.setDateRange('', '');
  store.setCurrentDashboard('geral');
}

export function setStoreState(updates: Partial<typeof defaultStoreState>) {
  const store = useAppStore.getState();
  
  if (updates.theme !== undefined) {
    store.setTheme(updates.theme);
  }
  if (updates.sidebarOpen !== undefined) {
    store.setSidebarOpen(updates.sidebarOpen);
  }
  if (updates.alertsOpen !== undefined) {
    store.setAlertsOpen(updates.alertsOpen);
  }
  if (updates.searchOpen !== undefined) {
    store.setSearchOpen(updates.searchOpen);
  }
  if (updates.comparisonMode !== undefined) {
    store.setComparisonMode(updates.comparisonMode);
  }
  if (updates.dateRange !== undefined) {
    store.setDateRange(updates.dateRange.start, updates.dateRange.end);
  }
  if (updates.currentDashboard !== undefined) {
    store.setCurrentDashboard(updates.currentDashboard);
  }
}
