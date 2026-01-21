# 📝 Fase 3: Sistema de Tipografia

## 📋 Objetivo

Criar um sistema tipográfico consistente, acessível e bem estruturado usando os design tokens e Tailwind CSS.

## ✅ Checklist

### 1. Análise da Tipografia Atual
- [ ] Revisar uso de tipografia no projeto
- [ ] Identificar inconsistências
- [ ] Mapear tamanhos de fonte usados
- [ ] Analisar hierarquia tipográfica atual
- [ ] Verificar acessibilidade (contraste, tamanhos)

### 2. Escala Tipográfica
- [ ] Definir escala baseada em design tokens
- [ ] Criar hierarquia clara (h1-h6, body, small, etc.)
- [ ] Garantir proporção harmônica entre tamanhos
- [ ] Definir line-heights para cada tamanho
- [ ] Criar tokens para letter-spacing quando necessário
- [ ] Documentar escala tipográfica

### 3. Font Families
- [ ] Consolidar font families (Geist Sans, Geist Mono)
- [ ] Configurar fallbacks apropriados
- [ ] Garantir carregamento otimizado de fontes
- [ ] Configurar font-display strategy
- [ ] Adicionar suporte a fontes variáveis (se aplicável)

### 4. Componentes de Texto
- [ ] Criar componente `Text` base
- [ ] Criar componente `Heading` (H1-H6)
- [ ] Criar componente `Paragraph`
- [ ] Criar componente `Label`
- [ ] Criar componente `Caption`
- [ ] Criar componente `Code` (inline e block)
- [ ] Criar componente `Link` tipográfico

### 5. Variantes de Texto
- [ ] Criar variantes de tamanho (xs, sm, base, lg, xl, etc.)
- [ ] Criar variantes de peso (light, normal, medium, semibold, bold)
- [ ] Criar variantes de cor (baseado em design tokens)
- [ ] Criar variantes de alinhamento (left, center, right, justify)
- [ ] Criar variantes de transformação (uppercase, lowercase, capitalize)
- [ ] Criar variantes de truncamento (truncate, line-clamp)

### 6. Hierarquia Semântica
- [ ] Definir estilos para h1 (display/title)
- [ ] Definir estilos para h2 (heading)
- [ ] Definir estilos para h3 (subheading)
- [ ] Definir estilos para h4-h6
- [ ] Definir estilos para body text
- [ ] Definir estilos para small/caption text
- [ ] Garantir hierarquia visual clara

### 7. Responsividade Tipográfica
- [ ] Criar tamanhos responsivos (fluid typography)
- [ ] Definir breakpoints para ajustes tipográficos
- [ ] Garantir legibilidade em mobile
- [ ] Testar em diferentes tamanhos de tela
- [ ] Usar clamp() para tipografia fluida (se aplicável)

### 8. Acessibilidade
- [ ] Garantir contraste mínimo WCAG AA (4.5:1)
- [ ] Garantir contraste para texto grande WCAG AA (3:1)
- [ ] Verificar tamanhos mínimos (16px para body)
- [ ] Garantir line-height adequado (mínimo 1.5)
- [ ] Testar com leitores de tela
- [ ] Garantir que hierarquia é semântica (HTML correto)

### 9. Integração com Tailwind
- [ ] Criar classes utilitárias para tipografia
- [ ] Criar @apply directives para componentes
- [ ] Garantir que tokens estão acessíveis
- [ ] Criar variantes customizadas se necessário
- [ ] Documentar uso de classes tipográficas

### 10. Componentes Tipográficos
- [ ] Implementar componente `Text` com props TypeScript
- [ ] Implementar componente `Heading` com variantes
- [ ] Implementar componente `Paragraph`
- [ ] Implementar componente `Label`
- [ ] Implementar componente `Caption`
- [ ] Implementar componente `Code`
- [ ] Implementar componente `Link`
- [ ] Adicionar suporte a asChild (Radix UI pattern)

### 11. Estilos Especiais
- [ ] Criar estilos para texto destacado (highlight)
- [ ] Criar estilos para texto muted
- [ ] Criar estilos para texto de erro/sucesso
- [ ] Criar estilos para texto de ajuda/hint
- [ ] Criar estilos para texto de código
- [ ] Criar estilos para citações (blockquote)

### 12. Dark Mode
- [ ] Garantir contraste adequado em dark mode
- [ ] Ajustar cores de texto para dark mode
- [ ] Testar legibilidade em ambos os modos
- [ ] Garantir transições suaves

### 13. Performance
- [ ] Otimizar carregamento de fontes
- [ ] Usar font-display: swap
- [ ] Considerar subsetting de fontes
- [ ] Minimizar número de font weights carregados
- [ ] Usar preload para fontes críticas

### 14. Documentação
- [ ] Documentar escala tipográfica
- [ ] Criar guia de uso de componentes
- [ ] Documentar quando usar cada variante
- [ ] Criar exemplos visuais
- [ ] Documentar decisões de design

### 15. Testes e Validação
- [ ] Testar todos os componentes tipográficos
- [ ] Validar acessibilidade
- [ ] Testar em diferentes navegadores
- [ ] Testar responsividade
- [ ] Validar contraste de cores
- [ ] Testar com leitores de tela

### 16. Migração
- [ ] Identificar uso de tipografia inline
- [ ] Migrar para componentes tipográficos
- [ ] Atualizar componentes existentes
- [ ] Garantir compatibilidade

## 📁 Arquivos a Criar/Modificar

- [ ] `src/components/typography/text.tsx` - Componente Text base
- [ ] `src/components/typography/heading.tsx` - Componente Heading
- [ ] `src/components/typography/paragraph.tsx` - Componente Paragraph
- [ ] `src/components/typography/label.tsx` - Componente Label
- [ ] `src/components/typography/caption.tsx` - Componente Caption
- [ ] `src/components/typography/code.tsx` - Componente Code
- [ ] `src/components/typography/link.tsx` - Componente Link tipográfico
- [ ] `src/components/typography/index.ts` - Exports
- [ ] `src/lib/design-tokens/typography.ts` - Tokens tipográficos (se não existir)
- [ ] `tailwind.config.ts` - Adicionar configurações tipográficas
- [ ] `src/app/globals.css` - Estilos globais tipográficos

## 🎯 Critérios de Sucesso

- ✅ Sistema tipográfico consistente e bem estruturado
- ✅ Componentes reutilizáveis e type-safe
- ✅ Acessibilidade garantida (WCAG)
- ✅ Responsivo e legível em todos os tamanhos
- ✅ Integrado com design tokens
- ✅ Documentação completa
- ✅ Performance otimizada

## 📝 Notas

- Priorizar acessibilidade e legibilidade
- Manter consistência com design tokens
- Usar componentes semânticos (HTML correto)
- Testar em diferentes contextos

---

**Próximo passo:** [Fase 4: Componentes Base](./04-base-components.md)
