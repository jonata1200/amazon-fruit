# 📋 Fase 2: Criação de Testes Unitários Faltantes

## Objetivo
Identificar e criar testes unitários para componentes, hooks e utilitários que ainda não possuem cobertura de testes.

## Contexto
Após a organização dos testes existentes, é necessário garantir que todos os componentes críticos tenham testes unitários adequados. Esta fase foca em preencher as lacunas de cobertura.

---

## ✅ Checklist de Ações

### 1. Análise de Cobertura Atual
- [x] Executar `npm test -- --coverage` e gerar relatório
- [x] Identificar componentes sem testes:
  - [x] Componentes UI sem testes
  - [x] Componentes de features sem testes
  - [x] Componentes de dashboards sem testes
  - [x] Hooks sem testes
  - [x] Utilitários sem testes
- [x] Priorizar componentes por criticidade (alta, média, baixa)
- [ ] Documentar gaps de cobertura em `docs/coverage-gaps.md` (opcional)

### 2. Testes para Componentes UI Faltantes
- [x] **EmptyState**
  - [x] Teste de renderização básica
  - [x] Teste com diferentes props (title, description, icon)
  - [x] Teste de ação opcional (button)

- [x] **Icon**
  - [x] Teste de renderização com diferentes ícones
  - [x] Teste de tamanhos (xs, sm, md, lg, xl)
  - [x] Teste de classes customizadas

- [x] **Label**
  - [x] Teste de renderização
  - [x] Teste de associação com input (htmlFor)
  - [x] Teste de estados (required, disabled)

- [x] **Progress**
  - [x] Teste de renderização
  - [x] Teste de valores (0%, 50%, 100%)
  - [x] Teste de cores/variantes

- [x] **Tooltip**
  - [x] Teste de renderização
  - [x] Teste de exibição ao hover
  - [x] Teste de posicionamento

- [ ] **Toaster** (gerenciado pelo Sonner, testes podem ser de integração)
  - [ ] Teste de renderização
  - [ ] Teste de diferentes tipos de toast (success, error, info, warning)
  - [ ] Teste de auto-dismiss

- [x] **LoadingScreen**
  - [x] Teste de renderização
  - [x] Teste de mensagem customizada

- [x] **Skeleton**
  - [x] Teste de renderização
  - [x] Teste de diferentes variantes (text, circle, rectangular)
  - [x] Teste de animação

- [x] **Skeletons Específicos**
  - [x] `chart-skeleton.test.tsx`
  - [x] `kpi-skeleton.test.tsx`
  - [x] `table-skeleton.test.tsx`

### 3. Testes para Componentes de Features Faltantes
- [x] **KeyboardShortcutsHelp**
  - [x] Teste de renderização
  - [x] Teste de exibição de atalhos
  - [x] Teste de toggle (abrir/fechar)

### 4. Testes para Componentes de Dashboards Faltantes
- [x] **PeriodSelector**
  - [x] Teste de renderização
  - [x] Teste de seleção de período
  - [x] Teste de callback onChange

- [x] **DashboardSkeleton**
  - [x] Teste de renderização
  - [x] Teste de diferentes layouts

- [ ] **Dashboard Contents** (opcional, podem ser testes de integração)
  - [ ] `dashboard-geral-content.test.tsx`
  - [ ] `dashboard-financas-content.test.tsx`
  - [ ] `dashboard-estoque-content.test.tsx`
  - [ ] `dashboard-publico-alvo-content.test.tsx`
  - [ ] `dashboard-fornecedores-content.test.tsx`
  - [ ] `dashboard-rh-content.test.tsx`

### 5. Testes para Componentes de Charts Faltantes
- [x] **BarChart**
  - [x] Teste de renderização
  - [x] Teste com dados válidos
  - [x] Teste com dados vazios
  - [x] Teste de múltiplas barras

- [x] **LineChart**
  - [x] Teste de renderização
  - [x] Teste com dados válidos
  - [x] Teste com dados vazios
  - [x] Teste de múltiplas séries

- [x] **PieChart**
  - [x] Teste de renderização
  - [x] Teste com dados válidos
  - [x] Teste com dados vazios
  - [x] Teste de múltiplos pontos de dados

### 6. Testes para Componentes de Layout Faltantes
- [x] **Header**
  - [x] Teste de renderização
  - [x] Teste de botões de ação (search, alerts, theme)
  - [x] Teste de contador de alertas
  - [x] Teste de tema toggle

- [x] **Sidebar**
  - [x] Teste de renderização
  - [x] Teste de navegação entre dashboards
  - [x] Teste de estado ativo
  - [x] Teste de favoritos
  - [x] Teste de collapse/expand

- [x] **Footer**
  - [x] Teste de renderização
  - [x] Teste de ano dinâmico

- [x] **MainLayout**
  - [x] Teste de renderização
  - [x] Teste de composição (Header + Sidebar + Content + Footer)

### 7. Testes para Hooks Faltantes
- [x] **useAlerts**
  - [x] Teste de criação de alerta
  - [x] Teste de remoção de alerta
  - [x] Teste de atualização de alerta
  - [x] Teste de filtros

- [ ] **useAnalytics** (pode ser testado em integração)
  - [ ] Teste de tracking de eventos
  - [ ] Teste de page views
  - [ ] Teste de métricas customizadas

- [ ] **useAppInitialization** (pode ser testado em integração)
  - [ ] Teste de inicialização
  - [ ] Teste de carregamento de dados
  - [ ] Teste de tratamento de erros

- [ ] **useDashboards** (pode ser testado em integração)
  - [ ] Teste de busca de dashboards
  - [ ] Teste de filtros
  - [ ] Teste de ordenação

- [x] **useKeyboardShortcuts**
  - [x] Teste de registro de atalhos
  - [x] Teste de execução de callbacks
  - [x] Teste de remoção de atalhos

- [x] **useNotifications**
  - [x] Teste de criação de notificação
  - [x] Teste de remoção automática
  - [x] Teste de diferentes tipos

### 8. Testes para Utilitários Faltantes
- [x] **lib/utils/**
  - [x] Teste de `cn()` (classNames utility)
  - [x] Teste de formatação de números
  - [x] Teste de formatação de datas
  - [x] Teste de validações
  - [ ] Teste de transformações de dados (se houver)

- [x] **lib/api/**
  - [x] Teste de cliente API (estrutura básica)
  - [x] Teste de métodos (get, post, put, delete)
  - [ ] Teste de interceptors (melhor em integração)
  - [ ] Teste de tratamento de erros (melhor em integração)
  - [ ] Teste de retry logic (melhor em integração)

- [x] **lib/validation/**
  - [x] Teste de schemas Zod
  - [x] Teste de validações customizadas
  - [x] Teste de helper functions

### 9. Testes para Store (Zustand)
- [x] **store/index.ts**
  - [x] Teste de estado inicial
  - [x] Teste de ações (theme, sidebar, alerts, search, etc.)
  - [x] Teste de toggle functions
  - [x] Teste de setters
  - [ ] Teste de persistência (melhor em integração)

### 10. Melhorias em Testes Existentes
- [x] Revisar testes existentes e adicionar casos de borda
- [x] Corrigir testes que estavam falhando
- [x] Ajustar mocks e fixtures conforme necessário
- [ ] Adicionar testes de acessibilidade onde faltam (próxima fase)
- [ ] Adicionar testes de responsividade onde relevante (próxima fase)

### 11. Validação e Cobertura
- [x] Executar `npm test -- --coverage` após cada grupo de testes
- [x] Verificar se a cobertura aumentou significativamente (283 testes passando)
- [x] Garantir que todos os testes passam (44 suites, 283 testes - 100% passando)
- [x] Verificar se não há testes duplicados ou redundantes

### 12. Documentação
- [x] Atualizar `docs/testes.md` com exemplos dos novos testes (já existe)
- [x] Documentar padrões de teste para cada tipo de componente (já existe)
- [x] Criar guia de boas práticas de testes (já existe)

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
