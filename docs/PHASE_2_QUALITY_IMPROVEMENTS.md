# 🎨 Fase 2: Aprimoramento e Qualidade

**Duração estimada:** 1 mês  
**Prioridade:** 🟡 Importante  
**Status:** 🟡 Não iniciado  
**Pré-requisito:** [Fase 1](../docs/PHASE_1_CRITICAL_FOUNDATIONS.md) concluída

## 📋 Visão Geral

Esta fase foca em melhorias de qualidade, performance, experiência do usuário e ferramentas de desenvolvimento que elevam o nível profissional do projeto.

## 🎯 Objetivos

- 📚 Documentar componentes visualmente (Storybook)
- 🧪 Garantir qualidade com testes E2E
- 🐛 Implementar rastreamento de erros
- ⚡ Otimizar performance (loading states e memoização)
- 📊 Adicionar monitoramento básico

---

## ✅ Checklist de Implementação

### 1. Storybook - Documentação Visual

#### 1.1 Setup Inicial
- [ ] Instalar Storybook para Next.js
- [ ] Configurar Storybook com TypeScript
- [ ] Configurar integração com Tailwind CSS
- [ ] Adicionar addons essenciais (controls, actions, a11y)

**Comando:**
```bash
npx storybook@latest init
```

**Addons recomendados:**
- `@storybook/addon-essentials`
- `@storybook/addon-a11y`
- `@storybook/addon-interactions`

#### 1.2 Documentar Componentes UI Base
- [ ] Button - todas as variantes e estados
- [ ] Card - com diferentes conteúdos
- [ ] Input - todos os tipos e estados
- [ ] Dialog - modal e comportamento
- [ ] Dropdown Menu - todos os estados
- [ ] Skeleton - variações de loading
- [ ] Spinner - diferentes tamanhos

**Estrutura sugerida:**
```
src/components/ui/
  button.stories.tsx
  card.stories.tsx
  ...
```

#### 1.3 Documentar Componentes de Dashboard
- [ ] KPICard - com diferentes métricas
- [ ] PeriodSelector - estados e interações
- [ ] LineChart - diferentes configurações
- [ ] BarChart - variações
- [ ] PieChart - exemplos diversos

#### 1.4 Documentar Features
- [ ] GlobalSearch - estados de busca
- [ ] AlertsPanel - diferentes tipos de alertas
- [ ] ExportButton - estados de exportação

#### 1.5 Configuração Avançada
- [ ] Adicionar documentação MDX para cada componente
- [ ] Configurar accessibility checks automáticos
- [ ] Adicionar visual regression testing (Chromatic - opcional)
- [ ] Integrar Storybook no CI/CD

**Arquivos de configuração:**
- `.storybook/main.ts`
- `.storybook/preview.ts`

**Progresso:** 0/5 tarefas concluídas

---

### 2. Testes E2E com Playwright

#### 2.1 Setup Inicial
- [ ] Instalar Playwright
- [ ] Configurar Playwright para Next.js
- [ ] Criar estrutura de testes E2E
- [ ] Configurar browsers para teste (Chromium, Firefox, WebKit)

**Comandos:**
```bash
npm install --save-dev @playwright/test
npx playwright install
```

**Arquivo:** `playwright.config.ts`

#### 2.2 Testes de Navegação
- [ ] Teste: Navegação entre dashboards
- [ ] Teste: Navegação via sidebar
- [ ] Teste: Navegação via busca global
- [ ] Teste: Responsividade mobile/desktop

**Arquivos:**
- `tests/e2e/navigation.spec.ts`

#### 2.3 Testes de Funcionalidades
- [ ] Teste: Seleção de período de datas
- [ ] Teste: Aplicar filtros de período
- [ ] Teste: Exportação de dados (simulado)
- [ ] Teste: Busca global funcional
- [ ] Teste: Abertura/fechamento de painéis (alerts, search)

**Arquivos:**
- `tests/e2e/features.spec.ts`

#### 2.4 Testes de Dashboard Específicos
- [ ] Teste: Dashboard Geral carrega e exibe dados
- [ ] Teste: Dashboard Finanças interage corretamente
- [ ] Teste: Dashboard Estoque mostra alertas
- [ ] Teste: Gráficos renderizam corretamente

**Arquivos:**
- `tests/e2e/dashboards.spec.ts`

#### 2.5 Testes de Acessibilidade E2E
- [ ] Teste: Navegação por teclado funciona
- [ ] Teste: Screen reader compatibility (usando axe-core)
- [ ] Teste: Contraste de cores em diferentes componentes
- [ ] Teste: Foco visível em todos os elementos interativos

**Arquivos:**
- `tests/e2e/accessibility.spec.ts`

#### 2.6 Integração com CI/CD
- [ ] Adicionar testes E2E ao workflow do GitHub Actions
- [ ] Configurar relatórios de teste (HTML reports)
- [ ] Adicionar screenshots de falhas
- [ ] Configurar execução em diferentes browsers

**Arquivo:** `.github/workflows/ci.yml`

**Progresso:** 0/6 tarefas concluídas

---

### 3. Error Tracking com Sentry

#### 3.1 Setup Inicial
- [ ] Criar conta no Sentry (ou usar self-hosted)
- [ ] Instalar `@sentry/nextjs`
- [ ] Configurar Sentry no Next.js
- [ ] Configurar variáveis de ambiente

**Comando:**
```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

**Arquivos:**
- `sentry.client.config.ts`
- `sentry.server.config.ts`
- `sentry.edge.config.ts`

#### 3.2 Configuração Básica
- [ ] Configurar DSN no `.env.local`
- [ ] Configurar environment (development/production)
- [ ] Configurar release tracking
- [ ] Configurar sample rate (100% em dev, reduzir em prod)

#### 3.3 Integração com Error Boundaries
- [ ] Conectar Error Boundaries ao Sentry
- [ ] Enviar contexto adicional (user, route, etc)
- [ ] Agrupar erros relacionados
- [ ] Adicionar breadcrumbs importantes

**Arquivo:** `src/components/error-boundary.tsx`

#### 3.4 Monitoramento de Performance
- [ ] Configurar performance monitoring
- [ ] Rastrear transações importantes (page loads, API calls)
- [ ] Configurar alertas para erros críticos
- [ ] Dashboard de erros e performance

#### 3.5 Source Maps e Debug
- [ ] Configurar upload de source maps
- [ ] Configurar release management
- [ ] Testar tracking em ambiente de staging

**Progresso:** 0/5 tarefas concluídas

---

### 4. Performance - Loading States e Memoização

#### 4.1 Skeleton Loaders Específicos
- [ ] Criar DashboardSkeleton genérico
- [ ] Criar ChartSkeleton para gráficos
- [ ] Criar TableSkeleton para tabelas
- [ ] Criar KPICardSkeleton para cards de métricas
- [ ] Substituir Skeleton genérico pelos específicos

**Arquivos:**
- `src/components/ui/skeletons/dashboard-skeleton.tsx`
- `src/components/ui/skeletons/chart-skeleton.tsx`
- `src/components/ui/skeletons/table-skeleton.tsx`
- `src/components/ui/skeletons/kpi-skeleton.tsx`

#### 4.2 Indicadores de Progresso
- [ ] Adicionar barra de progresso para operações longas
- [ ] Indicador de "Carregando X de Y itens"
- [ ] Estimativa de tempo restante (se aplicável)
- [ ] Feedback visual durante operações assíncronas

#### 4.3 Memoização de Componentes
- [ ] Envolver LineChart com React.memo
- [ ] Envolver BarChart com React.memo
- [ ] Envolver PieChart com React.memo
- [ ] Envolver KPICard com React.memo
- [ ] Verificar impacto na performance

**Arquivos afetados:**
- `src/components/charts/line-chart.tsx`
- `src/components/charts/bar-chart.tsx`
- `src/components/charts/pie-chart.tsx`
- `src/components/dashboards/kpi-card.tsx`

#### 4.4 Memoização de Dados
- [ ] Usar useMemo para dados de gráficos
- [ ] Usar useMemo para cálculos pesados
- [ ] Usar useCallback para handlers passados como props
- [ ] Medir impacto antes/depois

**Exemplo:**
```tsx
const chartData = useMemo(() => {
  return evolution_chart.months.map((month, index) => ({
    mes: month,
    receita: evolution_chart.receita[index],
    // ...
  }));
}, [evolution_chart]);
```

#### 4.5 Otimização de Re-renders
- [ ] Identificar componentes com re-renders desnecessários
- [ ] Usar React DevTools Profiler
- [ ] Otimizar seletores do Zustand (shallow comparison)
- [ ] Documentar otimizações realizadas

**Progresso:** 0/5 tarefas concluídas

---

### 5. Monitoramento Básico

#### 5.1 Web Vitals Tracking
- [ ] Configurar função `reportWebVitals` no Next.js
- [ ] Enviar métricas para analytics
- [ ] Configurar threshold para métricas importantes
- [ ] Dashboard de Web Vitals

**Arquivo:** `src/app/layout.tsx`

**Código de exemplo:**
```tsx
export function reportWebVitals(metric: NextWebVitalsMetric) {
  // Enviar para analytics/Sentry
  console.log(metric);
}
```

#### 5.2 Analytics Básico
- [ ] Escolher solução (Plausible, Google Analytics, PostHog)
- [ ] Instalar e configurar biblioteca escolhida
- [ ] Rastrear eventos importantes:
  - Visualização de dashboards
  - Exportações de dados
  - Uso de busca global
  - Mudanças de período
- [ ] Configurar privacidade (GDPR compliance)

**Opções:**
- Plausible (privacy-first)
- Google Analytics 4
- PostHog (open-source)

#### 5.3 Logging Estruturado
- [ ] Escolher biblioteca de logging (Pino, Winston)
- [ ] Configurar níveis de log (debug, info, warn, error)
- [ ] Adicionar contexto aos logs (user, route, timestamp)
- [ ] Configurar log rotation

**Opcional para frontend:**
- Pino (leve, rápido)
- winston (mais features)

#### 5.4 Health Check Endpoint
- [ ] Criar API route `/api/health`
- [ ] Verificar dependências críticas
- [ ] Retornar status da aplicação
- [ ] Usar para monitoramento externo

**Arquivo:** `src/app/api/health/route.ts`

**Progresso:** 0/4 tarefas concluídas

---

## 📊 Métricas de Sucesso

### Antes da Fase 2
- Documentação: ❌ Sem Storybook
- Testes E2E: ❌ Não implementados
- Error Tracking: ❌ Sem Sentry
- Performance: ⚠️ Sem otimizações específicas
- Monitoramento: ❌ Não configurado

### Meta Após Fase 2
- ✅ Storybook com todos os componentes principais documentados
- ✅ Cobertura E2E básica para fluxos críticos
- ✅ Sentry rastreando erros em produção
- ✅ Performance melhorada (menos re-renders, loading states específicos)
- ✅ Web Vitals sendo monitorados

---

## 📝 Notas e Decisões

### Decisões Técnicas
- [ ] Escolher entre Chromatic ou Percy para visual regression (ou nenhum)
- [ ] Decidir sobre estratégia de analytics (privacy-first vs features)
- [ ] Definir quais componentes merecem memoização (testar antes)

### Dependências Externas
- Sentry account ou self-hosted
- Storybook hosting (ou local apenas)
- Analytics service (se escolhido serviço pago)

### Riscos e Mitigações
- **Risco:** Storybook pode ficar desatualizado
  - **Mitigação:** Adicionar ao CI/CD, revisar em PRs de componentes
  
- **Risco:** Testes E2E podem ser lentos
  - **Mitigação:** Rodar em paralelo, apenas smoke tests no CI
  
- **Risco:** Sentry pode gerar custos com muitos erros
  - **Mitigação:** Configurar sample rate, filtrar erros conhecidos

---

## 🔗 Próximos Passos

Após completar a Fase 2, avançar para:
- [Fase 3: Experiência e Profissionalismo](./PHASE_3_EXPERIENCE_POLISH.md)

---

## 📅 Histórico de Atualizações

| Data | Descrição | Responsável |
|------|-----------|-------------|
| {{ data }} | Criação do documento | Equipe |

---

**Total de tarefas:** 25  
**Tarefas concluídas:** 0  
**Progresso:** 0%
