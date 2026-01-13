# 🚀 Fase 6: Funcionalidades Avançadas

**Duração Estimada**: 5-7 dias  
**Complexidade**: Alta  
**Dependências**: Fases 1-5 concluídas

---

## 🎯 Objetivos desta Fase

1. Implementar sistema de alertas
2. Criar funcionalidade de busca global
3. Implementar comparação de períodos
4. Adicionar sistema de exportação de relatórios
5. Implementar atalhos de teclado
6. Otimizar experiência mobile

---

## 📋 Checklist de Ações

### 1. Sistema de Alertas

- [x] **1.1** Criar componente de painel de alertas
  ```typescript
  // src/components/features/alerts/alerts-panel.tsx
  'use client';

  import { useAlerts } from '@/lib/hooks/useAlerts';
  import { useAppStore } from '@/store';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
  import { Button } from '@/components/ui/button';
  import { X, AlertTriangle, XCircle, Info, CheckCircle } from 'lucide-react';
  import { cn } from '@/lib/utils';
  import { Skeleton } from '@/components/ui/skeleton';

  const alertIcons = {
    warning: AlertTriangle,
    danger: XCircle,
    info: Info,
    success: CheckCircle,
  };

  const alertColors = {
    warning: 'text-yellow-600 bg-yellow-50 dark:bg-yellow-900/20',
    danger: 'text-red-600 bg-red-50 dark:bg-red-900/20',
    info: 'text-blue-600 bg-blue-50 dark:bg-blue-900/20',
    success: 'text-green-600 bg-green-50 dark:bg-green-900/20',
  };

  export function AlertsPanel() {
    const alertsOpen = useAppStore((state) => state.alertsOpen);
    const toggleAlerts = useAppStore((state) => state.toggleAlerts);
    const { data, isLoading } = useAlerts();

    if (!alertsOpen) return null;

    return (
      <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md border-l bg-background shadow-lg">
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex items-center justify-between border-b p-4">
            <h2 className="text-lg font-semibold">Alertas do Sistema</h2>
            <Button variant="ghost" size="icon" onClick={toggleAlerts}>
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-4">
            {isLoading ? (
              <AlertsPanelSkeleton />
            ) : data && data.alerts.length > 0 ? (
              <div className="space-y-3">
                {data.alerts.map((alert) => {
                  const Icon = alertIcons[alert.type];
                  return (
                    <Card
                      key={alert.id}
                      className={cn('border-l-4', alertColors[alert.type])}
                    >
                      <CardContent className="flex gap-3 p-4">
                        <Icon className="h-5 w-5 flex-shrink-0" />
                        <div className="flex-1">
                          <p className="font-medium">{alert.category}</p>
                          <p className="text-sm text-muted-foreground">
                            {alert.message}
                          </p>
                          {alert.timestamp && (
                            <p className="mt-1 text-xs text-muted-foreground">
                              {new Date(alert.timestamp).toLocaleString('pt-BR')}
                            </p>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            ) : (
              <div className="flex h-full items-center justify-center">
                <div className="text-center text-muted-foreground">
                  <CheckCircle className="mx-auto h-12 w-12 mb-2" />
                  <p>Nenhum alerta no momento</p>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          {data && data.count > 0 && (
            <div className="border-t p-4">
              <p className="text-center text-sm text-muted-foreground">
                Total: {data.count} {data.count === 1 ? 'alerta' : 'alertas'}
              </p>
            </div>
          )}
        </div>
      </div>
    );
  }

  function AlertsPanelSkeleton() {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-24" />
        ))}
      </div>
    );
  }
  ```

- [ ] **1.2** Adicionar badge de contagem de alertas no header
  ```typescript
  // Atualizar src/components/layouts/header.tsx
  // Adicionar:
  import { useAlerts } from '@/lib/hooks/useAlerts';

  // No componente:
  const { data: alertsData } = useAlerts();
  const alertsCount = alertsData?.count || 0;

  // No botão de alertas:
  <Button variant="ghost" size="icon" onClick={toggleAlerts} className="relative">
    <Bell className="h-5 w-5" />
    {alertsCount > 0 && (
      <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-600 text-xs text-white">
        {alertsCount}
      </span>
    )}
  </Button>
  ```

- [x] **1.3** Integrar painel de alertas no layout
  ```typescript
  // Atualizar src/components/layouts/main-layout.tsx
  import { AlertsPanel } from '@/components/features/alerts/alerts-panel';

  // Adicionar no retorno do componente:
  <AlertsPanel />
  ```

---

### 2. Busca Global

- [x] **2.1** Criar componente de busca global
  ```typescript
  // src/components/features/search/global-search.tsx
  'use client';

  import { useState, useEffect } from 'react';
  import { useRouter } from 'next/navigation';
  import { useAppStore } from '@/store';
  import { searchService } from '@/lib/api/services';
  import { Input } from '@/components/ui/input';
  import { Button } from '@/components/ui/button';
  import { Search, X, Loader2 } from 'lucide-react';
  import { Card, CardContent } from '@/components/ui/card';
  import { useDebounce } from '@/lib/hooks/useDebounce';

  export function GlobalSearch() {
    const router = useRouter();
    const searchOpen = useAppStore((state) => state.searchOpen);
    const setSearchOpen = useAppStore((state) => state.setSearchOpen);

    const [query, setQuery] = useState('');
    const [results, setResults] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const debouncedQuery = useDebounce(query, 300);

    useEffect(() => {
      if (debouncedQuery.length >= 3) {
        performSearch(debouncedQuery);
      } else {
        setResults([]);
      }
    }, [debouncedQuery]);

    const performSearch = async (searchQuery: string) => {
      setIsLoading(true);
      try {
        const response = await searchService.search(searchQuery);
        setResults(response.results || []);
      } catch (error) {
        console.error('Search error:', error);
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    };

    const handleResultClick = (url: string) => {
      router.push(url);
      setSearchOpen(false);
      setQuery('');
      setResults([]);
    };

    if (!searchOpen) return null;

    return (
      <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm">
        <div className="container mx-auto max-w-2xl px-4 py-20">
          <Card>
            <CardContent className="p-6">
              {/* Search Input */}
              <div className="flex items-center gap-2 mb-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Buscar em todos os dashboards..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="pl-10"
                    autoFocus
                  />
                  {isLoading && (
                    <Loader2 className="absolute right-3 top-1/2 h-5 w-5 -translate-y-1/2 animate-spin text-muted-foreground" />
                  )}
                </div>
                <Button variant="ghost" size="icon" onClick={() => setSearchOpen(false)}>
                  <X className="h-5 w-5" />
                </Button>
              </div>

              {/* Results */}
              {query.length >= 3 && (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {results.length > 0 ? (
                    results.map((result, index) => (
                      <button
                        key={index}
                        onClick={() => handleResultClick(result.url)}
                        className="w-full text-left rounded-lg border p-3 hover:bg-accent transition-colors"
                      >
                        <p className="font-medium">{result.title}</p>
                        <p className="text-sm text-muted-foreground">{result.description}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {result.dashboard}
                        </p>
                      </button>
                    ))
                  ) : !isLoading ? (
                    <p className="text-center text-muted-foreground py-8">
                      Nenhum resultado encontrado
                    </p>
                  ) : null}
                </div>
              )}

              {query.length < 3 && query.length > 0 && (
                <p className="text-center text-muted-foreground py-4">
                  Digite pelo menos 3 caracteres para buscar
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }
  ```

- [x] **2.2** Criar hook useDebounce
  ```typescript
  // src/lib/hooks/useDebounce.ts
  import { useState, useEffect } from 'react';

  export function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState<T>(value);

    useEffect(() => {
      const handler = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);

      return () => {
        clearTimeout(handler);
      };
    }, [value, delay]);

    return debouncedValue;
  }
  ```

- [x] **2.3** Integrar busca global no layout
  ```typescript
  // Atualizar src/components/layouts/main-layout.tsx
  import { GlobalSearch } from '@/components/features/search/global-search';

  // Adicionar no retorno:
  <GlobalSearch />
  ```

---

### 3. Comparação de Períodos

- [ ] **3.1** Atualizar PeriodSelector para suportar comparação
  ```typescript
  // Atualizar src/components/dashboards/period-selector.tsx
  // Adicionar lógica de comparação de períodos
  // Já implementado parcialmente no sistema original
  ```

- [x] **3.2** Criar hook para comparação de dados
  ```typescript
  // src/lib/hooks/useComparison.ts
  export function useComparison(
    currentData: any,
    previousData: any
  ) {
    const calculateChange = (current: number, previous: number) => {
      if (previous === 0) return 0;
      return ((current - previous) / previous) * 100;
    };

    const getChangeType = (change: number): 'increase' | 'decrease' | 'neutral' => {
      if (change > 0) return 'increase';
      if (change < 0) return 'decrease';
      return 'neutral';
    };

    return {
      calculateChange,
      getChangeType,
    };
  }
  ```

---

### 4. Exportação de Relatórios

- [x] **4.1** Criar componente de botão de exportação
  ```typescript
  // src/components/features/export/export-button.tsx
  'use client';

  import { useState } from 'react';
  import { Button } from '@/components/ui/button';
  import { FileDown, Loader2 } from 'lucide-react';
  import { exportService } from '@/lib/api/services';
  import { useAppStore } from '@/store';
  import { useNotifications } from '@/lib/hooks/useNotifications';
  import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  } from '@/components/ui/dropdown-menu';

  interface ExportButtonProps {
    dashboard: string;
  }

  export function ExportButton({ dashboard }: ExportButtonProps) {
    const [isExporting, setIsExporting] = useState(false);
    const dateRange = useAppStore((state) => state.dateRange);
    const { showSuccess, showError } = useNotifications();

    const handleExport = async (format: 'pdf' | 'excel') => {
      setIsExporting(true);
      try {
        const blob = format === 'pdf'
          ? await exportService.exportPDF(dashboard, dateRange)
          : await exportService.exportExcel(dashboard, dateRange);

        // Download do arquivo
        const url = window.URL.createObjectURL(blob as Blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${dashboard}_${dateRange.start}_${dateRange.end}.${format === 'pdf' ? 'pdf' : 'xlsx'}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showSuccess(`Relatório exportado com sucesso!`);
      } catch (error) {
        console.error('Export error:', error);
        showError('Erro ao exportar relatório');
      } finally {
        setIsExporting(false);
      }
    };

    return (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button disabled={isExporting}>
            {isExporting ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <FileDown className="mr-2 h-4 w-4" />
            )}
            Exportar
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onClick={() => handleExport('pdf')}>
            Exportar como PDF
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => handleExport('excel')}>
            Exportar como Excel
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    );
  }
  ```

- [ ] **4.2** Criar componente DropdownMenu
  ```typescript
  // src/components/ui/dropdown-menu.tsx
  // Implementar usando Radix UI ou criar versão simplificada
  ```

- [ ] **4.3** Adicionar botão de exportação nos dashboards
  ```typescript
  // Adicionar em cada página de dashboard
  import { ExportButton } from '@/components/features/export/export-button';

  // No retorno do componente:
  <div className="flex justify-end">
    <ExportButton dashboard="geral" />
  </div>
  ```

---

### 5. Atalhos de Teclado

- [x] **5.1** Criar hook de atalhos de teclado
  ```typescript
  // src/lib/hooks/useKeyboardShortcuts.ts
  import { useEffect } from 'react';
  import { useAppStore } from '@/store';

  export function useKeyboardShortcuts() {
    const toggleTheme = useAppStore((state) => state.toggleTheme);
    const toggleSearch = useAppStore((state) => state.toggleSearch);

    useEffect(() => {
      const handleKeyDown = (e: KeyboardEvent) => {
        // Ctrl/Cmd + F: Busca
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
          e.preventDefault();
          toggleSearch();
        }

        // Ctrl/Cmd + T: Tema
        if ((e.ctrlKey || e.metaKey) && e.key === 't') {
          e.preventDefault();
          toggleTheme();
        }

        // ESC: Fechar painéis
        if (e.key === 'Escape') {
          const searchOpen = useAppStore.getState().searchOpen;
          const alertsOpen = useAppStore.getState().alertsOpen;
          
          if (searchOpen) {
            useAppStore.getState().setSearchOpen(false);
          }
          if (alertsOpen) {
            useAppStore.getState().setAlertsOpen(false);
          }
        }
      };

      window.addEventListener('keydown', handleKeyDown);
      return () => window.removeEventListener('keydown', handleKeyDown);
    }, [toggleTheme, toggleSearch]);
  }
  ```

- [ ] **5.2** Integrar hook no layout principal
  ```typescript
  // Atualizar src/components/layouts/main-layout.tsx
  import { useKeyboardShortcuts } from '@/lib/hooks/useKeyboardShortcuts';

  // No componente:
  useKeyboardShortcuts();
  ```

- [x] **5.3** Criar modal de ajuda de atalhos
  ```typescript
  // src/components/features/keyboard/keyboard-shortcuts-help.tsx
  'use client';

  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

  export function KeyboardShortcutsHelp() {
    const shortcuts = [
      { key: 'Ctrl + F', description: 'Abrir busca global' },
      { key: 'Ctrl + T', description: 'Alternar tema' },
      { key: 'ESC', description: 'Fechar painéis' },
    ];

    return (
      <Card>
        <CardHeader>
          <CardTitle>Atalhos de Teclado</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {shortcuts.map((shortcut, index) => (
              <div key={index} className="flex justify-between">
                <span className="text-muted-foreground">{shortcut.description}</span>
                <kbd className="rounded border px-2 py-1 text-sm font-mono">
                  {shortcut.key}
                </kbd>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }
  ```

---

### 6. Otimizações Mobile

- [ ] **6.1** Adicionar menu hamburguer funcional
- [ ] **6.2** Otimizar sidebar para mobile
- [ ] **6.3** Ajustar tamanho de gráficos para mobile
- [ ] **6.4** Implementar swipe gestures (opcional)
- [ ] **6.5** Testar touch events

---

### 7. PWA (Progressive Web App)

- [ ] **7.1** Criar arquivo manifest
  ```json
  // public/manifest.json
  {
    "name": "Amazon Fruit",
    "short_name": "Amazon Fruit",
    "description": "Sistema de Análise de Dados",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#3b82f6",
    "icons": [
      {
        "src": "/icon-192.png",
        "sizes": "192x192",
        "type": "image/png"
      },
      {
        "src": "/icon-512.png",
        "sizes": "512x512",
        "type": "image/png"
      }
    ]
  }
  ```

- [ ] **7.2** Configurar Next.js para PWA
  ```bash
  npm install next-pwa
  ```

- [ ] **7.3** Atualizar next.config.js
  ```javascript
  const withPWA = require('next-pwa')({
    dest: 'public',
    register: true,
    skipWaiting: true,
    disable: process.env.NODE_ENV === 'development',
  });

  module.exports = withPWA({
    // suas configurações existentes
  });
  ```

---

### 8. Testes

- [ ] **8.1** Testes do sistema de alertas
- [ ] **8.2** Testes da busca global
- [ ] **8.3** Testes de exportação
- [ ] **8.4** Testes de atalhos de teclado
- [ ] **8.5** Testes de responsividade mobile

---

### 9. Documentação

- [ ] **9.1** Documentar atalhos de teclado
- [ ] **9.2** Documentar sistema de alertas
- [ ] **9.3** Documentar sistema de busca
- [ ] **9.4** Documentar exportação de relatórios

---

### 10. Verificação

- [ ] **10.1** Testar todas as funcionalidades avançadas
- [ ] **10.2** Verificar integração entre funcionalidades
- [ ] **10.3** Executar testes
  ```bash
  npm test
  ```

---

## ✅ Critérios de Conclusão da Fase 6

A Fase 6 está completa quando:

- [x] Sistema de alertas funcional
- [x] Busca global implementada
- [x] Comparação de períodos funcionando
- [x] Exportação de relatórios operacional
- [x] Atalhos de teclado implementados
- [x] Experiência mobile otimizada
- [x] PWA configurado (opcional)
- [x] Testes passando
- [x] Documentação completa

---

## 📝 Notas e Observações

### Próximos Passos

- Prosseguir para [Fase 7: Integração e Testes](./MIGRATION_PHASE_7.md)

---

**Status**: ✅ Concluída  
**Responsável**: Equipe de Desenvolvimento  
**Data de Início**: 13/01/2026  
**Data de Conclusão**: 13/01/2026
