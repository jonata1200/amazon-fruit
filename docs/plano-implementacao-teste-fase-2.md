# 📋 Fase 2: Criação de Testes Unitários Faltantes

## Objetivo
Identificar e criar testes unitários para componentes, hooks e utilitários que ainda não possuem cobertura de testes.

## Contexto
Após a organização dos testes existentes, é necessário garantir que todos os componentes críticos tenham testes unitários adequados. Esta fase foca em preencher as lacunas de cobertura.

---

## ✅ Checklist de Ações

### 1. Análise de Cobertura Atual
- [ ] Executar `npm test -- --coverage` e gerar relatório
- [ ] Identificar componentes sem testes:
  - [ ] Componentes UI sem testes
  - [ ] Componentes de features sem testes
  - [ ] Componentes de dashboards sem testes
  - [ ] Hooks sem testes
  - [ ] Utilitários sem testes
- [ ] Priorizar componentes por criticidade (alta, média, baixa)
- [ ] Documentar gaps de cobertura em `docs/coverage-gaps.md`

### 2. Testes para Componentes UI Faltantes
- [ ] **EmptyState**
  - [ ] Teste de renderização básica
  - [ ] Teste com diferentes props (title, description, icon)
  - [ ] Teste de ação opcional (button)

- [ ] **Icon**
  - [ ] Teste de renderização com diferentes ícones
  - [ ] Teste de tamanhos (xs, sm, md, lg, xl)
  - [ ] Teste de classes customizadas

- [ ] **Label**
  - [ ] Teste de renderização
  - [ ] Teste de associação com input (htmlFor)
  - [ ] Teste de estados (required, disabled)

- [ ] **Progress**
  - [ ] Teste de renderização
  - [ ] Teste de valores (0%, 50%, 100%)
  - [ ] Teste de cores/variantes

- [ ] **Tooltip**
  - [ ] Teste de renderização
  - [ ] Teste de exibição ao hover
  - [ ] Teste de posicionamento

- [ ] **Toaster**
  - [ ] Teste de renderização
  - [ ] Teste de diferentes tipos de toast (success, error, info, warning)
  - [ ] Teste de auto-dismiss

- [ ] **LoadingScreen**
  - [ ] Teste de renderização
  - [ ] Teste de mensagem customizada

- [ ] **Skeleton**
  - [ ] Teste de renderização
  - [ ] Teste de diferentes variantes (text, circle, rectangular)
  - [ ] Teste de animação

- [ ] **Skeletons Específicos**
  - [ ] `chart-skeleton.test.tsx`
  - [ ] `kpi-skeleton.test.tsx`
  - [ ] `table-skeleton.test.tsx`

### 3. Testes para Componentes de Features Faltantes
- [ ] **KeyboardShortcutsHelp**
  - [ ] Teste de renderização
  - [ ] Teste de exibição de atalhos
  - [ ] Teste de toggle (abrir/fechar)

### 4. Testes para Componentes de Dashboards Faltantes
- [ ] **PeriodSelector**
  - [ ] Teste de renderização
  - [ ] Teste de seleção de período
  - [ ] Teste de callback onChange

- [ ] **DashboardSkeleton**
  - [ ] Teste de renderização
  - [ ] Teste de diferentes layouts

- [ ] **Dashboard Contents** (opcional, podem ser testes de integração)
  - [ ] `dashboard-geral-content.test.tsx`
  - [ ] `dashboard-financas-content.test.tsx`
  - [ ] `dashboard-estoque-content.test.tsx`
  - [ ] `dashboard-publico-alvo-content.test.tsx`
  - [ ] `dashboard-fornecedores-content.test.tsx`
  - [ ] `dashboard-rh-content.test.tsx`

### 5. Testes para Componentes de Charts Faltantes
- [ ] **BarChart**
  - [ ] Teste de renderização
  - [ ] Teste com dados válidos
  - [ ] Teste com dados vazios
  - [ ] Teste de responsividade

- [ ] **LineChart**
  - [ ] Teste de renderização
  - [ ] Teste com dados válidos
  - [ ] Teste com dados vazios
  - [ ] Teste de múltiplas séries

- [ ] **PieChart**
  - [ ] Teste de renderização
  - [ ] Teste com dados válidos
  - [ ] Teste com dados vazios
  - [ ] Teste de interatividade (hover, click)

### 6. Testes para Componentes de Layout Faltantes
- [ ] **Header**
  - [ ] Teste de renderização
  - [ ] Teste de navegação
  - [ ] Teste de busca global (integração)
  - [ ] Teste de tema toggle

- [ ] **Sidebar**
  - [ ] Teste de renderização
  - [ ] Teste de navegação entre dashboards
  - [ ] Teste de estado ativo
  - [ ] Teste de collapse/expand

- [ ] **Footer**
  - [ ] Teste de renderização
  - [ ] Teste de links

- [ ] **MainLayout**
  - [ ] Teste de renderização
  - [ ] Teste de composição (Header + Sidebar + Content + Footer)

### 7. Testes para Hooks Faltantes
- [ ] **useAlerts**
  - [ ] Teste de criação de alerta
  - [ ] Teste de remoção de alerta
  - [ ] Teste de atualização de alerta
  - [ ] Teste de filtros

- [ ] **useAnalytics**
  - [ ] Teste de tracking de eventos
  - [ ] Teste de page views
  - [ ] Teste de métricas customizadas

- [ ] **useAppInitialization**
  - [ ] Teste de inicialização
  - [ ] Teste de carregamento de dados
  - [ ] Teste de tratamento de erros

- [ ] **useDashboards**
  - [ ] Teste de busca de dashboards
  - [ ] Teste de filtros
  - [ ] Teste de ordenação

- [ ] **useKeyboardShortcuts**
  - [ ] Teste de registro de atalhos
  - [ ] Teste de execução de callbacks
  - [ ] Teste de remoção de atalhos

- [ ] **useNotifications**
  - [ ] Teste de criação de notificação
  - [ ] Teste de remoção automática
  - [ ] Teste de diferentes tipos

### 8. Testes para Utilitários Faltantes
- [ ] **lib/utils/**
  - [ ] Teste de `cn()` (classNames utility)
  - [ ] Teste de formatação de números
  - [ ] Teste de formatação de datas
  - [ ] Teste de validações
  - [ ] Teste de transformações de dados

- [ ] **lib/api/**
  - [ ] Teste de cliente API
  - [ ] Teste de interceptors
  - [ ] Teste de tratamento de erros
  - [ ] Teste de retry logic

- [ ] **lib/validation/**
  - [ ] Teste de schemas Zod
  - [ ] Teste de validações customizadas

### 9. Testes para Store (Zustand)
- [ ] **store/slices/**
  - [ ] Teste de cada slice do store
  - [ ] Teste de ações (actions)
  - [ ] Teste de seletores (selectors)
  - [ ] Teste de estado inicial
  - [ ] Teste de persistência (se aplicável)

### 10. Melhorias em Testes Existentes
- [ ] Revisar testes existentes e adicionar casos de borda
- [ ] Adicionar testes de acessibilidade onde faltam
- [ ] Adicionar testes de responsividade onde relevante
- [ ] Melhorar mocks e fixtures

### 11. Validação e Cobertura
- [ ] Executar `npm test -- --coverage` após cada grupo de testes
- [ ] Verificar se a cobertura aumentou significativamente
- [ ] Garantir que todos os testes passam
- [ ] Verificar se não há testes duplicados ou redundantes

### 12. Documentação
- [ ] Atualizar `docs/testes.md` com exemplos dos novos testes
- [ ] Documentar padrões de teste para cada tipo de componente
- [ ] Criar guia de boas práticas de testes

---

## 📊 Critérios de Sucesso

- ✅ Cobertura de testes acima de 80% para componentes críticos
- ✅ Todos os componentes UI principais têm testes
- ✅ Todos os hooks customizados têm testes
- ✅ Todos os utilitários críticos têm testes
- ✅ Testes seguem padrões consistentes
- ✅ Todos os testes passam

---

## ⏱️ Estimativa
**Tempo estimado:** 8-12 horas (dependendo da quantidade de componentes)

## 🔗 Dependências
- **Fase 1** deve estar completa (organização dos testes)

## 📝 Notas
- Priorizar componentes mais utilizados e críticos primeiro
- Usar TDD (Test-Driven Development) quando possível
- Manter testes simples e focados em uma responsabilidade
- Considerar usar `@testing-library/user-event` para interações mais realistas

## 🎯 Meta de Cobertura
- **Componentes UI:** 90%+
- **Hooks:** 85%+
- **Utilitários:** 80%+
- **Componentes de Features:** 75%+
- **Componentes de Dashboards:** 70%+
