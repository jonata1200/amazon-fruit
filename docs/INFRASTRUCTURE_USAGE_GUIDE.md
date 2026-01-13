# 📘 Guia de Uso da Infraestrutura - Fase 2

Este guia mostra como usar todos os recursos implementados na Fase 2.

---

## 🗂️ Estado Global (Zustand)

### Acessar Estado

```typescript
'use client';

import { useAppStore } from '@/store';

export function MyComponent() {
  // Selecionar um estado específico
  const theme = useAppStore((state) => state.theme);
  const dateRange = useAppStore((state) => state.dateRange);
  const sidebarOpen = useAppStore((state) => state.sidebarOpen);
  
  // Selecionar múltiplos estados
  const { theme, dateRange, toggleTheme } = useAppStore((state) => ({
    theme: state.theme,
    dateRange: state.dateRange,
    toggleTheme: state.toggleTheme,
  }));
  
  return <div>Tema atual: {theme}</div>;
}
```

### Modificar Estado

```typescript
const setDateRange = useAppStore((state) => state.setDateRange);
const toggleTheme = useAppStore((state) => state.toggleTheme);
const toggleSidebar = useAppStore((state) => state.toggleSidebar);

// Uso
setDateRange('2024-01-01', '2024-12-31');
toggleTheme(); // Alterna entre light/dark
toggleSidebar(); // Abre/fecha sidebar
```

---

## 📊 Buscar Dados de Dashboards

### Dashboard Geral

```typescript
'use client';

import { useDashboardGeral } from '@/lib/hooks/useDashboards';

export function DashboardGeralPage() {
  const { data, isLoading, error, refetch } = useDashboardGeral();
  
  if (isLoading) return <div>Carregando...</div>;
  if (error) return <div>Erro ao carregar</div>;
  
  return (
    <div>
      <h1>Receita: {data?.financial_summary.receita}</h1>
      <button onClick={() => refetch()}>Atualizar</button>
    </div>
  );
}
```

### Dashboard com DateRange Customizado

```typescript
const customRange = { start: '2024-01-01', end: '2024-06-30' };
const { data } = useDashboardFinancas(customRange);
```

### Buscar Alertas

```typescript
import { useAlerts } from '@/lib/hooks/useAlerts';

const { data: alertsData } = useAlerts();
const alertsCount = alertsData?.count || 0;
const alerts = alertsData?.alerts || [];
```

---

## 🔔 Sistema de Notificações

```typescript
'use client';

import { useNotifications } from '@/lib/hooks/useNotifications';

export function MyComponent() {
  const { showSuccess, showError, showWarning, showInfo } = useNotifications();
  
  const handleAction = async () => {
    try {
      // ... sua lógica
      showSuccess('Operação realizada com sucesso!');
    } catch (error) {
      showError('Erro ao realizar operação');
    }
  };
  
  return <button onClick={handleAction}>Executar</button>;
}
```

---

## 🎨 Sistema de Temas

### Alternar Tema

```typescript
import { useAppStore } from '@/store';

export function ThemeToggle() {
  const theme = useAppStore((state) => state.theme);
  const toggleTheme = useAppStore((state) => state.toggleTheme);
  
  return (
    <button onClick={toggleTheme}>
      {theme === 'light' ? '🌙 Dark' : '☀️ Light'}
    </button>
  );
}
```

### Usar Tema Atual

```typescript
const theme = useAppStore((state) => state.theme);

<div className={theme === 'dark' ? 'dark-specific-class' : 'light-specific-class'}>
  Conteúdo
</div>
```

---

## 🛠️ Utilitários

### Formatação

```typescript
import { formatCurrency, formatNumber, formatPercentage, formatDate } from '@/lib/utils';

// Exemplos
formatCurrency(1000);           // "R$ 1.000,00"
formatNumber(1234.56, 2);       // "1.234,56"
formatPercentage(15.5);         // "15,5%"
formatDate('2024-01-15');       // "15/01/2024"
formatDateLong('2024-01-15');   // "15 de janeiro de 2024"
```

### Validação

```typescript
import { isValidDate, isValidDateRange, isValidEmail } from '@/lib/utils';

// Exemplos
isValidDate('2024-01-15');                    // true
isValidDateRange('2024-01-01', '2024-12-31'); // true
isValidEmail('user@example.com');             // true
```

### Classes CSS

```typescript
import { cn } from '@/lib/utils';

// Combinar classes Tailwind
<div className={cn(
  'base-class',
  isActive && 'active-class',
  'another-class'
)}>
  Conteúdo
</div>
```

---

## 🌐 Chamar API Diretamente

### Usar Serviços

```typescript
import { dashboardService, alertService, searchService } from '@/lib/api/services';

// Buscar dados
const data = await dashboardService.getDashboardGeral({ 
  start: '2024-01-01', 
  end: '2024-12-31' 
});

// Buscar alertas
const alerts = await alertService.getAlerts();

// Buscar
const results = await searchService.search('financeiro');
```

### Usar Cliente Diretamente

```typescript
import { apiClient } from '@/lib/api/client';

// GET
const data = await apiClient.get<MyType>('/api/endpoint');

// POST
const result = await apiClient.post<MyType>('/api/endpoint', { data: 'value' });
```

---

## 🎯 Constantes

### Dashboards

```typescript
import { DASHBOARDS } from '@/lib/constants';

// Array de todos os dashboards
DASHBOARDS.forEach(dashboard => {
  console.log(dashboard.name, dashboard.path);
});

// Exemplo: Criar menu
<nav>
  {DASHBOARDS.map(dash => (
    <Link key={dash.id} href={dash.path}>
      {dash.name}
    </Link>
  ))}
</nav>
```

### Tipos de Alertas

```typescript
import { ALERT_TYPES } from '@/lib/constants';

const warningConfig = ALERT_TYPES.warning; // { color: 'yellow', icon: 'AlertTriangle' }
```

---

## 🚀 Inicializar Aplicação

```typescript
'use client';

import { useAppInitialization } from '@/lib/hooks/useAppInitialization';

export function DashboardPage() {
  const { isReady } = useAppInitialization();
  
  if (!isReady) {
    return <LoadingScreen message="Inicializando..." />;
  }
  
  // App inicializada, dateRange está disponível
  return <YourDashboard />;
}
```

---

## 📦 Exportação de Relatórios

```typescript
import { exportService } from '@/lib/api/services';
import { useAppStore } from '@/store';

export function ExportButton() {
  const dateRange = useAppStore((state) => state.dateRange);
  
  const handleExportPDF = async () => {
    const blob = await exportService.exportPDF('geral', dateRange);
    // Download do arquivo
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `relatorio_${dateRange.start}_${dateRange.end}.pdf`;
    a.click();
  };
  
  return <button onClick={handleExportPDF}>Exportar PDF</button>;
}
```

---

## 🧪 Exemplo Completo: Componente de Dashboard

```typescript
'use client';

import { useDashboardGeral } from '@/lib/hooks/useDashboards';
import { useAppStore } from '@/store';
import { useNotifications } from '@/lib/hooks/useNotifications';
import { formatCurrency } from '@/lib/utils';

export function DashboardGeral() {
  // Estado global
  const dateRange = useAppStore((state) => state.dateRange);
  const setDateRange = useAppStore((state) => state.setDateRange);
  
  // Dados do dashboard
  const { data, isLoading, error, refetch } = useDashboardGeral();
  
  // Notificações
  const { showSuccess, showError } = useNotifications();
  
  // Handlers
  const handleRefresh = async () => {
    try {
      await refetch();
      showSuccess('Dashboard atualizado!');
    } catch (err) {
      showError('Erro ao atualizar');
    }
  };
  
  const handlePeriodChange = (start: string, end: string) => {
    setDateRange(start, end);
    showInfo('Período alterado');
  };
  
  // Renderização
  if (isLoading) return <Skeleton />;
  if (error) return <ErrorState />;
  if (!data) return <EmptyState />;
  
  return (
    <div>
      <h1>Dashboard Geral</h1>
      <p>Receita: {formatCurrency(data.financial_summary.receita)}</p>
      <p>Período: {dateRange.start} até {dateRange.end}</p>
      <button onClick={handleRefresh}>Atualizar</button>
    </div>
  );
}
```

---

## 📚 Recursos Adicionais

### Documentação Completa
- [Relatório de Verificação](./PHASE_2_VERIFICATION_REPORT.md)
- [Resumo Final](./FASE_2_RESUMO_FINAL.md)
- [Checklist Completo](./MIGRATION_PHASE_2.md)

### Próximos Passos
- Avançar para [Fase 3: Componentes Base](./MIGRATION_PHASE_3.md)

---

**Criado em**: 13/01/2026  
**Versão**: 1.0  
**Status**: ✅ Infraestrutura Completa
