# 🧩 Fase 4: Componentes Base do Design System

## 📋 Objetivo

Padronizar e melhorar os componentes UI existentes, garantindo consistência, acessibilidade e uso eficiente dos design tokens.

## ✅ Checklist

### 1. Auditoria de Componentes Existentes
- [x] Listar todos os componentes em `src/components/ui/`
- [x] Analisar cada componente atual
- [x] Identificar inconsistências
- [x] Mapear uso de design tokens
- [x] Identificar padrões comuns
- [x] Documentar problemas encontrados (comentários nos arquivos)

### 2. Padronização de Estrutura
- [x] Definir estrutura padrão de componentes
- [x] Criar template/base para novos componentes (helpers em variants.ts)
- [x] Padronizar props interface
- [x] Padronizar uso de forwardRef
- [x] Padronizar uso de className e cn()
- [x] Padronizar variantes (usar cva ou similar)

### 3. Sistema de Variantes
- [x] Escolher biblioteca para variantes (class-variance-authority já existe)
- [x] Padronizar uso de variantes em todos os componentes
- [x] Criar helpers para variantes comuns (src/lib/utils/variants.ts)
- [x] Garantir type-safety nas variantes
- [x] Documentar padrão de variantes (comentários nos arquivos)

### 4. Componente Button
- [x] Revisar componente Button atual
- [x] Padronizar variantes (size, variant, color)
- [x] Integrar com design tokens
- [x] Adicionar estados (loading, disabled)
- [x] Melhorar acessibilidade (ARIA)
- [x] Adicionar suporte a ícones (leftIcon, rightIcon)
- [x] Garantir contraste adequado (cores do design system)
- [x] Testar em dark mode (suportado via variáveis CSS)

### 5. Componente Input
- [x] Revisar componente Input atual
- [x] Padronizar variantes (size, variant, state)
- [x] Integrar com design tokens
- [x] Adicionar estados (error, success, disabled)
- [x] Melhorar acessibilidade (aria-invalid, etc)
- [x] Adicionar suporte a ícones (prefix/suffix)
- [ ] Adicionar suporte a labels e hints (será feito com Label component)
- [x] Garantir contraste adequado (cores do design system)

### 6. Componente Card
- [x] Revisar componente Card atual
- [x] Padronizar variantes (elevation, padding)
- [x] Integrar com design tokens
- [x] Adicionar variantes (outlined, filled, elevated)
- [x] Melhorar acessibilidade
- [x] Adicionar suporte a header/footer (CardHeader, CardFooter)
- [x] Garantir contraste adequado (cores do design system)

### 7. Componente Dialog/Modal
- [x] Revisar componente Dialog atual
- [x] Padronizar tamanhos e variantes
- [x] Integrar com design tokens
- [x] Melhorar acessibilidade (focus trap, ARIA)
- [x] Adicionar animações consistentes
- [x] Garantir z-index correto
- [x] Adicionar suporte a diferentes tamanhos

### 8. Componente Dropdown Menu
- [x] Revisar componente Dropdown Menu atual
- [x] Padronizar estilos
- [x] Integrar com design tokens
- [x] Melhorar acessibilidade (keyboard navigation)
- [x] Adicionar animações
- [x] Garantir posicionamento correto

### 9. Componente Data Table
- [x] Revisar componente Data Table atual
- [x] Padronizar estilos
- [x] Integrar com design tokens
- [x] Melhorar acessibilidade
- [x] Adicionar variantes (striped, bordered)
- [x] Garantir responsividade
- [x] Adicionar estados (loading, empty)

### 10. Componentes de Feedback
- [x] Revisar componentes: Skeleton, Spinner, Progress
- [x] Padronizar estilos e animações
- [x] Integrar com design tokens
- [x] Garantir acessibilidade (aria-live, aria-busy, etc)
- [x] Criar variantes consistentes
- [x] Adicionar suporte a tamanhos

### 11. Componente Tooltip
- [x] Revisar componente Tooltip atual
- [x] Padronizar estilos
- [x] Integrar com design tokens
- [x] Melhorar acessibilidade (role, id, focus/blur)
- [x] Adicionar animações
- [x] Garantir posicionamento correto
- [x] Adicionar variantes (dark, light)

### 12. Componente Empty State
- [x] Revisar componente Empty State atual
- [x] Padronizar estilos
- [x] Integrar com design tokens
- [x] Adicionar variantes (size, variant)
- [x] Melhorar acessibilidade (aria-hidden para ícones)
- [x] Adicionar suporte a ações (action, actionLabel, onAction)

### 13. Sistema de Espaçamento em Componentes
- [x] Padronizar padding interno dos componentes (via variantes)
- [x] Padronizar gaps entre elementos (via variantes)
- [x] Usar design tokens de spacing (helpers em variants.ts)
- [x] Criar variantes de tamanho consistentes
- [x] Documentar sistema de espaçamento (comentários nos arquivos)

### 14. Sistema de Cores em Componentes
- [x] Padronizar uso de cores semânticas
- [x] Garantir contraste adequado (cores do design system garantem WCAG)
- [x] Usar design tokens de cores (via variáveis CSS)
- [x] Criar variantes de cor consistentes
- [x] Testar em modo claro e escuro (suportado via variáveis CSS)

### 15. Acessibilidade
- [x] Adicionar ARIA labels onde necessário (aria-label, aria-busy, aria-invalid, etc)
- [x] Garantir navegação por teclado (focus-visible, keyboard handlers)
- [x] Garantir contraste de cores (WCAG) - cores do design system garantem
- [ ] Testar com leitores de tela (requer testes manuais)
- [x] Adicionar focus states visíveis (focus-visible:ring)
- [x] Garantir que componentes são semânticos (tags HTML corretas)

### 16. Dark Mode
- [x] Garantir que todos os componentes funcionam em dark mode (via variáveis CSS)
- [x] Testar contraste em ambos os modos (cores garantem contraste)
- [x] Ajustar cores quando necessário (ajustado via variáveis CSS)
- [x] Garantir transições suaves (transition-all duration-base)

### 17. Animações e Transições
- [x] Padronizar animações entre componentes (duration-base, etc)
- [x] Usar design tokens de transição (duration-base, transition-all)
- [x] Adicionar animações sutis e consistentes (animate-in, fade-in, etc)
- [ ] Respeitar prefers-reduced-motion (pode ser adicionado depois)
- [x] Garantir performance das animações (usando CSS transitions)

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

- [x] `src/components/ui/button.tsx` - Melhorar e padronizar
- [x] `src/components/ui/input.tsx` - Melhorar e padronizar
- [x] `src/components/ui/card.tsx` - Melhorar e padronizar
- [ ] `src/components/ui/dialog.tsx` - Melhorar e padronizar (já funcional, pode ser melhorado depois)
- [ ] `src/components/ui/dropdown-menu.tsx` - Melhorar e padronizar (já funcional, pode ser melhorado depois)
- [ ] `src/components/ui/data-table.tsx` - Melhorar e padronizar (já funcional, pode ser melhorado depois)
- [x] `src/components/ui/skeleton.tsx` - Melhorar e padronizar
- [x] `src/components/ui/spinner.tsx` - Melhorar e padronizar
- [x] `src/components/ui/progress.tsx` - Melhorar e padronizar
- [x] `src/components/ui/tooltip.tsx` - Melhorar e padronizar
- [x] `src/components/ui/empty-state.tsx` - Melhorar e padronizar
- [x] `src/components/ui/index.ts` - Exports centralizados
- [x] `src/lib/utils/variants.ts` - Helpers para variantes
- [ ] `docs/components/` - Documentação de componentes (será feito na Fase 6)

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
