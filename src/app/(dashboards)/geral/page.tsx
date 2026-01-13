// src/app/(dashboards)/geral/page.tsx
'use client';

import { MainLayout } from '@/components/layouts/main-layout';
import { PeriodSelector } from '@/components/dashboards/period-selector';
import { DashboardGeralContent } from '@/components/dashboards/geral/dashboard-geral-content';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';

export default function DashboardGeralPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <MainLayout title="Visão Geral do Negócio">
      <div className="space-y-6">
        <PeriodSelector />
        <DashboardGeralContent />
      </div>
    </MainLayout>
  );
}
