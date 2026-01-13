// src/app/(dashboards)/publico-alvo/page.tsx
'use client';

import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardPublicoAlvoContent } from '@/components/dashboards/publico-alvo/dashboard-publico-alvo-content';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';

export default function DashboardPublicoAlvoPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <MainLayout title="Dashboard de Público-Alvo">
      <div className="space-y-6">
        <DashboardPublicoAlvoContent />
      </div>
    </MainLayout>
  );
}
