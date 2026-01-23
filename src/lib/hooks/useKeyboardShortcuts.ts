// src/lib/hooks/useKeyboardShortcuts.ts
import { useEffect } from 'react';
import { useAppStore } from '@/store';

export function useKeyboardShortcuts() {
  const toggleTheme = useAppStore((state) => state.toggleTheme);
  const toggleSearch = useAppStore((state) => state.toggleSearch);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Verificar se é mobile (largura < 640px)
      const isMobile = window.innerWidth < 640;

      // Em mobile, apenas ESC funciona (para fechar painéis)
      if (isMobile) {
        if (e.key === 'Escape') {
          const searchOpen = useAppStore.getState().searchOpen;
          const alertsOpen = useAppStore.getState().alertsOpen;

          if (searchOpen) {
            useAppStore.getState().setSearchOpen(false);
          }
          if (alertsOpen) {
            useAppStore.getState().setAlertsOpen(false);
          }
        }
        return; // Não processar outros atalhos em mobile
      }

      // Atalhos apenas em desktop
      // Ctrl/Cmd + K: Busca
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        toggleSearch();
      }

      // Ctrl/Cmd + T: Tema
      if ((e.ctrlKey || e.metaKey) && e.key === 't') {
        e.preventDefault();
        toggleTheme();
      }

      // ESC: Fechar painéis
      if (e.key === 'Escape') {
        const searchOpen = useAppStore.getState().searchOpen;
        const alertsOpen = useAppStore.getState().alertsOpen;

        if (searchOpen) {
          useAppStore.getState().setSearchOpen(false);
        }
        if (alertsOpen) {
          useAppStore.getState().setAlertsOpen(false);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleTheme, toggleSearch]);
}
