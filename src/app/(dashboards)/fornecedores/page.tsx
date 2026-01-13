// src/app/(dashboards)/fornecedores/page.tsx
'use client';

import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardFornecedoresContent } from '@/components/dashboards/fornecedores/dashboard-fornecedores-content';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';

export default function DashboardFornecedoresPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <MainLayout title="Dashboard de Fornecedores">
      <div className="space-y-6">
        <DashboardFornecedoresContent />
      </div>
    </MainLayout>
  );
}
