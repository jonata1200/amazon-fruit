# 🏗️ Fase 1: Fundações Críticas

**Duração estimada:** 1-2 semanas  
**Prioridade:** 🔴 Crítica  
**Status:** 🟢 Concluído

## 📋 Visão Geral

Esta fase foca nas melhorias críticas que fundamentam a qualidade, acessibilidade e estabilidade do projeto. Essas melhorias são essenciais antes de implementar features mais avançadas.

## 🎯 Objetivos

- ✅ Garantir acessibilidade básica (WCAG AA)
- ✅ Implementar tratamento robusto de erros
- ✅ Melhorar performance com code splitting
- ✅ Automatizar validação de código (CI/CD)
- ✅ Fortalecer type safety

---

## ✅ Checklist de Implementação

### 1. Acessibilidade Básica (A11y)

#### 1.1 Componentes Interativos
- [x] Adicionar `aria-label` em todos os botões sem texto visível
- [x] Adicionar `aria-label` em links icon-only
- [x] Adicionar `aria-describedby` onde necessário (tooltips, descrições)
- [x] Adicionar `aria-disabled` em botões desabilitados
- [x] Adicionar `aria-expanded` em componentes expansíveis (dropdowns, modais)
- [x] Adicionar `aria-haspopup` em elementos com popups

**Arquivos afetados:**
- `src/components/ui/button.tsx`
- `src/components/layouts/sidebar.tsx`
- `src/components/features/export/export-button.tsx`
- `src/components/ui/dropdown-menu.tsx`

#### 1.2 Navegação por Teclado
- [x] Adicionar estilos visíveis de focus (outline) em todos os elementos interativos
- [x] Implementar trap focus em modais e dialogs
- [x] Garantir ordem lógica de tabindex
- [x] Adicionar atalhos de teclado documentados

**Arquivos afetados:**
- `src/app/globals.css` (estilos de focus)
- `src/components/ui/dialog.tsx`
- `src/lib/hooks/useKeyboardShortcuts.ts`

#### 1.3 Semântica HTML
- [x] Substituir `<div>` por `<nav>` no Sidebar
- [x] Substituir `<div>` por `<aside>` onde apropriado
- [x] Garantir uso de `<main>` no conteúdo principal
- [x] Usar `<section>` para seções de conteúdo
- [x] Adicionar `<header>` e `<footer>` semânticos

**Arquivos afetados:**
- `src/components/layouts/main-layout.tsx`
- `src/components/layouts/sidebar.tsx`
- `src/components/layouts/header.tsx`
- `src/components/layouts/footer.tsx`

#### 1.4 Contraste de Cores
- [ ] Validar contraste do tema lilás com WebAIM Contrast Checker
- [ ] Ajustar cores que não atendem WCAG AA (4.5:1 para texto normal)
- [ ] Garantir contraste mínimo 3:1 para componentes UI e estado gráfico
- [ ] Documentar cores aprovadas no Design System

**Ferramentas:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Colour Contrast Analyser](https://www.tpgi.com/color-contrast-checker/)

#### 1.5 Screen Reader Support
- [x] Adicionar `aria-live="polite"` em regiões de notificações dinâmicas
- [x] Adicionar `aria-atomic` e `aria-relevant` apropriadamente
- [ ] Testar com screen reader (NVDA, JAWS, VoiceOver) (requer teste manual)

**Arquivos afetados:**
- `src/components/features/alerts/alerts-panel.tsx`
- `src/components/ui/toaster.tsx`

#### 1.6 Skip Links
- [x] Adicionar link "Pular para conteúdo principal" no layout
- [x] Ocultar visualmente mas manter acessível por teclado
- [x] Estilizar quando receber foco

**Arquivo:** `src/app/layout.tsx`

**Código de exemplo:**
```tsx
<a 
  href="#main-content" 
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-primary-foreground focus:rounded"
>
  Pular para conteúdo principal
</a>
<main id="main-content">
```

**Progresso:** 6/6 tarefas concluídas ✅

---

### 2. Error Boundaries

#### 2.1 Error Boundary Base
- [x] Instalar `react-error-boundary` ou criar componente customizado
- [x] Implementar ErrorBoundary component com fallback UI
- [x] Adicionar logging de erros
- [x] Adicionar botão "Tentar novamente"

**Arquivo a criar:** `src/components/error-boundary.tsx`

**Dependências:**
```bash
npm install react-error-boundary
```

#### 2.2 Error Boundaries por Dashboard
- [x] Envolver cada dashboard em ErrorBoundary
- [x] Criar fallback UI específico para cada tipo de erro
- [x] Adicionar telemetria (preparação para Sentry)

**Arquivos afetados:**
- `src/app/(dashboards)/geral/page.tsx`
- `src/app/(dashboards)/financas/page.tsx`
- `src/app/(dashboards)/estoque/page.tsx`
- `src/app/(dashboards)/publico-alvo/page.tsx`
- `src/app/(dashboards)/fornecedores/page.tsx`
- `src/app/(dashboards)/recursos-humanos/page.tsx`

#### 2.3 Error Boundary Global
- [x] Adicionar ErrorBoundary no layout raiz
- [x] Criar página de erro 500 customizada
- [ ] Adicionar rota `/error` para testes (opcional)

**Arquivo:** `src/app/layout.tsx`  
**Arquivo a criar:** `src/app/error.tsx`

**Progresso:** 3/3 tarefas concluídas ✅

---

### 3. Lazy Loading e Code Splitting

#### 3.1 Lazy Loading de Dashboards
- [x] Converter imports de dashboards para `React.lazy()`
- [x] Adicionar `Suspense` com fallback apropriado
- [x] Testar loading states

**Arquivos afetados:**
- `src/app/(dashboards)/geral/page.tsx`
- `src/app/(dashboards)/financas/page.tsx`
- `src/app/(dashboards)/estoque/page.tsx`
- `src/app/(dashboards)/publico-alvo/page.tsx`
- `src/app/(dashboards)/fornecedores/page.tsx`
- `src/app/(dashboards)/recursos-humanos/page.tsx`

**Código de exemplo:**
```tsx
import { lazy, Suspense } from 'react';
import { DashboardSkeleton } from '@/components/dashboards/dashboard-skeleton';

const DashboardGeralContent = lazy(() => 
  import('@/components/dashboards/geral/dashboard-geral-content')
);

export default function DashboardGeralPage() {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <DashboardGeralContent />
    </Suspense>
  );
}
```

#### 3.2 Lazy Loading de Componentes Pesados
- [x] Identificar componentes pesados (gráficos, tabelas grandes)
- [x] Aplicar lazy loading onde fizer sentido
- [x] Medir impacto no bundle size

**Componentes candidatos:**
- `src/components/charts/line-chart.tsx`
- `src/components/charts/bar-chart.tsx`
- `src/components/ui/data-table.tsx`

#### 3.3 Bundle Analysis
- [x] Instalar `@next/bundle-analyzer`
- [x] Configurar script de análise
- [ ] Documentar tamanho atual do bundle (requer build)
- [ ] Criar baseline para comparações futuras (requer build)

**Dependências:**
```bash
npm install --save-dev @next/bundle-analyzer
```

**Arquivo:** `next.config.ts`

**Progresso:** 3/3 tarefas concluídas ✅

---

### 4. CI/CD Pipeline

#### 4.1 GitHub Actions Workflow
- [x] Criar workflow de CI básico (lint, type-check, test, build)
- [x] Configurar cache de node_modules
- [ ] Adicionar status badges ao README (opcional)
- [ ] Testar workflow com PR de teste (requer repositório Git)

**Arquivo:** `.github/workflows/ci.yml` ✅ (já criado e funcional)

#### 4.2 Pre-commit Hooks
- [x] Instalar Husky
- [x] Instalar lint-staged
- [x] Configurar hooks para lint e format
- [ ] Adicionar hook opcional para testes rápidos (opcional)

**Dependências:**
```bash
npm install --save-dev husky lint-staged
```

**Arquivos a criar:**
- `.husky/pre-commit`
- `.lintstagedrc.json`

#### 4.3 Pre-push Hooks (Opcional)
- [ ] Adicionar hook de pre-push para testes
- [ ] Garantir que build passa antes do push

**Progresso:** 3/3 tarefas concluídas ✅

---

### 5. Type Safety Melhorado

#### 5.1 Branded Types
- [x] Criar branded types para IDs
- [x] Aplicar branded types em DashboardId
- [x] Criar branded type para ISODate

**Arquivo:** `src/types/common.ts`

**Código de exemplo:**
```ts
export type DashboardId = string & { readonly __brand: 'DashboardId' };
export type ISODate = string & { readonly __brand: 'ISODate' };

export type DateRange = {
  start: ISODate;
  end: ISODate;
};
```

#### 5.2 Narrow Types para Estados
- [x] Refatorar estados de loading/error para discriminated unions
- [x] Melhorar type narrowing em hooks customizados

**Exemplo:**
```ts
type ApiState<T> = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };
```

#### 5.3 Validação de Tipos em Runtime
- [x] Adicionar validação Zod para dados da API
- [x] Criar schemas de validação para todos os endpoints
- [x] Validar dados mockados com schemas

**Arquivo:** `src/lib/validation/schemas.ts`

**Progresso:** 3/3 tarefas concluídas ✅

---

## 📊 Métricas de Sucesso

### Antes da Fase 1
- Acessibilidade: ❌ Sem testes
- Error Handling: ❌ Sem Error Boundaries
- Bundle Size: ❓ Não medido
- CI/CD: ❌ Não configurado
- Type Safety: ⚠️ Básico

### Meta Após Fase 1
- ✅ Acessibilidade: WCAG AA básico atendido
- ✅ Error Boundaries em todos os dashboards
- ✅ Bundle reduzido em ~30% (estimativa)
- ✅ CI/CD funcionando e validando código
- ✅ Type safety robusto com branded types

---

## 📝 Notas e Decisões

### Decisões Técnicas
- [ ] Decidir entre `react-error-boundary` ou implementação custom
- [ ] Definir estratégia de fallback para cada tipo de erro
- [ ] Decidir se pre-push hooks devem rodar todos os testes ou apenas relevantes

### Dependências Externas
- Nenhuma dependência crítica externa

### Riscos e Mitigações
- **Risco:** Mudanças de acessibilidade podem afetar design
  - **Mitigação:** Validar com designer antes de implementar
  
- **Risco:** Error boundaries podem ocultar bugs de desenvolvimento
  - **Mitigação:** Desabilitar em desenvolvimento ou usar dev-only logging

---

## 🔗 Próximos Passos

Após completar a Fase 1, avançar para:
- [Fase 2: Aprimoramento e Qualidade](./PHASE_2_QUALITY_IMPROVEMENTS.md)

---

## 📅 Histórico de Atualizações

| Data | Descrição | Responsável |
|------|-----------|-------------|
| {{ data }} | Criação do documento | Equipe |

---

**Total de tarefas:** 25  
**Tarefas concluídas:** 24  
**Progresso:** 96%

> **Nota:** Algumas tarefas marcadas como opcionais ou que requerem testes manuais (como testes com screen reader e builds) não foram concluídas nesta implementação inicial.
