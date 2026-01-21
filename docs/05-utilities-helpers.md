# 🛠️ Fase 5: Utilitários e Helpers

## 📋 Objetivo

Criar utilitários, helpers e funções auxiliares para facilitar o uso do design system e garantir consistência no desenvolvimento.

## ✅ Checklist

### 1. Função `cn()` Otimizada
- [ ] Revisar implementação atual de `cn()`
- [ ] Otimizar performance (usar clsx + tailwind-merge)
- [ ] Adicionar suporte a design tokens
- [ ] Adicionar suporte a conditional classes
- [ ] Criar variantes com type-safety
- [ ] Adicionar helpers para variantes de componentes
- [ ] Documentar uso avançado

### 2. Helpers para Design Tokens
- [ ] Criar função `getColor()` para acessar cores
- [ ] Criar função `getSpacing()` para acessar espaçamento
- [ ] Criar função `getTypography()` para tipografia
- [ ] Criar função `getShadow()` para sombras
- [ ] Criar função `getRadius()` para border-radius
- [ ] Criar função `getTransition()` para transições
- [ ] Garantir type-safety em todos os helpers

### 3. Helpers para Variantes de Componentes
- [ ] Criar helper genérico para variantes
- [ ] Criar helpers específicos por componente
- [ ] Integrar com class-variance-authority
- [ ] Garantir type-safety
- [ ] Criar helpers para combinação de variantes
- [ ] Documentar padrão de uso

### 4. Utilitários de Cores
- [ ] Criar função para obter cor com opacidade
- [ ] Criar função para obter cor de texto baseada em fundo
- [ ] Criar função para verificar contraste
- [ ] Criar função para gerar paleta de cores
- [ ] Criar função para converter cores (hex, rgb, hsl)
- [ ] Criar helpers para dark mode

### 5. Utilitários de Espaçamento
- [ ] Criar função para calcular espaçamento
- [ ] Criar helpers para padding/margin consistentes
- [ ] Criar função para gaps em layouts
- [ ] Criar helpers para spacing responsivo
- [ ] Documentar sistema de espaçamento

### 6. Utilitários de Tipografia
- [ ] Criar função para obter estilos tipográficos
- [ ] Criar helpers para line-height baseado em font-size
- [ ] Criar função para truncar texto
- [ ] Criar função para line-clamp
- [ ] Criar helpers para hierarquia tipográfica

### 7. Utilitários de Layout
- [ ] Criar helpers para flexbox comum
- [ ] Criar helpers para grid comum
- [ ] Criar helpers para container widths
- [ ] Criar helpers para posicionamento
- [ ] Criar helpers para responsividade

### 8. Utilitários de Acessibilidade
- [ ] Criar função para gerar IDs únicos
- [ ] Criar helpers para ARIA attributes
- [ ] Criar função para verificar contraste
- [ ] Criar helpers para focus management
- [ ] Criar helpers para screen reader text

### 9. Utilitários de Animações
- [ ] Criar helpers para transições comuns
- [ ] Criar função para respeitar reduced-motion
- [ ] Criar helpers para keyframes
- [ ] Criar função para delays de animação
- [ ] Documentar sistema de animações

### 10. Utilitários de Breakpoints
- [ ] Criar hooks para breakpoints (useMediaQuery)
- [ ] Criar função para verificar breakpoint atual
- [ ] Criar helpers para classes responsivas
- [ ] Integrar com design tokens de breakpoints
- [ ] Documentar uso

### 11. Utilitários de Validação
- [ ] Criar função para validar design tokens
- [ ] Criar função para validar cores
- [ ] Criar função para validar espaçamento
- [ ] Criar helpers para validação de props
- [ ] Adicionar warnings em desenvolvimento

### 12. Composables e Hooks
- [ ] Criar hook `useDesignToken()` para acessar tokens
- [ ] Criar hook `useTheme()` melhorado
- [ ] Criar hook `useBreakpoint()` para responsividade
- [ ] Criar hook `useColorMode()` para dark mode
- [ ] Criar hook `useAccessibility()` para helpers de acessibilidade

### 13. TypeScript Types e Interfaces
- [ ] Criar tipos para design tokens
- [ ] Criar tipos para variantes de componentes
- [ ] Criar tipos para utilitários
- [ ] Criar tipos para helpers
- [ ] Garantir type-safety em todo o sistema
- [ ] Exportar tipos para uso externo

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

- [ ] `src/lib/utils/cn.ts` - Função cn() otimizada
- [ ] `src/lib/utils/design-tokens.ts` - Helpers para design tokens
- [ ] `src/lib/utils/colors.ts` - Utilitários de cores
- [ ] `src/lib/utils/spacing.ts` - Utilitários de espaçamento
- [ ] `src/lib/utils/typography.ts` - Utilitários de tipografia
- [ ] `src/lib/utils/variants.ts` - Helpers para variantes
- [ ] `src/lib/utils/layout.ts` - Utilitários de layout
- [ ] `src/lib/utils/accessibility.ts` - Utilitários de acessibilidade
- [ ] `src/lib/utils/animations.ts` - Utilitários de animações
- [ ] `src/lib/utils/breakpoints.ts` - Utilitários de breakpoints
- [ ] `src/lib/utils/validation.ts` - Utilitários de validação
- [ ] `src/lib/hooks/use-design-token.ts` - Hook para design tokens
- [ ] `src/lib/hooks/use-breakpoint.ts` - Hook para breakpoints
- [ ] `src/lib/hooks/use-color-mode.ts` - Hook para color mode
- [ ] `src/lib/types/design-system.ts` - Types do design system
- [ ] `src/lib/utils/index.ts` - Exports centralizados

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
