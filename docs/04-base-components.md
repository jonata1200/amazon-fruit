# 🧩 Fase 4: Componentes Base do Design System

## 📋 Objetivo

Padronizar e melhorar os componentes UI existentes, garantindo consistência, acessibilidade e uso eficiente dos design tokens.

## ✅ Checklist

### 1. Auditoria de Componentes Existentes
- [ ] Listar todos os componentes em `src/components/ui/`
- [ ] Analisar cada componente atual
- [ ] Identificar inconsistências
- [ ] Mapear uso de design tokens
- [ ] Identificar padrões comuns
- [ ] Documentar problemas encontrados

### 2. Padronização de Estrutura
- [ ] Definir estrutura padrão de componentes
- [ ] Criar template/base para novos componentes
- [ ] Padronizar props interface
- [ ] Padronizar uso de forwardRef
- [ ] Padronizar uso de className e cn()
- [ ] Padronizar variantes (usar cva ou similar)

### 3. Sistema de Variantes
- [ ] Escolher biblioteca para variantes (class-variance-authority já existe)
- [ ] Padronizar uso de variantes em todos os componentes
- [ ] Criar helpers para variantes comuns
- [ ] Garantir type-safety nas variantes
- [ ] Documentar padrão de variantes

### 4. Componente Button
- [ ] Revisar componente Button atual
- [ ] Padronizar variantes (size, variant, color)
- [ ] Integrar com design tokens
- [ ] Adicionar estados (loading, disabled)
- [ ] Melhorar acessibilidade (ARIA)
- [ ] Adicionar suporte a ícones
- [ ] Garantir contraste adequado
- [ ] Testar em dark mode

### 5. Componente Input
- [ ] Revisar componente Input atual
- [ ] Padronizar variantes (size, variant, state)
- [ ] Integrar com design tokens
- [ ] Adicionar estados (error, success, disabled)
- [ ] Melhorar acessibilidade
- [ ] Adicionar suporte a ícones (prefix/suffix)
- [ ] Adicionar suporte a labels e hints
- [ ] Garantir contraste adequado

### 6. Componente Card
- [ ] Revisar componente Card atual
- [ ] Padronizar variantes (elevation, padding)
- [ ] Integrar com design tokens
- [ ] Adicionar variantes (outlined, filled, elevated)
- [ ] Melhorar acessibilidade
- [ ] Adicionar suporte a header/footer
- [ ] Garantir contraste adequado

### 7. Componente Dialog/Modal
- [ ] Revisar componente Dialog atual
- [ ] Padronizar tamanhos e variantes
- [ ] Integrar com design tokens
- [ ] Melhorar acessibilidade (focus trap, ARIA)
- [ ] Adicionar animações consistentes
- [ ] Garantir z-index correto
- [ ] Adicionar suporte a diferentes tamanhos

### 8. Componente Dropdown Menu
- [ ] Revisar componente Dropdown Menu atual
- [ ] Padronizar estilos
- [ ] Integrar com design tokens
- [ ] Melhorar acessibilidade (keyboard navigation)
- [ ] Adicionar animações
- [ ] Garantir posicionamento correto

### 9. Componente Data Table
- [ ] Revisar componente Data Table atual
- [ ] Padronizar estilos
- [ ] Integrar com design tokens
- [ ] Melhorar acessibilidade
- [ ] Adicionar variantes (striped, bordered)
- [ ] Garantir responsividade
- [ ] Adicionar estados (loading, empty)

### 10. Componentes de Feedback
- [ ] Revisar componentes: Skeleton, Spinner, Progress
- [ ] Padronizar estilos e animações
- [ ] Integrar com design tokens
- [ ] Garantir acessibilidade (aria-live)
- [ ] Criar variantes consistentes
- [ ] Adicionar suporte a tamanhos

### 11. Componente Tooltip
- [ ] Revisar componente Tooltip atual
- [ ] Padronizar estilos
- [ ] Integrar com design tokens
- [ ] Melhorar acessibilidade
- [ ] Adicionar animações
- [ ] Garantir posicionamento correto
- [ ] Adicionar variantes (dark, light)

### 12. Componente Empty State
- [ ] Revisar componente Empty State atual
- [ ] Padronizar estilos
- [ ] Integrar com design tokens
- [ ] Adicionar variantes
- [ ] Melhorar acessibilidade
- [ ] Adicionar suporte a ações

### 13. Sistema de Espaçamento em Componentes
- [ ] Padronizar padding interno dos componentes
- [ ] Padronizar gaps entre elementos
- [ ] Usar design tokens de spacing
- [ ] Criar variantes de tamanho consistentes
- [ ] Documentar sistema de espaçamento

### 14. Sistema de Cores em Componentes
- [ ] Padronizar uso de cores semânticas
- [ ] Garantir contraste adequado
- [ ] Usar design tokens de cores
- [ ] Criar variantes de cor consistentes
- [ ] Testar em modo claro e escuro

### 15. Acessibilidade
- [ ] Adicionar ARIA labels onde necessário
- [ ] Garantir navegação por teclado
- [ ] Garantir contraste de cores (WCAG)
- [ ] Testar com leitores de tela
- [ ] Adicionar focus states visíveis
- [ ] Garantir que componentes são semânticos

### 16. Dark Mode
- [ ] Garantir que todos os componentes funcionam em dark mode
- [ ] Testar contraste em ambos os modos
- [ ] Ajustar cores quando necessário
- [ ] Garantir transições suaves

### 17. Animações e Transições
- [ ] Padronizar animações entre componentes
- [ ] Usar design tokens de transição
- [ ] Adicionar animações sutis e consistentes
- [ ] Respeitar prefers-reduced-motion
- [ ] Garantir performance das animações

### 18. Documentação de Componentes
- [ ] Documentar cada componente
- [ ] Criar exemplos de uso
- [ ] Documentar props e variantes
- [ ] Criar guia de quando usar cada componente
- [ ] Documentar acessibilidade
- [ ] Criar playground/exemplos interativos

### 19. Testes
- [ ] Criar testes para cada componente
- [ ] Testar variantes
- [ ] Testar acessibilidade
- [ ] Testar dark mode
- [ ] Testar responsividade
- [ ] Testar interações (hover, focus, etc.)

### 20. Refatoração e Migração
- [ ] Refatorar componentes para usar design tokens
- [ ] Atualizar componentes existentes
- [ ] Remover código duplicado
- [ ] Consolidar padrões
- [ ] Garantir compatibilidade

## 📁 Arquivos a Modificar/Criar

- [ ] `src/components/ui/button.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/input.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/card.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/dialog.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/dropdown-menu.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/data-table.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/skeleton.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/spinner.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/progress.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/tooltip.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/empty-state.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/index.ts` - Exports centralizados
- [ ] `src/lib/utils/variants.ts` - Helpers para variantes
- [ ] `docs/components/` - Documentação de componentes

## 🎯 Critérios de Sucesso

- ✅ Todos os componentes padronizados e consistentes
- ✅ Uso consistente de design tokens
- ✅ Acessibilidade garantida (WCAG)
- ✅ Dark mode funcionando em todos os componentes
- ✅ Type-safety garantido
- ✅ Documentação completa
- ✅ Testes cobrindo casos principais

## 📝 Notas

- Manter compatibilidade com código existente
- Priorizar acessibilidade
- Testar cada componente individualmente
- Documentar decisões de design
- Usar class-variance-authority para variantes

---

**Próximo passo:** [Fase 5: Utilitários e Helpers](./05-utilities-helpers.md)
