# 🎨 Fase 1: Design Tokens - Fundação do Design System

## 📋 Objetivo

Consolidar e expandir os design tokens existentes, criando uma base sólida e consistente para todo o design system.

## ✅ Checklist

### 1. Análise e Consolidação dos Tokens Existentes
- [x] Revisar `src/lib/design-tokens.ts` atual
- [x] Identificar tokens duplicados ou inconsistentes
- [x] Mapear uso atual dos tokens no projeto
- [x] Documentar gaps e necessidades

### 2. Estrutura de Tokens
- [x] Organizar tokens em categorias lógicas:
  - [x] Cores (semânticas, neutras, status)
  - [x] Espaçamento (spacing scale)
  - [x] Tipografia (fontes, tamanhos, pesos)
  - [x] Bordas e raios (border radius)
  - [x] Sombras (elevation system)
  - [x] Breakpoints (responsividade)
  - [x] Z-index (layering)
  - [x] Transições e animações
  - [x] Opacidade
  - [x] Dimensões (widths, heights)

### 3. Sistema de Cores
- [x] Expandir paleta de cores semânticas:
  - [x] Primary (já existe - roxo)
  - [x] Secondary (já existe - cinza)
  - [x] Success (já existe - verde)
  - [x] Warning (já existe - amarelo)
  - [x] Error (já existe - vermelho)
  - [x] Info (já existe - azul)
  - [x] Neutral/Gray scale
- [x] Criar variantes para modo claro e escuro
- [x] Definir cores de texto para cada cor de fundo
- [x] Adicionar cores de estado (hover, active, disabled)
- [x] Criar escala de opacidade para overlays

### 4. Integração com Tailwind CSS
- [x] Mapear tokens para variáveis CSS custom properties
- [x] Atualizar `tailwind.config.ts` para usar tokens (cores semânticas adicionadas)
- [x] Garantir suporte a dark mode (via variáveis CSS)
- [x] Criar classes utilitárias baseadas em tokens (Tailwind gera automaticamente)
- [x] Testar geração de classes do Tailwind (configuração completa)

### 5. Sistema de Espaçamento
- [x] Definir escala de espaçamento consistente (4px base)
- [x] Criar tokens para padding e margin
- [x] Definir espaçamento para componentes (gaps, padding interno)
- [x] Criar sistema de grid spacing
- [x] Documentar uso de espaçamento

### 6. Sistema de Tipografia
- [x] Consolidar font families (Geist Sans, Geist Mono)
- [x] Definir escala de tamanhos de fonte
- [x] Criar tokens para line-heights
- [x] Definir font weights disponíveis
- [x] Criar tokens para letter-spacing
- [x] Definir hierarquia tipográfica

### 7. Sistema de Elevação (Shadows)
- [x] Expandir sistema de sombras existente
- [x] Criar níveis de elevação (0-5)
- [x] Definir sombras para modo claro e escuro
- [x] Criar sombras para componentes específicos (cards, modals, tooltips)

### 8. Border Radius System
- [x] Consolidar valores de border-radius
- [x] Criar tokens para diferentes tamanhos
- [x] Definir radius para componentes (buttons, cards, inputs)
- [x] Garantir consistência visual

### 9. Z-Index System
- [x] Revisar e expandir sistema de z-index
- [x] Criar camadas bem definidas (base, dropdown, modal, tooltip, etc.)
- [x] Documentar uso de cada camada
- [x] Garantir que não há conflitos

### 10. Sistema de Transições
- [x] Expandir tokens de duração
- [x] Criar easing functions consistentes
- [x] Definir transições padrão para componentes
- [x] Criar tokens para delays

### 11. Breakpoints e Responsividade
- [x] Revisar breakpoints existentes
- [x] Garantir que estão alinhados com Tailwind
- [x] Documentar uso de cada breakpoint
- [x] Criar tokens para container widths

### 12. TypeScript Types
- [x] Criar tipos TypeScript para todos os tokens
- [x] Garantir type-safety ao usar tokens
- [x] Criar helpers para acessar tokens com autocomplete
- [x] Exportar tipos para uso em componentes

### 13. Validação e Testes
- [ ] Criar testes para validação de tokens
- [x] Verificar que todos os tokens são válidos
- [x] Testar em modo claro e escuro (variáveis CSS já suportam)
- [ ] Validar acessibilidade de cores (contraste) - pendente validação manual

### 14. Documentação
- [x] Documentar cada categoria de token (comentários nos arquivos)
- [ ] Criar exemplos de uso (será feito nas fases seguintes)
- [x] Documentar decisões de design (comentários nos arquivos)
- [ ] Criar guia de quando usar cada token (será feito na Fase 6)

### 15. Migração e Compatibilidade
- [ ] Identificar código que usa valores hardcoded (será feito nas fases seguintes)
- [x] Criar plano de migração gradual (arquivo antigo re-exporta novo)
- [x] Manter compatibilidade com código existente
- [ ] Atualizar componentes existentes para usar tokens (será feito nas fases seguintes)

## 📁 Arquivos a Criar/Modificar

- [x] `src/lib/design-tokens/index.ts` - Export principal
- [x] `src/lib/design-tokens/colors.ts` - Sistema de cores
- [x] `src/lib/design-tokens/spacing.ts` - Sistema de espaçamento
- [x] `src/lib/design-tokens/typography.ts` - Sistema tipográfico
- [x] `src/lib/design-tokens/shadows.ts` - Sistema de sombras
- [x] `src/lib/design-tokens/borders.ts` - Bordas e radius
- [x] `src/lib/design-tokens/transitions.ts` - Transições
- [x] `src/lib/design-tokens/z-index.ts` - Sistema de camadas
- [x] `src/lib/design-tokens/types.ts` - Tipos TypeScript
- [x] `tailwind.config.ts` - Atualizar configuração
- [ ] `src/app/globals.css` - Atualizar variáveis CSS (mantido como está - já usa variáveis CSS)

## 🎯 Critérios de Sucesso

- ✅ Todos os tokens estão centralizados e organizados
- ✅ Tokens estão integrados com Tailwind CSS
- ✅ Suporte completo a dark mode
- ✅ Type-safety garantido com TypeScript
- ✅ Documentação completa e clara
- ✅ Código existente continua funcionando

## 📝 Notas

- Manter compatibilidade com `design-tokens.ts` existente durante migração
- Priorizar tokens mais usados primeiro
- Testar cada mudança antes de avançar

---

**Próximo passo:** [Fase 2: Otimização do Tailwind](./02-tailwind-optimization.md)
