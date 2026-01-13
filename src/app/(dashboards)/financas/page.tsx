// src/app/(dashboards)/financas/page.tsx
'use client';

import { MainLayout } from '@/components/layouts/main-layout';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { DashboardFinancasContent } from '@/components/dashboards/financas/dashboard-financas-content';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';

export default function DashboardFinancasPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <MainLayout title="Dashboard de Finanças">
      <div className="space-y-6">
        <PeriodSelector />
        <DashboardFinancasContent />
      </div>
    </MainLayout>
  );
}
