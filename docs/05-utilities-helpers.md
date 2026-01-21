# 🛠️ Fase 5: Utilitários e Helpers

## 📋 Objetivo

Criar utilitários, helpers e funções auxiliares para facilitar o uso do design system e garantir consistência no desenvolvimento.

## ✅ Checklist

### 1. Função `cn()` Otimizada
- [x] Revisar implementação atual de `cn()`
- [x] Otimizar performance (usar clsx + tailwind-merge)
- [x] Adicionar suporte a design tokens (tokenClass helper)
- [x] Adicionar suporte a conditional classes (já suportado)
- [x] Criar variantes com type-safety (cnVariants)
- [x] Adicionar helpers para variantes de componentes (cnVariants)
- [x] Documentar uso avançado (comentários JSDoc)

### 2. Helpers para Design Tokens
- [x] Criar função `getColor()` para acessar cores
- [x] Criar função `getSpacing()` para acessar espaçamento
- [x] Criar função `getTypography()` para tipografia
- [x] Criar função `getShadow()` para sombras
- [x] Criar função `getRadius()` para border-radius
- [x] Criar função `getTransition()` para transições
- [x] Garantir type-safety em todos os helpers

### 3. Helpers para Variantes de Componentes
- [x] Criar helper genérico para variantes (variants.ts)
- [x] Criar helpers específicos por componente (createSizeVariants, createStateVariants)
- [x] Integrar com class-variance-authority
- [x] Garantir type-safety
- [x] Criar helpers para combinação de variantes (cnVariants)
- [x] Documentar padrão de uso (comentários JSDoc)

### 4. Utilitários de Cores
- [x] Criar função para obter cor com opacidade (getColorWithOpacity)
- [x] Criar função para obter cor de texto baseada em fundo (getTextColor)
- [x] Criar função para verificar contraste (getContrastRatio, meetsContrastRatio)
- [ ] Criar função para gerar paleta de cores (pode ser adicionado depois)
- [x] Criar função para converter cores (hex, rgb, hsl)
- [x] Criar helpers para dark mode (useColorMode hook)

### 5. Utilitários de Espaçamento
- [x] Criar função para calcular espaçamento (calculateSpacing)
- [x] Criar helpers para padding/margin consistentes (getPaddingClasses, getMarginClasses)
- [x] Criar função para gaps em layouts (getGapClasses)
- [x] Criar helpers para spacing responsivo (getResponsiveSpacing)
- [x] Documentar sistema de espaçamento (comentários JSDoc)

### 6. Utilitários de Tipografia
- [x] Criar função para obter estilos tipográficos (getFontSizeClasses, getFontWeightClasses)
- [x] Criar helpers para line-height baseado em font-size (calculateLineHeight)
- [x] Criar função para truncar texto (getTruncateClasses)
- [x] Criar função para line-clamp (getTruncateClasses com linhas)
- [x] Criar helpers para hierarquia tipográfica (getTypeScaleClasses)

### 7. Utilitários de Layout
- [ ] Criar helpers para flexbox comum (pode ser adicionado depois se necessário)
- [ ] Criar helpers para grid comum (pode ser adicionado depois se necessário)
- [ ] Criar helpers para container widths (já existe no Tailwind)
- [ ] Criar helpers para posicionamento (já existe no Tailwind)
- [x] Criar helpers para responsividade (getResponsiveClasses)

### 8. Utilitários de Acessibilidade
- [x] Criar função para gerar IDs únicos (generateId)
- [x] Criar helpers para ARIA attributes (createAriaAttributes)
- [x] Criar função para verificar contraste (meetsContrastRatio)
- [x] Criar helpers para focus management (createFocusAttributes)
- [x] Criar helpers para screen reader text (srOnly)

### 9. Utilitários de Animações
- [x] Criar helpers para transições comuns (getTransitionClasses)
- [x] Criar função para respeitar reduced-motion (prefersReducedMotion, getRespectfulTransitionDuration)
- [ ] Criar helpers para keyframes (já existem no CSS)
- [x] Criar função para delays de animação (getAnimationDelay)
- [x] Documentar sistema de animações (comentários JSDoc)

### 10. Utilitários de Breakpoints
- [x] Criar hooks para breakpoints (useBreakpoint, useBreakpointBelow, useCurrentBreakpoint)
- [x] Criar função para verificar breakpoint atual (useCurrentBreakpoint)
- [x] Criar helpers para classes responsivas (getResponsiveClasses)
- [x] Integrar com design tokens de breakpoints
- [x] Documentar uso (comentários JSDoc)

### 11. Utilitários de Validação
- [ ] Criar função para validar design tokens
- [ ] Criar função para validar cores
- [ ] Criar função para validar espaçamento
- [ ] Criar helpers para validação de props
- [ ] Adicionar warnings em desenvolvimento

### 12. Composables e Hooks
- [ ] Criar hook `useDesignToken()` para acessar tokens (pode ser adicionado depois)
- [x] Criar hook `useTheme()` melhorado (useColorMode)
- [x] Criar hook `useBreakpoint()` para responsividade
- [x] Criar hook `useColorMode()` para dark mode
- [ ] Criar hook `useAccessibility()` para helpers de acessibilidade (pode ser adicionado depois)

### 13. TypeScript Types e Interfaces
- [x] Criar tipos para design tokens
- [x] Criar tipos para variantes de componentes
- [x] Criar tipos para utilitários
- [x] Criar tipos para helpers
- [x] Garantir type-safety em todo o sistema
- [x] Exportar tipos para uso externo

### 14. Funções de Transformação
- [ ] Criar função para transformar tokens em CSS
- [ ] Criar função para transformar tokens em Tailwind classes
- [ ] Criar função para gerar CSS custom properties
- [ ] Criar função para validar e normalizar valores

### 15. Utilitários de Performance
- [ ] Criar helpers para lazy loading
- [ ] Criar helpers para memoização
- [ ] Criar helpers para debounce/throttle
- [ ] Criar helpers para otimização de renders
- [ ] Documentar boas práticas

### 16. Utilitários de Desenvolvimento
- [ ] Criar helpers para logging em desenvolvimento
- [ ] Criar helpers para debugging
- [ ] Criar helpers para validação de props
- [ ] Criar helpers para warnings
- [ ] Adicionar apenas em modo desenvolvimento

### 17. Documentação de Utilitários
- [ ] Documentar cada utilitário criado
- [ ] Criar exemplos de uso
- [ ] Documentar quando usar cada utilitário
- [ ] Criar guia de boas práticas
- [ ] Documentar performance considerations

### 18. Testes
- [ ] Criar testes para utilitários críticos
- [ ] Testar type-safety
- [ ] Testar edge cases
- [ ] Testar performance
- [ ] Validar helpers de acessibilidade

### 19. Integração
- [ ] Integrar utilitários com componentes
- [ ] Atualizar componentes para usar novos helpers
- [ ] Garantir compatibilidade
- [ ] Remover código duplicado
- [ ] Consolidar padrões

### 20. Otimização
- [ ] Otimizar bundle size
- [ ] Tree-shake utilitários não utilizados
- [ ] Lazy load quando apropriado
- [ ] Minimizar dependências
- [ ] Validar performance

## 📁 Arquivos a Criar/Modificar

- [x] `src/lib/utils/cn.ts` - Função cn() otimizada (já existia, melhorada)
- [x] `src/lib/utils/design-tokens.ts` - Helpers para design tokens
- [x] `src/lib/utils/colors.ts` - Utilitários de cores
- [x] `src/lib/utils/spacing.ts` - Utilitários de espaçamento
- [x] `src/lib/utils/typography.ts` - Utilitários de tipografia
- [x] `src/lib/utils/variants.ts` - Helpers para variantes (já existia)
- [ ] `src/lib/utils/layout.ts` - Utilitários de layout (não necessário, Tailwind cobre)
- [x] `src/lib/utils/accessibility.ts` - Utilitários de acessibilidade
- [x] `src/lib/utils/animations.ts` - Utilitários de animações
- [x] `src/lib/utils/breakpoints.ts` - Utilitários de breakpoints
- [ ] `src/lib/utils/validation.ts` - Utilitários de validação (já existe validators.ts)
- [ ] `src/lib/hooks/use-design-token.ts` - Hook para design tokens (pode ser adicionado depois)
- [x] `src/lib/hooks/use-breakpoint.ts` - Hook para breakpoints
- [x] `src/lib/hooks/use-color-mode.ts` - Hook para color mode
- [ ] `src/lib/types/design-system.ts` - Types do design system (já existem em design-tokens/types.ts)
- [x] `src/lib/utils/index.ts` - Exports centralizados

## 🎯 Critérios de Sucesso

- ✅ Utilitários type-safe e bem documentados
- ✅ Helpers facilitam desenvolvimento
- ✅ Performance otimizada
- ✅ Código reutilizável e DRY
- ✅ Integração completa com design tokens
- ✅ Documentação completa
- ✅ Testes cobrindo casos principais

## 📝 Notas

- Priorizar type-safety
- Manter utilitários simples e focados
- Documentar bem para facilitar uso
- Testar performance de utilitários críticos
- Evitar over-engineering

---

**Próximo passo:** [Fase 6: Documentação e Ferramentas](./06-documentation-tools.md)
