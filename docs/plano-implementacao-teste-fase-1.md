# 📋 Fase 1: Organização dos Testes Unitários

## Objetivo
Reorganizar os testes unitários existentes em uma estrutura padronizada e centralizada na pasta `tests/unit/`, facilitando a manutenção e execução.

## Contexto
Atualmente, os testes unitários estão espalhados junto aos componentes em pastas `__tests__/`. Esta fase visa centralizar todos os testes em `tests/unit/` mantendo a mesma estrutura de pastas do `src/`.

---

## ✅ Checklist de Ações

### 1. Preparação da Estrutura
- [x] Criar estrutura de pastas em `tests/unit/` espelhando `src/`:
  - [x] `tests/unit/components/ui/`
  - [x] `tests/unit/components/features/`
  - [x] `tests/unit/components/dashboards/`
  - [x] `tests/unit/components/charts/`
  - [x] `tests/unit/components/layouts/`
  - [x] `tests/unit/lib/hooks/`
  - [x] `tests/unit/lib/utils/`
  - [x] `tests/unit/lib/api/`
  - [x] `tests/unit/store/`

### 2. Migração dos Testes Existentes
- [x] Mover testes de componentes UI:
  - [x] `src/components/ui/__tests__/button.test.tsx` → `tests/unit/components/ui/button.test.tsx`
  - [x] `src/components/ui/__tests__/card.test.tsx` → `tests/unit/components/ui/card.test.tsx`
  - [x] `src/components/ui/__tests__/input.test.tsx` → `tests/unit/components/ui/input.test.tsx`
  - [x] `src/components/ui/__tests__/dialog.test.tsx` → `tests/unit/components/ui/dialog.test.tsx`
  - [x] `src/components/ui/__tests__/dropdown-menu.test.tsx` → `tests/unit/components/ui/dropdown-menu.test.tsx`
  - [x] `src/components/ui/__tests__/spinner.test.tsx` → `tests/unit/components/ui/spinner.test.tsx`
  - [x] `src/components/ui/__tests__/data-table.test.tsx` → `tests/unit/components/ui/data-table.test.tsx`

- [x] Mover testes de features:
  - [x] `src/components/features/__tests__/global-search.test.tsx` → `tests/unit/components/features/global-search.test.tsx`
  - [x] `src/components/features/__tests__/export-button.test.tsx` → `tests/unit/components/features/export-button.test.tsx`
  - [x] `src/components/features/__tests__/alerts-panel.test.tsx` → `tests/unit/components/features/alerts-panel.test.tsx`

- [x] Mover testes de dashboards:
  - [x] `src/components/dashboards/__tests__/kpi-card.test.tsx` → `tests/unit/components/dashboards/kpi-card.test.tsx`

- [x] Mover testes de hooks:
  - [x] `src/lib/hooks/__tests__/useFavorites.test.ts` → `tests/unit/lib/hooks/useFavorites.test.ts`
  - [x] `src/lib/hooks/__tests__/useDebounce.test.ts` → `tests/unit/lib/hooks/useDebounce.test.ts`
  - [x] `src/lib/hooks/__tests__/useComparison.test.ts` → `tests/unit/lib/hooks/useComparison.test.ts`

- [x] Mover outros testes:
  - [x] `src/components/__tests__/error-boundary.test.tsx` → `tests/unit/components/error-boundary.test.tsx`

### 3. Atualização de Imports
- [x] Atualizar todos os imports nos testes movidos para usar paths relativos corretos
- [x] Verificar se os imports de `@/` ainda funcionam ou ajustar conforme necessário
- [x] Atualizar imports de helpers de teste (`test-utils.tsx`)

### 4. Atualização da Configuração Jest
- [x] Atualizar `jest.config.js` para incluir `tests/unit/` no padrão de busca
- [x] Configurar `testMatch` para incluir `tests/unit/**/*.test.{ts,tsx}`
- [x] Verificar se `moduleNameMapper` está correto para os novos caminhos
- [x] Atualizar `collectCoverageFrom` se necessário

### 5. Criação de Helpers de Teste
- [x] Mover ou criar `tests/helpers/test-utils.tsx` se ainda não existir
- [x] Garantir que os helpers estejam acessíveis para todos os testes
- [x] Criar mocks compartilhados em `tests/helpers/mocks/` se necessário

### 6. Validação e Testes
- [x] Executar `npm test` para garantir que todos os testes ainda passam
- [x] Verificar se a cobertura de testes não diminuiu
- [x] Executar `npm test -- --coverage` e documentar a cobertura atual
- [x] Verificar se não há testes duplicados ou órfãos

### 7. Limpeza
- [x] Remover pastas `__tests__/` vazias dos componentes
- [x] Atualizar `.gitignore` se necessário
- [x] Verificar se não há referências quebradas em outros arquivos

### 8. Documentação
- [x] Atualizar `README.md` com a nova estrutura de testes
- [x] Criar ou atualizar `docs/testes.md` com guia de como escrever testes
- [x] Documentar a convenção de nomenclatura e estrutura

---

## 📊 Critérios de Sucesso

- ✅ Todos os testes unitários existentes foram movidos para `tests/unit/`
- ✅ Todos os testes continuam passando após a migração
- ✅ A estrutura de pastas em `tests/unit/` espelha `src/`
- ✅ Configuração do Jest está atualizada e funcionando
- ✅ Cobertura de testes mantida ou melhorada
- ✅ Documentação atualizada

---

## ⏱️ Estimativa
**Tempo estimado:** 2-3 horas

## 🔗 Dependências
- Nenhuma (pode ser executada imediatamente)

## 📝 Notas
- Manter a mesma estrutura de pastas facilita a localização de testes
- Considerar criar um script de migração se houver muitos arquivos
- Fazer commits incrementais durante a migração para facilitar rollback se necessário
