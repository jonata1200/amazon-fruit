# 📈 Fase 5: Dashboards - Parte 2 (Estoque, Público-Alvo, Fornecedores e RH)

**Duração Estimada**: 7-10 dias  
**Complexidade**: Alta  
**Dependências**: Fases 1-4 concluídas

---

## 🎯 Objetivos desta Fase

1. Implementar Dashboard de Estoque
2. Implementar Dashboard de Público-Alvo
3. Implementar Dashboard de Fornecedores
4. Implementar Dashboard de Recursos Humanos
5. Garantir consistência entre todos os dashboards
6. Otimizar performance e responsividade

---

## 📋 Checklist de Ações

### 1. Dashboard de Estoque

- [ ] **1.1** Criar hooks para Dashboard de Estoque (se ainda não criado)
  ```typescript
  // Adicionar em src/lib/hooks/useDashboards.ts
  export function useDashboardEstoque(dateRange?: DateRange) {
    const defaultDateRange = useAppStore((state) => state.dateRange);
    const range = dateRange || defaultDateRange;

    return useQuery({
      queryKey: ['dashboard', 'estoque', range.start, range.end],
      queryFn: () => dashboardService.getDashboardEstoque(range),
      enabled: !!range.start && !!range.end,
    });
  }
  ```

- [ ] **1.2** Criar página do Dashboard de Estoque
  ```typescript
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
  ```

- [ ] **1.3** Criar componente de conteúdo do Dashboard de Estoque
  ```typescript
  // src/components/dashboards/estoque/dashboard-estoque-content.tsx
  'use client';

  import { useDashboardEstoque } from '@/lib/hooks/useDashboards';
  import { KPICard } from '@/components/dashboards/kpi-card';
  import { DataTable } from '@/components/ui/data-table';
  import { LoadingScreen } from '@/components/ui/loading-screen';
  import { EmptyState } from '@/components/ui/empty-state';
  import { Package, AlertTriangle, TrendingUp } from 'lucide-react';
  import { Skeleton } from '@/components/ui/skeleton';
  import { formatCurrency, formatNumber } from '@/lib/utils';

  export function DashboardEstoqueContent() {
    const { data, isLoading, error } = useDashboardEstoque();

    if (isLoading) {
      return <DashboardEstoqueSkeleton />;
    }

    if (error) {
      return (
        <EmptyState
          title="Erro ao carregar dashboard"
          description="Não foi possível carregar os dados. Tente novamente mais tarde."
        />
      );
    }

    if (!data) {
      return (
        <EmptyState
          title="Sem dados disponíveis"
          description="Não há dados para o período selecionado."
        />
      );
    }

    const { kpis, top_selling, least_selling, low_stock } = data;

    return (
      <div className="space-y-6">
        {/* KPIs */}
        <div className="grid gap-4 md:grid-cols-3">
          <KPICard
            title="Total de Itens"
            value={kpis.total_items}
            format="number"
            icon={Package}
          />
          <KPICard
            title="Valor Total em Estoque"
            value={kpis.total_value}
            format="currency"
            icon={TrendingUp}
          />
          <KPICard
            title="Itens com Estoque Baixo"
            value={kpis.low_stock_count}
            format="number"
            icon={AlertTriangle}
          />
        </div>

        {/* Tabelas */}
        <div className="grid gap-6 lg:grid-cols-2">
          <DataTable
            title="Produtos Mais Vendidos"
            columns={[
              { key: 'produto', label: 'Produto' },
              { key: 'quantidade', label: 'Quantidade', format: (v) => formatNumber(v) },
              { key: 'valor', label: 'Valor', format: (v) => formatCurrency(v) },
            ]}
            data={Object.entries(top_selling).map(([produto, dados]: [string, any]) => ({
              produto,
              quantidade: dados.quantidade || 0,
              valor: dados.valor || 0,
            }))}
          />

          <DataTable
            title="Produtos Menos Vendidos"
            columns={[
              { key: 'produto', label: 'Produto' },
              { key: 'quantidade', label: 'Quantidade', format: (v) => formatNumber(v) },
              { key: 'valor', label: 'Valor', format: (v) => formatCurrency(v) },
            ]}
            data={Object.entries(least_selling).map(([produto, dados]: [string, any]) => ({
              produto,
              quantidade: dados.quantidade || 0,
              valor: dados.valor || 0,
            }))}
          />
        </div>

        {/* Alertas de Estoque Baixo */}
        {low_stock.length > 0 && (
          <DataTable
            title="⚠️ Alertas de Estoque Baixo"
            columns={[
              { key: 'produto', label: 'Produto' },
              { key: 'estoque_atual', label: 'Estoque Atual', format: (v) => formatNumber(v) },
              { key: 'estoque_minimo', label: 'Estoque Mínimo', format: (v) => formatNumber(v) },
            ]}
            data={low_stock}
          />
        )}
      </div>
    );
  }

  function DashboardEstoqueSkeleton() {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
          <Skeleton className="h-96" />
          <Skeleton className="h-96" />
        </div>
      </div>
    );
  }
  ```

---

### 2. Dashboard de Público-Alvo

- [ ] **2.1** Criar serviço para Dashboard de Público-Alvo
  ```typescript
  // Adicionar em src/lib/api/services.ts
  getDashboardPublicoAlvo: async () => {
    return apiClient.get<any>('/api/dashboard/publico_alvo');
  },
  ```

- [ ] **2.2** Criar hook para Dashboard de Público-Alvo
  ```typescript
  // Adicionar em src/lib/hooks/useDashboards.ts
  export function useDashboardPublicoAlvo() {
    return useQuery({
      queryKey: ['dashboard', 'publico-alvo'],
      queryFn: () => dashboardService.getDashboardPublicoAlvo(),
      staleTime: 5 * 60 * 1000, // 5 minutos
    });
  }
  ```

- [ ] **2.3** Criar página do Dashboard de Público-Alvo
  ```typescript
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
  ```

- [ ] **2.4** Criar componente de conteúdo do Dashboard de Público-Alvo
  ```typescript
  // src/components/dashboards/publico-alvo/dashboard-publico-alvo-content.tsx
  'use client';

  import { useDashboardPublicoAlvo } from '@/lib/hooks/useDashboards';
  import { BarChart } from '@/components/charts/bar-chart';
  import { PieChart } from '@/components/charts/pie-chart';
  import { LoadingScreen } from '@/components/ui/loading-screen';
  import { EmptyState } from '@/components/ui/empty-state';
  import { Skeleton } from '@/components/ui/skeleton';

  export function DashboardPublicoAlvoContent() {
    const { data, isLoading, error } = useDashboardPublicoAlvo();

    if (isLoading) {
      return <DashboardPublicoAlvoSkeleton />;
    }

    if (error) {
      return (
        <EmptyState
          title="Erro ao carregar dashboard"
          description="Não foi possível carregar os dados. Tente novamente mais tarde."
        />
      );
    }

    if (!data) {
      return (
        <EmptyState
          title="Sem dados disponíveis"
          description="Não há dados disponíveis."
        />
      );
    }

    const { by_location, by_gender, by_channel } = data;

    // Preparar dados
    const locationData = Object.entries(by_location).map(([local, count]) => ({
      local,
      count: count as number,
    }));

    const genderData = Object.entries(by_gender).map(([genero, count]) => ({
      name: genero,
      value: count as number,
    }));

    const channelData = Object.entries(by_channel).map(([canal, count]) => ({
      name: canal,
      value: count as number,
    }));

    return (
      <div className="space-y-6">
        {/* Distribuição por Localização */}
        <BarChart
          title="Clientes por Localização (Top 10)"
          data={locationData.slice(0, 10)}
          xAxisKey="local"
          bars={[{ dataKey: 'count', name: 'Clientes', color: '#3b82f6' }]}
          layout="vertical"
          height={400}
        />

        {/* Gráficos de Pizza */}
        <div className="grid gap-6 lg:grid-cols-2">
          <PieChart
            title="Distribuição por Gênero"
            data={genderData}
            dataKey="value"
            nameKey="name"
            colors={['#3b82f6', '#ec4899', '#10b981']}
            height={300}
          />
          <PieChart
            title="Distribuição por Canal de Venda"
            data={channelData}
            dataKey="value"
            nameKey="name"
            colors={['#f59e0b', '#8b5cf6', '#14b8a6', '#f43f5e']}
            height={300}
          />
        </div>
      </div>
    );
  }

  function DashboardPublicoAlvoSkeleton() {
    return (
      <div className="space-y-6">
        <Skeleton className="h-96" />
        <div className="grid gap-6 lg:grid-cols-2">
          <Skeleton className="h-72" />
          <Skeleton className="h-72" />
        </div>
      </div>
    );
  }
  ```

---

### 3. Dashboard de Fornecedores

- [ ] **3.1** Criar serviço e hook para Fornecedores
  ```typescript
  // Em src/lib/api/services.ts
  getDashboardFornecedores: async () => {
    return apiClient.get<any>('/api/dashboard/fornecedores');
  },

  // Em src/lib/hooks/useDashboards.ts
  export function useDashboardFornecedores() {
    return useQuery({
      queryKey: ['dashboard', 'fornecedores'],
      queryFn: () => dashboardService.getDashboardFornecedores(),
      staleTime: 5 * 60 * 1000,
    });
  }
  ```

- [ ] **3.2** Criar página do Dashboard de Fornecedores
  ```typescript
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
  ```

- [ ] **3.3** Criar componente de conteúdo do Dashboard de Fornecedores
  ```typescript
  // src/components/dashboards/fornecedores/dashboard-fornecedores-content.tsx
  'use client';

  import { useDashboardFornecedores } from '@/lib/hooks/useDashboards';
  import { DataTable } from '@/components/ui/data-table';
  import { PieChart } from '@/components/charts/pie-chart';
  import { LoadingScreen } from '@/components/ui/loading-screen';
  import { EmptyState } from '@/components/ui/empty-state';
  import { Skeleton } from '@/components/ui/skeleton';

  export function DashboardFornecedoresContent() {
    const { data, isLoading, error } = useDashboardFornecedores();

    if (isLoading) {
      return <DashboardFornecedoresSkeleton />;
    }

    if (error) {
      return (
        <EmptyState
          title="Erro ao carregar dashboard"
          description="Não foi possível carregar os dados. Tente novamente mais tarde."
        />
      );
    }

    if (!data) {
      return (
        <EmptyState
          title="Sem dados disponíveis"
          description="Não há dados disponíveis."
        />
      );
    }

    const { top_suppliers, bottom_suppliers, by_state } = data;

    // Preparar dados por estado
    const stateData = Object.entries(by_state).map(([estado, count]) => ({
      name: estado,
      value: count as number,
    }));

    return (
      <div className="space-y-6">
        {/* Tabelas de Top e Bottom */}
        <div className="grid gap-6 lg:grid-cols-2">
          <DataTable
            title="🏆 Top 5 Fornecedores"
            columns={[
              { key: 'nome', label: 'Fornecedor' },
              { key: 'pontuacao', label: 'Pontuação' },
              { key: 'estado', label: 'Estado' },
            ]}
            data={top_suppliers}
          />
          <DataTable
            title="⚠️ Fornecedores com Menor Avaliação"
            columns={[
              { key: 'nome', label: 'Fornecedor' },
              { key: 'pontuacao', label: 'Pontuação' },
              { key: 'estado', label: 'Estado' },
            ]}
            data={bottom_suppliers}
          />
        </div>

        {/* Distribuição por Estado */}
        <PieChart
          title="Distribuição de Fornecedores por Estado"
          data={stateData}
          dataKey="value"
          nameKey="name"
          colors={['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#14b8a6']}
          height={400}
        />
      </div>
    );
  }

  function DashboardFornecedoresSkeleton() {
    return (
      <div className="space-y-6">
        <div className="grid gap-6 lg:grid-cols-2">
          <Skeleton className="h-64" />
          <Skeleton className="h-64" />
        </div>
        <Skeleton className="h-96" />
      </div>
    );
  }
  ```

---

### 4. Dashboard de Recursos Humanos

- [ ] **4.1** Criar serviço e hook para RH
  ```typescript
  // Em src/lib/api/services.ts
  getDashboardRecursosHumanos: async () => {
    return apiClient.get<any>('/api/dashboard/recursos_humanos');
  },

  // Em src/lib/hooks/useDashboards.ts
  export function useDashboardRecursosHumanos() {
    return useQuery({
      queryKey: ['dashboard', 'recursos-humanos'],
      queryFn: () => dashboardService.getDashboardRecursosHumanos(),
      staleTime: 5 * 60 * 1000,
    });
  }
  ```

- [ ] **4.2** Criar página do Dashboard de RH
  ```typescript
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
  ```

- [ ] **4.3** Criar componente de conteúdo do Dashboard de RH
  ```typescript
  // src/components/dashboards/recursos-humanos/dashboard-rh-content.tsx
  'use client';

  import { useDashboardRecursosHumanos } from '@/lib/hooks/useDashboards';
  import { BarChart } from '@/components/charts/bar-chart';
  import { PieChart } from '@/components/charts/pie-chart';
  import { LineChart } from '@/components/charts/line-chart';
  import { LoadingScreen } from '@/components/ui/loading-screen';
  import { EmptyState } from '@/components/ui/empty-state';
  import { Skeleton } from '@/components/ui/skeleton';

  export function DashboardRHContent() {
    const { data, isLoading, error } = useDashboardRecursosHumanos();

    if (isLoading) {
      return <DashboardRHSkeleton />;
    }

    if (error) {
      return (
        <EmptyState
          title="Erro ao carregar dashboard"
          description="Não foi possível carregar os dados. Tente novamente mais tarde."
        />
      );
    }

    if (!data) {
      return (
        <EmptyState
          title="Sem dados disponíveis"
          description="Não há dados disponíveis."
        />
      );
    }

    const { headcount_by_department, cost_by_department, by_role, hiring_over_time } = data;

    // Preparar dados
    const headcountData = Object.entries(headcount_by_department).map(([dept, count]) => ({
      departamento: dept,
      funcionarios: count as number,
    }));

    const costData = Object.entries(cost_by_department).map(([dept, cost]) => ({
      departamento: dept,
      custo: cost as number,
    }));

    const roleData = Object.entries(by_role).map(([role, count]) => ({
      name: role,
      value: count as number,
    }));

    const hiringData = Object.entries(hiring_over_time).map(([periodo, count]) => ({
      periodo,
      contratacoes: count as number,
    }));

    return (
      <div className="space-y-6">
        {/* Headcount e Custos por Departamento */}
        <div className="grid gap-6 lg:grid-cols-2">
          <BarChart
            title="Headcount por Departamento"
            data={headcountData}
            xAxisKey="departamento"
            bars={[{ dataKey: 'funcionarios', name: 'Funcionários', color: '#3b82f6' }]}
            height={300}
          />
          <BarChart
            title="Custo por Departamento"
            data={costData}
            xAxisKey="departamento"
            bars={[{ dataKey: 'custo', name: 'Custo', color: '#10b981' }]}
            height={300}
          />
        </div>

        {/* Distribuição por Cargo */}
        <PieChart
          title="Distribuição de Funcionários por Cargo"
          data={roleData}
          dataKey="value"
          nameKey="name"
          colors={['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']}
          height={350}
        />

        {/* Histórico de Contratações */}
        <LineChart
          title="Histórico de Contratações"
          data={hiringData}
          xAxisKey="periodo"
          lines={[{ dataKey: 'contratacoes', name: 'Contratações', color: '#8b5cf6' }]}
          height={300}
        />
      </div>
    );
  }

  function DashboardRHSkeleton() {
    return (
      <div className="space-y-6">
        <div className="grid gap-6 lg:grid-cols-2">
          <Skeleton className="h-72" />
          <Skeleton className="h-72" />
        </div>
        <Skeleton className="h-80" />
        <Skeleton className="h-72" />
      </div>
    );
  }
  ```

---

### 5. Página Inicial (Home)

- [ ] **5.1** Criar página inicial que redireciona para Dashboard Geral
  ```typescript
  // src/app/page.tsx
  import { redirect } from 'next/navigation';

  export default function HomePage() {
    redirect('/geral');
  }
  ```

---

### 6. Rotas e Navegação

- [ ] **6.1** Criar layout de grupo para dashboards
  ```typescript
  // src/app/(dashboards)/layout.tsx
  import { ErrorBoundary } from '@/components/error-boundary';

  export default function DashboardsLayout({
    children,
  }: {
    children: React.ReactNode;
  }) {
    return <ErrorBoundary>{children}</ErrorBoundary>;
  }
  ```

---

### 7. Testes de Todos os Dashboards

- [ ] **7.1** Testes do Dashboard de Estoque
- [ ] **7.2** Testes do Dashboard de Público-Alvo
- [ ] **7.3** Testes do Dashboard de Fornecedores
- [ ] **7.4** Testes do Dashboard de RH
- [ ] **7.5** Testes de navegação entre dashboards
- [ ] **7.6** Testes de responsividade

---

### 8. Otimização de Performance

- [ ] **8.1** Implementar code splitting por dashboard
- [ ] **8.2** Otimizar re-renders com React.memo
- [ ] **8.3** Implementar virtualização para listas longas (se necessário)
- [ ] **8.4** Otimizar tamanho dos gráficos

---

### 9. Acessibilidade

- [ ] **9.1** Adicionar labels ARIA em gráficos
- [ ] **9.2** Garantir navegação por teclado
- [ ] **9.3** Testar com leitores de tela
- [ ] **9.4** Verificar contraste de cores

---

### 10. Documentação

- [ ] **10.1** Documentar estrutura de cada dashboard
- [ ] **10.2** Criar guia de como adicionar novos dashboards
- [ ] **10.3** Documentar padrões de componentes usados
- [ ] **10.4** Atualizar README com screenshots

---

### 11. Verificação Final

- [ ] **11.1** Testar todos os dashboards
- [ ] **11.2** Verificar integração com API
- [ ] **11.3** Testar filtros de período (quando aplicável)
- [ ] **11.4** Verificar responsividade em todos os dashboards
- [ ] **11.5** Executar testes
  ```bash
  npm test
  ```

---

## ✅ Critérios de Conclusão da Fase 5

A Fase 5 está completa quando:

- [x] Todos os 6 dashboards implementados e funcionais
- [x] Navegação entre dashboards funcionando
- [x] Dados da API integrados em todos os dashboards
- [x] Todos os dashboards responsivos
- [x] Performance otimizada
- [x] Acessibilidade validada
- [x] Testes passando
- [x] Documentação completa

---

## 📝 Notas e Observações

### Decisões Técnicas

1. **Consistência**: Todos os dashboards seguem o mesmo padrão de estrutura
2. **Skeleton Screens**: Implementados em todos os dashboards para melhor UX
3. **Error Handling**: Error boundaries aplicados em todos os dashboards

### Próximos Passos

- Prosseguir para [Fase 6: Funcionalidades Avançadas](./MIGRATION_PHASE_6.md)

---

**Status**: ⏳ Pendente  
**Responsável**: [Nome]  
**Data de Início**: [Data]  
**Data de Conclusão**: [Data]
