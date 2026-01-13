// src/app/(dashboards)/recursos-humanos/page.tsx
'use client';

import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardRHContent } from '@/components/dashboards/recursos-humanos/dashboard-rh-content';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';

export default function DashboardRecursosHumanosPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <MainLayout title="Dashboard de Recursos Humanos">
      <div className="space-y-6">
        <DashboardRHContent />
      </div>
    </MainLayout>
  );
}
