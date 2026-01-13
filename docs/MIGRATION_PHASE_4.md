# 📊 Fase 4: Dashboards - Parte 1 (Geral e Finanças)

**Duração Estimada**: 7-10 dias  
**Complexidade**: Alta  
**Dependências**: Fases 1, 2 e 3 concluídas

---

## 🎯 Objetivos desta Fase

1. Implementar Dashboard Geral completo
2. Implementar Dashboard de Finanças completo
3. Criar componentes de gráficos reutilizáveis
4. Implementar sistema de filtros de período
5. Integrar dados da API com visualizações
6. Garantir responsividade e performance

---

## 📋 Checklist de Ações

### 1. Componentes de Gráficos Base

- [ ] **1.1** Escolher biblioteca de gráficos
  - Avaliar: Recharts vs Plotly.js vs Victory
  - Decisão recomendada: **Recharts** (melhor integração com React)
  
- [ ] **1.2** Instalar Recharts (se escolhido)
  ```bash
  npm install recharts
  ```

- [ ] **1.3** Criar wrapper de gráfico de linha
  ```typescript
  // src/components/charts/line-chart.tsx
  'use client';

  import {
    LineChart as RechartsLineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
  } from 'recharts';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

  interface LineChartProps {
    title?: string;
    data: any[];
    lines: {
      dataKey: string;
      name: string;
      color: string;
    }[];
    xAxisKey: string;
    height?: number;
  }

  export function LineChart({ title, data, lines, xAxisKey, height = 300 }: LineChartProps) {
    return (
      <Card>
        {title && (
          <CardHeader>
            <CardTitle>{title}</CardTitle>
          </CardHeader>
        )}
        <CardContent>
          <ResponsiveContainer width="100%" height={height}>
            <RechartsLineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xAxisKey} />
              <YAxis />
              <Tooltip />
              <Legend />
              {lines.map((line) => (
                <Line
                  key={line.dataKey}
                  type="monotone"
                  dataKey={line.dataKey}
                  name={line.name}
                  stroke={line.color}
                  strokeWidth={2}
                />
              ))}
            </RechartsLineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    );
  }
  ```

- [ ] **1.4** Criar wrapper de gráfico de barras
  ```typescript
  // src/components/charts/bar-chart.tsx
  'use client';

  import {
    BarChart as RechartsBarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
  } from 'recharts';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

  interface BarChartProps {
    title?: string;
    data: any[];
    bars: {
      dataKey: string;
      name: string;
      color: string;
    }[];
    xAxisKey: string;
    height?: number;
    layout?: 'horizontal' | 'vertical';
  }

  export function BarChart({
    title,
    data,
    bars,
    xAxisKey,
    height = 300,
    layout = 'horizontal',
  }: BarChartProps) {
    return (
      <Card>
        {title && (
          <CardHeader>
            <CardTitle>{title}</CardTitle>
          </CardHeader>
        )}
        <CardContent>
          <ResponsiveContainer width="100%" height={height}>
            <RechartsBarChart data={data} layout={layout}>
              <CartesianGrid strokeDasharray="3 3" />
              {layout === 'horizontal' ? (
                <>
                  <XAxis dataKey={xAxisKey} />
                  <YAxis />
                </>
              ) : (
                <>
                  <XAxis type="number" />
                  <YAxis dataKey={xAxisKey} type="category" />
                </>
              )}
              <Tooltip />
              <Legend />
              {bars.map((bar) => (
                <Bar key={bar.dataKey} dataKey={bar.dataKey} name={bar.name} fill={bar.color} />
              ))}
            </RechartsBarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    );
  }
  ```

- [ ] **1.5** Criar wrapper de gráfico de pizza
  ```typescript
  // src/components/charts/pie-chart.tsx
  'use client';

  import {
    PieChart as RechartsPieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer,
  } from 'recharts';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

  interface PieChartProps {
    title?: string;
    data: any[];
    dataKey: string;
    nameKey: string;
    colors: string[];
    height?: number;
  }

  export function PieChart({ title, data, dataKey, nameKey, colors, height = 300 }: PieChartProps) {
    return (
      <Card>
        {title && (
          <CardHeader>
            <CardTitle>{title}</CardTitle>
          </CardHeader>
        )}
        <CardContent>
          <ResponsiveContainer width="100%" height={height}>
            <RechartsPieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => entry[nameKey]}
                outerRadius={80}
                fill="#8884d8"
                dataKey={dataKey}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </RechartsPieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    );
  }
  ```

---

### 2. Dashboard Geral - Estrutura

- [ ] **2.1** Criar página do Dashboard Geral
  ```typescript
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
  ```

- [ ] **2.2** Criar componente de conteúdo do Dashboard Geral
  ```typescript
  // src/components/dashboards/geral/dashboard-geral-content.tsx
  'use client';

  import { useDashboardGeral } from '@/lib/hooks/useDashboards';
  import { KPICard } from '@/components/dashboards/kpi-card';
  import { LineChart } from '@/components/charts/line-chart';
  import { LoadingScreen } from '@/components/ui/loading-screen';
  import { EmptyState } from '@/components/ui/empty-state';
  import { DollarSign, TrendingUp, TrendingDown } from 'lucide-react';
  import { Skeleton } from '@/components/ui/skeleton';

  export function DashboardGeralContent() {
    const { data, isLoading, error } = useDashboardGeral();

    if (isLoading) {
      return <DashboardGeralSkeleton />;
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

    const { financial_summary, evolution_chart } = data;

    // Preparar dados do gráfico de evolução
    const chartData = evolution_chart.months.map((month, index) => ({
      mes: month,
      receita: evolution_chart.receita[index],
      despesa: evolution_chart.despesa[index],
      lucro: evolution_chart.lucro[index],
    }));

    return (
      <div className="space-y-6">
        {/* KPIs */}
        <div className="grid gap-4 md:grid-cols-3">
          <KPICard
            title="Receita Total"
            value={financial_summary.receita}
            change={financial_summary.variacao_receita}
            changeType={
              financial_summary.variacao_receita && financial_summary.variacao_receita > 0
                ? 'increase'
                : 'decrease'
            }
            format="currency"
            icon={DollarSign}
          />
          <KPICard
            title="Despesa Total"
            value={financial_summary.despesa}
            change={financial_summary.variacao_despesa}
            changeType={
              financial_summary.variacao_despesa && financial_summary.variacao_despesa > 0
                ? 'increase'
                : 'decrease'
            }
            format="currency"
            icon={TrendingDown}
          />
          <KPICard
            title="Lucro"
            value={financial_summary.lucro}
            change={financial_summary.variacao_lucro}
            changeType={
              financial_summary.variacao_lucro && financial_summary.variacao_lucro > 0
                ? 'increase'
                : 'decrease'
            }
            format="currency"
            icon={TrendingUp}
          />
        </div>

        {/* Gráfico de Evolução */}
        <LineChart
          title="Evolução Financeira Mensal"
          data={chartData}
          xAxisKey="mes"
          lines={[
            { dataKey: 'receita', name: 'Receita', color: '#10b981' },
            { dataKey: 'despesa', name: 'Despesa', color: '#ef4444' },
            { dataKey: 'lucro', name: 'Lucro', color: '#3b82f6' },
          ]}
          height={400}
        />
      </div>
    );
  }

  function DashboardGeralSkeleton() {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
        <Skeleton className="h-96" />
      </div>
    );
  }
  ```

---

### 3. Dashboard de Finanças - Estrutura

- [ ] **3.1** Criar página do Dashboard de Finanças
  ```typescript
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
  ```

- [ ] **3.2** Criar componente de conteúdo do Dashboard de Finanças
  ```typescript
  // src/components/dashboards/financas/dashboard-financas-content.tsx
  'use client';

  import { useDashboardFinancas } from '@/lib/hooks/useDashboards';
  import { KPICard } from '@/components/dashboards/kpi-card';
  import { LineChart } from '@/components/charts/line-chart';
  import { BarChart } from '@/components/charts/bar-chart';
  import { LoadingScreen } from '@/components/ui/loading-screen';
  import { EmptyState } from '@/components/ui/empty-state';
  import { DollarSign, TrendingUp, TrendingDown } from 'lucide-react';
  import { Skeleton } from '@/components/ui/skeleton';

  export function DashboardFinancasContent() {
    const { data, isLoading, error } = useDashboardFinancas();

    if (isLoading) {
      return <DashboardFinancasSkeleton />;
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

    const { financial_summary, evolution_chart, top_expenses, top_revenues } = data;

    // Preparar dados dos gráficos
    const chartData = evolution_chart.months.map((month, index) => ({
      mes: month,
      receita: evolution_chart.receita[index],
      despesa: evolution_chart.despesa[index],
      lucro: evolution_chart.lucro[index],
    }));

    // Preparar dados de top despesas
    const expensesData = Object.entries(top_expenses).map(([categoria, valor]) => ({
      categoria,
      valor: valor as number,
    }));

    // Preparar dados de top receitas
    const revenuesData = Object.entries(top_revenues).map(([categoria, valor]) => ({
      categoria,
      valor: valor as number,
    }));

    return (
      <div className="space-y-6">
        {/* KPIs */}
        <div className="grid gap-4 md:grid-cols-3">
          <KPICard
            title="Receita Total"
            value={financial_summary.receita}
            change={financial_summary.variacao_receita}
            changeType={
              financial_summary.variacao_receita && financial_summary.variacao_receita > 0
                ? 'increase'
                : 'decrease'
            }
            format="currency"
            icon={DollarSign}
          />
          <KPICard
            title="Despesa Total"
            value={financial_summary.despesa}
            change={financial_summary.variacao_despesa}
            changeType={
              financial_summary.variacao_despesa && financial_summary.variacao_despesa > 0
                ? 'increase'
                : 'decrease'
            }
            format="currency"
            icon={TrendingDown}
          />
          <KPICard
            title="Lucro"
            value={financial_summary.lucro}
            change={financial_summary.variacao_lucro}
            changeType={
              financial_summary.variacao_lucro && financial_summary.variacao_lucro > 0
                ? 'increase'
                : 'decrease'
            }
            format="currency"
            icon={TrendingUp}
          />
        </div>

        {/* Gráfico de Evolução */}
        <LineChart
          title="Evolução Financeira Mensal"
          data={chartData}
          xAxisKey="mes"
          lines={[
            { dataKey: 'receita', name: 'Receita', color: '#10b981' },
            { dataKey: 'despesa', name: 'Despesa', color: '#ef4444' },
            { dataKey: 'lucro', name: 'Lucro', color: '#3b82f6' },
          ]}
          height={400}
        />

        {/* Gráficos de Top Despesas e Receitas */}
        <div className="grid gap-6 lg:grid-cols-2">
          <BarChart
            title="Top 5 Despesas"
            data={expensesData}
            xAxisKey="categoria"
            bars={[{ dataKey: 'valor', name: 'Valor', color: '#ef4444' }]}
            layout="vertical"
            height={300}
          />
          <BarChart
            title="Top 5 Receitas"
            data={revenuesData}
            xAxisKey="categoria"
            bars={[{ dataKey: 'valor', name: 'Valor', color: '#10b981' }]}
            layout="vertical"
            height={300}
          />
        </div>
      </div>
    );
  }

  function DashboardFinancasSkeleton() {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
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

### 4. Componente de Tabela de Dados

- [ ] **4.1** Criar componente DataTable
  ```typescript
  // src/components/ui/data-table.tsx
  import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from '@/components/ui/table';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

  interface Column {
    key: string;
    label: string;
    format?: (value: any) => string;
  }

  interface DataTableProps {
    title?: string;
    columns: Column[];
    data: any[];
    emptyMessage?: string;
  }

  export function DataTable({ title, columns, data, emptyMessage = 'Nenhum dado disponível' }: DataTableProps) {
    return (
      <Card>
        {title && (
          <CardHeader>
            <CardTitle>{title}</CardTitle>
          </CardHeader>
        )}
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  {columns.map((column) => (
                    <TableHead key={column.key}>{column.label}</TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={columns.length} className="text-center text-muted-foreground">
                      {emptyMessage}
                    </TableCell>
                  </TableRow>
                ) : (
                  data.map((row, index) => (
                    <TableRow key={index}>
                      {columns.map((column) => (
                        <TableCell key={column.key}>
                          {column.format ? column.format(row[column.key]) : row[column.key]}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    );
  }
  ```

- [ ] **4.2** Criar componente Table (primitivo)
  ```typescript
  // src/components/ui/table.tsx
  import * as React from 'react';
  import { cn } from '@/lib/utils';

  const Table = React.forwardRef<
    HTMLTableElement,
    React.HTMLAttributes<HTMLTableElement>
  >(({ className, ...props }, ref) => (
    <div className="w-full overflow-auto">
      <table
        ref={ref}
        className={cn('w-full caption-bottom text-sm', className)}
        {...props}
      />
    </div>
  ));
  Table.displayName = 'Table';

  const TableHeader = React.forwardRef<
    HTMLTableSectionElement,
    React.HTMLAttributes<HTMLTableSectionElement>
  >(({ className, ...props }, ref) => (
    <thead ref={ref} className={cn('[&_tr]:border-b', className)} {...props} />
  ));
  TableHeader.displayName = 'TableHeader';

  const TableBody = React.forwardRef<
    HTMLTableSectionElement,
    React.HTMLAttributes<HTMLTableSectionElement>
  >(({ className, ...props }, ref) => (
    <tbody
      ref={ref}
      className={cn('[&_tr:last-child]:border-0', className)}
      {...props}
    />
  ));
  TableBody.displayName = 'TableBody';

  const TableRow = React.forwardRef<
    HTMLTableRowElement,
    React.HTMLAttributes<HTMLTableRowElement>
  >(({ className, ...props }, ref) => (
    <tr
      ref={ref}
      className={cn(
        'border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted',
        className
      )}
      {...props}
    />
  ));
  TableRow.displayName = 'TableRow';

  const TableHead = React.forwardRef<
    HTMLTableCellElement,
    React.ThHTMLAttributes<HTMLTableCellElement>
  >(({ className, ...props }, ref) => (
    <th
      ref={ref}
      className={cn(
        'h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0',
        className
      )}
      {...props}
    />
  ));
  TableHead.displayName = 'TableHead';

  const TableCell = React.forwardRef<
    HTMLTableCellElement,
    React.TdHTMLAttributes<HTMLTableCellElement>
  >(({ className, ...props }, ref) => (
    <td
      ref={ref}
      className={cn('p-4 align-middle [&:has([role=checkbox])]:pr-0', className)}
      {...props}
    />
  ));
  TableCell.displayName = 'TableCell';

  export { Table, TableHeader, TableBody, TableRow, TableHead, TableCell };
  ```

---

### 5. Otimização de Performance

- [ ] **5.1** Implementar React.memo em componentes de gráficos
- [ ] **5.2** Implementar lazy loading para gráficos pesados
- [ ] **5.3** Otimizar re-renders com useMemo e useCallback

---

### 6. Responsividade

- [ ] **6.1** Testar dashboards em diferentes resoluções
- [ ] **6.2** Ajustar grid de KPIs para mobile
- [ ] **6.3** Ajustar gráficos para mobile
- [ ] **6.4** Testar scroll horizontal em tabelas

---

### 7. Tratamento de Erros

- [ ] **7.1** Implementar error boundaries
  ```typescript
  // src/components/error-boundary.tsx
  'use client';

  import React from 'react';
  import { EmptyState } from './ui/empty-state';
  import { AlertTriangle } from 'lucide-react';
  import { Button } from './ui/button';

  interface Props {
    children: React.ReactNode;
  }

  interface State {
    hasError: boolean;
    error?: Error;
  }

  export class ErrorBoundary extends React.Component<Props, State> {
    constructor(props: Props) {
      super(props);
      this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): State {
      return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
      console.error('Error caught by boundary:', error, errorInfo);
    }

    render() {
      if (this.state.hasError) {
        return (
          <EmptyState
            icon={AlertTriangle}
            title="Algo deu errado"
            description="Ocorreu um erro inesperado. Por favor, recarregue a página."
            action={
              <Button onClick={() => window.location.reload()}>
                Recarregar Página
              </Button>
            }
          />
        );
      }

      return this.props.children;
    }
  }
  ```

---

### 8. Testes

- [ ] **8.1** Testes unitários dos componentes de gráficos
- [ ] **8.2** Testes de integração do Dashboard Geral
- [ ] **8.3** Testes de integração do Dashboard de Finanças
- [ ] **8.4** Testes de responsividade
- [ ] **8.5** Testes de performance com grandes volumes de dados

---

### 9. Documentação

- [ ] **9.1** Documentar componentes de gráficos
- [ ] **9.2** Documentar estrutura dos dashboards
- [ ] **9.3** Criar guia de como adicionar novos gráficos
- [ ] **9.4** Documentar padrões de formatação de dados

---

### 10. Verificação e Commit

- [ ] **10.1** Executar testes
  ```bash
  npm test
  ```

- [ ] **10.2** Verificar performance
- [ ] **10.3** Testar em diferentes navegadores
- [ ] **10.4** Commit das mudanças
  ```bash
  git add .
  git commit -m "feat: implementar dashboards geral e finanças"
  ```

---

## ✅ Critérios de Conclusão da Fase 4

A Fase 4 está completa quando:

- [x] Dashboard Geral totalmente funcional
- [x] Dashboard de Finanças totalmente funcional
- [x] Componentes de gráficos reutilizáveis criados
- [x] Dados da API integrados corretamente
- [x] Dashboards responsivos
- [x] Performance otimizada
- [x] Testes passando
- [x] Documentação atualizada

---

## 📝 Notas e Observações

### Decisões Técnicas

1. **Recharts**: Escolhido pela facilidade de uso e boa integração com React
2. **Skeletons**: Implementados para melhor UX durante carregamento
3. **Error Boundaries**: Essenciais para capturar erros de renderização

### Próximos Passos

- Prosseguir para [Fase 5: Dashboards - Parte 2](./MIGRATION_PHASE_5.md)

---

**Status**: ⏳ Pendente  
**Responsável**: [Nome]  
**Data de Início**: [Data]  
**Data de Conclusão**: [Data]
