// src/app/(dashboards)/estoque/page.tsx
'use client';

import { MainLayout } from '@/components/layouts/main-layout';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { DashboardEstoqueContent } from '@/components/dashboards/estoque/dashboard-estoque-content';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';

export default function DashboardEstoquePage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <MainLayout title="Dashboard de Estoque">
      <div className="space-y-6">
        <PeriodSelector />
        <DashboardEstoqueContent />
      </div>
    </MainLayout>
  );
}
