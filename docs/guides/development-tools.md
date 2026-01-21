# 🛠️ Ferramentas de Desenvolvimento

## Visão Geral

Este guia documenta as ferramentas e configurações disponíveis para facilitar o desenvolvimento com o design system.

## Snippets para VS Code

Snippets estão disponíveis em `.vscode/snippets.code-snippets`:

### Componentes

- `ds-button` - Componente Button
- `ds-input` - Componente Input com Label
- `ds-card` - Componente Card completo
- `ds-dialog` - Componente Dialog
- `ds-table` - Componente DataTable

### Utilitários

- `ds-token` - Hook useDesignToken
- `ds-cn` - Função cn()
- `ds-text` - Componentes de tipografia

## ESLint

### Configuração

O ESLint está configurado com regras específicas para o design system:

```javascript
// eslint.config.mjs
{
  rules: {
    // Tailwind CSS
    "tailwindcss/classnames-order": "warn",
    "tailwindcss/no-contradicting-classname": "error",
    
    // Design System
    "@typescript-eslint/no-unused-vars": "warn",
  }
}
```

### Executar

```bash
# Verificar erros
npm run lint

# Corrigir automaticamente
npm run lint:fix
```

## Prettier

### Configuração

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

### Executar

```bash
# Formatar arquivos
npm run format

# Verificar formatação
npm run format:check
```

## Validação de Tokens

### Script de Validação

```bash
# Validar design tokens
npm run validate:tokens
```

O script valida:
- Estrutura de tokens
- Valores de cores
- Contraste WCAG
- Espaçamento
- Tipografia

## Testes

### Executar Testes

```bash
# Todos os testes
npm test

# Modo watch
npm run test:watch

# Com cobertura
npm run test:coverage
```

### Estrutura

```
tests/
├── unit/
│   ├── components/    # Testes de componentes
│   └── lib/          # Testes de utilitários
├── helpers/          # Helpers de teste
└── templates/        # Templates para novos testes
```

## Type Checking

```bash
# Verificar tipos TypeScript
npm run type-check
```

## Build e Análise

```bash
# Build de produção
npm run build

# Analisar bundle
npm run analyze
```

## Git Hooks

O projeto usa Husky para git hooks:

- **Pre-commit**: Executa lint-staged
- **Pre-push**: Validações adicionais (se configurado)

## Workflow Recomendado

1. **Desenvolvimento**:
   ```bash
   npm run dev
   ```

2. **Antes de commitar**:
   ```bash
   npm run lint:fix
   npm run format
   npm run type-check
   npm test
   ```

3. **Antes de fazer push**:
   ```bash
   npm run build
   ```

## Debugging

### Dev Logger

```typescript
import { devLogger } from '@/lib/utils/development';

// Logs apenas em desenvolvimento
devLogger.log('Mensagem');
devLogger.warn('Aviso');
devLogger.error('Erro');
```

### Performance

```typescript
import { measurePerformance } from '@/lib/utils/development';

const result = measurePerformance('Operação', () => {
  // Código a ser medido
});
```

## Integração com Editores

### VS Code

1. Instale extensões recomendadas:
   - ESLint
   - Prettier
   - Tailwind CSS IntelliSense

2. Snippets já estão configurados em `.vscode/snippets.code-snippets`

### Configuração Recomendada

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

---

**Referência**: 
- `eslint.config.mjs` - Configuração ESLint
- `.prettierrc` - Configuração Prettier
- `.vscode/snippets.code-snippets` - Snippets VS Code
