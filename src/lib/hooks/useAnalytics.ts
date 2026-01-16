// src/lib/hooks/useAnalytics.ts
import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { analytics } from '@/lib/analytics/events';

/**
 * Hook para rastrear visualizações de página/dashboard
 */
export function usePageView(dashboard?: string) {
  const pathname = usePathname();

  useEffect(() => {
    if (dashboard) {
      analytics.dashboardViewed(dashboard);
    } else if (pathname) {
      // Extrair nome do dashboard do pathname
      const dashboardName = pathname.split('/').filter(Boolean)[0] || 'home';
      analytics.dashboardViewed(dashboardName);
    }
  }, [pathname, dashboard]);
}

/**
 * Hook para rastrear tempo de sessão
 */
export function useSessionTracking() {
  useEffect(() => {
    const startTime = Date.now();

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        const sessionDuration = Date.now() - startTime;
        analytics.featureUsed('session_ended', {
          duration: sessionDuration,
        });
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      const sessionDuration = Date.now() - startTime;
      analytics.featureUsed('session_ended', {
        duration: sessionDuration,
      });
    };
  }, []);
}
