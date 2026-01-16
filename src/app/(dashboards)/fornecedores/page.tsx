// src/app/(dashboards)/fornecedores/page.tsx
'use client';

import { lazy, Suspense } from 'react';
import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';
import { useAppInitialization } from '@/lib/hooks/useAppInitialization';
import { LoadingScreen } from '@/components/ui/loading-screen';
import { ErrorBoundary } from '@/components/error-boundary';

const DashboardFornecedoresContent = lazy(() =>
  import('@/components/dashboards/fornecedores/dashboard-fornecedores-content').then((module) => ({
    default: module.DashboardFornecedoresContent,
  }))
);

export default function DashboardFornecedoresPage() {
  const { isReady } = useAppInitialization();

  if (!isReady) {
    return <LoadingScreen message="Inicializando aplicação..." />;
  }

  return (
    <ErrorBoundary title="Erro no Dashboard de Fornecedores" message="Ocorreu um erro ao carregar o dashboard de fornecedores.">
      <MainLayout title="Dashboard de Fornecedores">
        <div className="space-y-6">
          <Suspense fallback={<DashboardSkeleton />}>
            <DashboardFornecedoresContent />
          </Suspense>
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}
