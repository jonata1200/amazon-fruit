# ⚡ Fase 2: Otimização do Tailwind CSS

## 📋 Objetivo

Otimizar a configuração do Tailwind CSS, melhorar performance, criar utilitários customizados e garantir uso eficiente.

## ✅ Checklist

### 1. Análise da Configuração Atual
- [ ] Revisar `tailwind.config.ts` atual
- [ ] Analisar uso de classes Tailwind no projeto
- [ ] Identificar classes não utilizadas
- [ ] Verificar tamanho do bundle CSS
- [ ] Analisar performance de build

### 2. Otimização de Content Paths
- [ ] Revisar paths em `content` array
- [ ] Garantir que todos os arquivos relevantes estão incluídos
- [ ] Remover paths desnecessários
- [ ] Otimizar glob patterns para melhor performance
- [ ] Adicionar exclusões para node_modules e build

### 3. Configuração de Purge/Tree-shaking
- [ ] Verificar se purge está configurado corretamente
- [ ] Configurar safelist para classes dinâmicas
- [ ] Adicionar patterns para preservar classes necessárias
- [ ] Testar que classes importantes não são removidas
- [ ] Otimizar safelist para mínimo necessário

### 4. Extensão do Theme
- [ ] Integrar design tokens no theme do Tailwind
- [ ] Mapear tokens de cores para Tailwind colors
- [ ] Configurar spacing scale baseado em tokens
- [ ] Adicionar font families dos tokens
- [ ] Configurar typography scale
- [ ] Adicionar border radius dos tokens
- [ ] Configurar box shadows dos tokens
- [ ] Adicionar breakpoints customizados (se necessário)

### 5. Plugins Customizados
- [ ] Criar plugin para design tokens
- [ ] Criar plugin para utilitários customizados
- [ ] Criar plugin para componentes comuns
- [ ] Adicionar plugin para animações customizadas
- [ ] Criar plugin para variantes customizadas
- [ ] Documentar cada plugin criado

### 6. Utilitários Customizados
- [ ] Criar utilitários para espaçamento consistente
- [ ] Criar utilitários para cores semânticas
- [ ] Criar utilitários para tipografia
- [ ] Criar utilitários para elevação/shadows
- [ ] Criar utilitários para transições
- [ ] Criar utilitários para layout comum
- [ ] Criar utilitários para acessibilidade

### 7. Variantes Customizadas
- [ ] Criar variantes para estados de componentes
- [ ] Criar variantes para breakpoints customizados
- [ ] Criar variantes para dark mode melhorado
- [ ] Criar variantes para reduced-motion (acessibilidade)
- [ ] Criar variantes para print media

### 8. Performance e Build
- [ ] Configurar JIT mode (já ativo por padrão no Tailwind v4)
- [ ] Otimizar ordem de plugins
- [ ] Configurar minificação de CSS
- [ ] Verificar tamanho do CSS final
- [ ] Otimizar imports de Tailwind
- [ ] Configurar source maps para desenvolvimento

### 9. Integração com PostCSS
- [ ] Revisar `postcss.config.mjs`
- [ ] Garantir ordem correta de plugins
- [ ] Configurar autoprefixer
- [ ] Otimizar processamento de CSS
- [ ] Configurar para produção e desenvolvimento

### 10. CSS Variables e Custom Properties
- [ ] Garantir que variáveis CSS estão acessíveis no Tailwind
- [ ] Criar bridge entre CSS vars e Tailwind
- [ ] Testar uso de variáveis em classes Tailwind
- [ ] Documentar uso de variáveis customizadas

### 11. Função `cn()` Otimizada
- [ ] Revisar implementação atual de `cn()`
- [ ] Otimizar para melhor performance
- [ ] Adicionar suporte a conditional classes
- [ ] Adicionar suporte a design tokens
- [ ] Criar helpers para variantes de componentes
- [ ] Adicionar TypeScript types melhorados

### 12. Linting e Validação
- [ ] Configurar ESLint para Tailwind
- [ ] Adicionar regras para uso consistente
- [ ] Criar regras customizadas se necessário
- [ ] Configurar validação de classes Tailwind
- [ ] Adicionar warnings para classes não utilizadas

### 13. Documentação de Uso
- [ ] Documentar utilitários customizados
- [ ] Criar guia de uso do Tailwind no projeto
- [ ] Documentar convenções e padrões
- [ ] Criar exemplos de uso
- [ ] Documentar anti-patterns a evitar

### 14. Testes e Validação
- [ ] Testar build em desenvolvimento
- [ ] Testar build em produção
- [ ] Verificar que todas as classes funcionam
- [ ] Testar dark mode
- [ ] Validar acessibilidade
- [ ] Verificar performance de renderização

### 15. Migração e Refatoração
- [ ] Identificar uso de classes inline que podem ser utilitários
- [ ] Refatorar componentes para usar utilitários customizados
- [ ] Remover classes duplicadas
- [ ] Consolidar padrões comuns
- [ ] Atualizar componentes existentes

## 📁 Arquivos a Criar/Modificar

- [ ] `tailwind.config.ts` - Configuração otimizada
- [ ] `postcss.config.mjs` - Configuração PostCSS
- [ ] `src/lib/utils/cn.ts` - Função cn() otimizada
- [ ] `src/lib/tailwind/plugins.ts` - Plugins customizados
- [ ] `src/lib/tailwind/utilities.ts` - Utilitários customizados
- [ ] `src/lib/tailwind/variants.ts` - Variantes customizadas
- [ ] `.eslintrc.js` ou `eslint.config.mjs` - Regras ESLint para Tailwind
- [ ] `src/app/globals.css` - Imports e configurações CSS

## 🎯 Critérios de Sucesso

- ✅ Build do Tailwind otimizado e rápido
- ✅ CSS final menor e mais eficiente
- ✅ Utilitários customizados funcionando
- ✅ Design tokens integrados
- ✅ Dark mode funcionando perfeitamente
- ✅ Performance melhorada
- ✅ Documentação completa

## 📝 Notas

- Tailwind v4 usa JIT por padrão, não precisa configurar
- Focar em reutilização e consistência
- Manter compatibilidade com código existente
- Testar cada mudança antes de avançar

---

**Próximo passo:** [Fase 3: Sistema de Tipografia](./03-typography-system.md)
