# ♿ Guia de Acessibilidade

Este documento descreve os padrões e práticas de acessibilidade adotados no projeto Amazon Fruit.

## 📋 Visão Geral

O projeto segue as diretrizes WCAG 2.1 nível AA, garantindo que a aplicação seja acessível para todos os usuários, incluindo aqueles que usam tecnologias assistivas.

## 🎯 Princípios Fundamentais

### 1. Perceptível
- Informações e componentes da interface devem ser apresentáveis aos usuários de forma que possam percebê-los.
- Contraste mínimo de 4.5:1 para texto normal e 3:1 para componentes UI.

### 2. Operável
- Componentes da interface e navegação devem ser operáveis.
- Navegação completa por teclado.
- Tempo suficiente para ler e usar o conteúdo.

### 3. Compreensível
- Informações e operação da interface devem ser compreensíveis.
- Textos claros e objetivos.
- Feedback de erros e validações.

### 4. Robusto
- O conteúdo deve ser robusto o suficiente para ser interpretado por uma ampla variedade de agentes de usuário.
- HTML semântico.
- Compatibilidade com tecnologias assistivas.

## ✅ Checklist para Novos Componentes

### Componentes Interativos

- [ ] Todos os botões têm `aria-label` ou texto visível
- [ ] Links icon-only têm `aria-label` descritivo
- [ ] Elementos desabilitados têm `aria-disabled="true"`
- [ ] Componentes expansíveis têm `aria-expanded`
- [ ] Popups têm `aria-haspopup` apropriado
- [ ] Formulários têm labels associados (`htmlFor` e `id`)

### Navegação por Teclado

- [ ] Todos os elementos interativos são focáveis
- [ ] Ordem de tabindex é lógica
- [ ] Focus visível em todos os elementos (outline)
- [ ] Trap focus em modais e dialogs
- [ ] Atalhos de teclado documentados

### Semântica HTML

- [ ] Uso de elementos semânticos (`<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`)
- [ ] Headings hierárquicos (`h1` → `h2` → `h3`)
- [ ] Listas usam `<ul>`, `<ol>`, `<li>`
- [ ] Formulários estruturados corretamente

### Contraste de Cores

- [ ] Texto normal: contraste mínimo 4.5:1
- [ ] Texto grande (18pt+): contraste mínimo 3:1
- [ ] Componentes UI: contraste mínimo 3:1
- [ ] Não depende apenas de cor para transmitir informação

### Screen Readers

- [ ] Regiões dinâmicas têm `aria-live="polite"` ou `aria-live="assertive"`
- [ ] Notificações são anunciadas
- [ ] Estados de loading são comunicados
- [ ] Erros são claramente identificados

### Imagens e Mídia

- [ ] Imagens decorativas têm `alt=""`
- [ ] Imagens informativas têm `alt` descritivo
- [ ] Vídeos têm legendas (se aplicável)
- [ ] Áudio tem transcrição (se aplicável)

## 🛠️ Ferramentas de Teste

### Testes Automatizados

- **axe-core**: Testes de acessibilidade automatizados
- **Playwright**: Testes E2E com verificação de acessibilidade
- **@axe-core/react**: Testes em componentes React

### Testes Manuais

- **Screen Readers**: NVDA (Windows), JAWS (Windows), VoiceOver (macOS/iOS)
- **Navegação por Teclado**: Testar toda a aplicação apenas com teclado
- **Contraste**: WebAIM Contrast Checker, Colour Contrast Analyser
- **Lighthouse**: Auditoria de acessibilidade

## 📝 Padrões de Código

### Exemplo: Botão Acessível

```tsx
<Button
  aria-label="Exportar relatório"
  aria-disabled={isExporting}
  disabled={isExporting}
>
  {isExporting ? 'Exportando...' : 'Exportar'}
</Button>
```

### Exemplo: Modal Acessível

```tsx
<Dialog>
  <DialogTrigger aria-haspopup="dialog" aria-expanded={isOpen}>
    Abrir
  </DialogTrigger>
  <DialogContent
    aria-labelledby="dialog-title"
    aria-describedby="dialog-description"
  >
    <DialogTitle id="dialog-title">Título</DialogTitle>
    <DialogDescription id="dialog-description">
      Descrição
    </DialogDescription>
  </DialogContent>
</Dialog>
```

### Exemplo: Formulário Acessível

```tsx
<div>
  <Label htmlFor="email">Email</Label>
  <Input
    id="email"
    type="email"
    aria-required="true"
    aria-invalid={hasError}
    aria-describedby={hasError ? "email-error" : undefined}
  />
  {hasError && (
    <span id="email-error" role="alert" className="text-destructive">
      Email inválido
    </span>
  )}
</div>
```

## 🔗 Recursos

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [A11y Project](https://www.a11yproject.com/)
- [WebAIM](https://webaim.org/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

## 📅 Revisão

Este guia deve ser revisado periodicamente e atualizado conforme novas práticas e diretrizes são estabelecidas.
