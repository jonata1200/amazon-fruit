// src/lib/hooks/useFavorites.ts
import { useState, useEffect } from 'react';
import { analytics } from '@/lib/analytics/events';

const FAVORITES_STORAGE_KEY = 'amazon-fruit-favorites';

export type DashboardId = 'geral' | 'financas' | 'estoque' | 'publico-alvo' | 'fornecedores' | 'recursos-humanos';

interface UseFavoritesReturn {
  favorites: DashboardId[];
  addFavorite: (dashboard: DashboardId) => void;
  removeFavorite: (dashboard: DashboardId) => void;
  toggleFavorite: (dashboard: DashboardId) => void;
  isFavorite: (dashboard: DashboardId) => boolean;
}

export function useFavorites(): UseFavoritesReturn {
  const [favorites, setFavorites] = useState<DashboardId[]>([]);

  // Carregar favoritos do localStorage na montagem
  useEffect(() => {
    try {
      const stored = localStorage.getItem(FAVORITES_STORAGE_KEY);
      if (stored) {
        setFavorites(JSON.parse(stored));
      }
    } catch (error) {
      console.error('Erro ao carregar favoritos:', error);
    }
  }, []);

  // Salvar favoritos no localStorage sempre que mudar
  useEffect(() => {
    try {
      localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify(favorites));
    } catch (error) {
      console.error('Erro ao salvar favoritos:', error);
    }
  }, [favorites]);

  const addFavorite = (dashboard: DashboardId) => {
    setFavorites((prev) => {
      if (prev.includes(dashboard)) return prev;
      const newFavorites = [...prev, dashboard];
      analytics.featureUsed('favorite_added', { dashboard });
      return newFavorites;
    });
  };

  const removeFavorite = (dashboard: DashboardId) => {
    setFavorites((prev) => {
      const newFavorites = prev.filter((fav) => fav !== dashboard);
      analytics.featureUsed('favorite_removed', { dashboard });
      return newFavorites;
    });
  };

  const toggleFavorite = (dashboard: DashboardId) => {
    setFavorites((prev) => {
      if (prev.includes(dashboard)) {
        analytics.featureUsed('favorite_removed', { dashboard });
        return prev.filter((fav) => fav !== dashboard);
      } else {
        analytics.featureUsed('favorite_added', { dashboard });
        return [...prev, dashboard];
      }
    });
  };

  const isFavorite = (dashboard: DashboardId) => {
    return favorites.includes(dashboard);
  };

  return {
    favorites,
    addFavorite,
    removeFavorite,
    toggleFavorite,
    isFavorite,
  };
}
