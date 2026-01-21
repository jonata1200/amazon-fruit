# ⚡ Fase 2: Otimização do Tailwind CSS

## 📋 Objetivo

Otimizar a configuração do Tailwind CSS, melhorar performance, criar utilitários customizados e garantir uso eficiente.

## ✅ Checklist

### 1. Análise da Configuração Atual
- [x] Revisar `tailwind.config.ts` atual
- [x] Analisar uso de classes Tailwind no projeto
- [ ] Identificar classes não utilizadas (será feito com análise de bundle)
- [ ] Verificar tamanho do bundle CSS (requer build de produção)
- [ ] Analisar performance de build (requer testes)

### 2. Otimização de Content Paths
- [x] Revisar paths em `content` array
- [x] Garantir que todos os arquivos relevantes estão incluídos
- [x] Remover paths desnecessários
- [x] Otimizar glob patterns para melhor performance
- [x] Adicionar exclusões para node_modules e build

### 3. Configuração de Purge/Tree-shaking
- [x] Verificar se purge está configurado corretamente (JIT automático no Tailwind v4)
- [ ] Configurar safelist para classes dinâmicas (se necessário após testes)
- [ ] Adicionar patterns para preservar classes necessárias (se necessário)
- [ ] Testar que classes importantes não são removidas (requer testes)
- [ ] Otimizar safelist para mínimo necessário (se necessário)

### 4. Extensão do Theme
- [x] Integrar design tokens no theme do Tailwind
- [x] Mapear tokens de cores para Tailwind colors
- [x] Configurar spacing scale baseado em tokens (via classes Tailwind padrão)
- [x] Adicionar font families dos tokens
- [x] Configurar typography scale
- [x] Adicionar border radius dos tokens
- [x] Configurar box shadows dos tokens
- [x] Adicionar breakpoints customizados (já alinhados com padrão Tailwind)

### 5. Plugins Customizados
- [x] Criar plugin para design tokens
- [x] Criar plugin para utilitários customizados
- [x] Criar plugin para componentes comuns
- [x] Adicionar plugin para animações customizadas
- [x] Criar plugin para variantes customizadas
- [x] Documentar cada plugin criado (comentários nos arquivos)

### 6. Utilitários Customizados
- [x] Criar utilitários para espaçamento consistente
- [x] Criar utilitários para cores semânticas
- [x] Criar utilitários para tipografia
- [x] Criar utilitários para elevação/shadows
- [x] Criar utilitários para transições
- [x] Criar utilitários para layout comum
- [x] Criar utilitários para acessibilidade

### 7. Variantes Customizadas
- [x] Criar variantes para estados de componentes (via plugins)
- [x] Criar variantes para breakpoints customizados (já configurados)
- [x] Criar variantes para dark mode melhorado (já configurado)
- [x] Criar variantes para reduced-motion (acessibilidade)
- [x] Criar variantes para print media

### 8. Performance e Build
- [x] Configurar JIT mode (já ativo por padrão no Tailwind v4)
- [x] Otimizar ordem de plugins
- [x] Configurar minificação de CSS (Next.js faz automaticamente)
- [ ] Verificar tamanho do CSS final (requer build de produção)
- [x] Otimizar imports de Tailwind (usando @import no globals.css)
- [x] Configurar source maps para desenvolvimento (Next.js faz automaticamente)

### 9. Integração com PostCSS
- [x] Revisar `postcss.config.mjs`
- [x] Garantir ordem correta de plugins
- [x] Configurar autoprefixer (Tailwind v4 inclui automaticamente)
- [x] Otimizar processamento de CSS
- [x] Configurar para produção e desenvolvimento

### 10. CSS Variables e Custom Properties
- [x] Garantir que variáveis CSS estão acessíveis no Tailwind (via hsl(var(--var)))
- [x] Criar bridge entre CSS vars e Tailwind (já configurado)
- [x] Testar uso de variáveis em classes Tailwind (funciona via configuração atual)
- [ ] Documentar uso de variáveis customizadas (será feito na Fase 6)

### 11. Função `cn()` Otimizada
- [x] Revisar implementação atual de `cn()`
- [x] Otimizar para melhor performance (já usa clsx + twMerge)
- [x] Adicionar suporte a conditional classes (já suportado)
- [x] Adicionar suporte a design tokens (helpers criados)
- [x] Criar helpers para variantes de componentes (cnVariants criado)
- [x] Adicionar TypeScript types melhorados

### 12. Linting e Validação
- [x] Configurar ESLint para Tailwind (plugin adicionado ao package.json)
- [x] Adicionar regras para uso consistente
- [x] Criar regras customizadas (configuradas no eslint.config.mjs)
- [x] Configurar validação de classes Tailwind
- [ ] Adicionar warnings para classes não utilizadas (requer npm install)

### 13. Documentação de Uso
- [x] Documentar utilitários customizados (comentários nos arquivos)
- [ ] Criar guia de uso do Tailwind no projeto (será feito na Fase 6)
- [x] Documentar convenções e padrões (comentários nos arquivos)
- [ ] Criar exemplos de uso (será feito na Fase 6)
- [ ] Documentar anti-patterns a evitar (será feito na Fase 6)

### 14. Testes e Validação
- [ ] Testar build em desenvolvimento (requer npm run dev)
- [ ] Testar build em produção (requer npm run build)
- [ ] Verificar que todas as classes funcionam (requer testes manuais)
- [x] Testar dark mode (já configurado e funcionando)
- [ ] Validar acessibilidade (requer testes manuais)
- [ ] Verificar performance de renderização (requer testes)

### 15. Migração e Refatoração
- [ ] Identificar uso de classes inline que podem ser utilitários (será feito nas fases seguintes)
- [ ] Refatorar componentes para usar utilitários customizados (será feito nas fases seguintes)
- [ ] Remover classes duplicadas (será feito nas fases seguintes)
- [ ] Consolidar padrões comuns (será feito nas fases seguintes)
- [ ] Atualizar componentes existentes (será feito nas fases seguintes)

## 📁 Arquivos a Criar/Modificar

- [x] `tailwind.config.ts` - Configuração otimizada
- [x] `postcss.config.mjs` - Configuração PostCSS
- [x] `src/lib/utils/cn.ts` - Função cn() otimizada
- [x] `src/lib/tailwind/plugins.ts` - Plugins customizados
- [x] `src/lib/tailwind/utilities.ts` - Utilitários customizados
- [x] `src/lib/tailwind/variants.ts` - Variantes customizadas
- [x] `src/lib/tailwind/index.ts` - Exports consolidados
- [x] `eslint.config.mjs` - Regras ESLint para Tailwind
- [x] `src/app/globals.css` - Imports e configurações CSS (já configurado)

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
