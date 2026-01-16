# Contribuindo para Amazon Fruit

Obrigado por considerar contribuir para o Amazon Fruit! Este documento fornece diretrizes para contribuições.

## 📋 Índice

- [Como Contribuir](#como-contribuir)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)
- [Comandos Úteis](#comandos-úteis)

## 🚀 Como Contribuir

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Depois clone seu fork
git clone https://github.com/seu-usuario/amazon-fruit.git
cd amazon-fruit
```

### 2. Instale as Dependências

```bash
npm install
```

### 3. Crie uma Branch

```bash
git checkout -b feature/sua-feature
# ou
git checkout -b fix/seu-bugfix
```

**Convenção de nomes de branches:**
- `feature/` - Novas funcionalidades
- `fix/` - Correção de bugs
- `docs/` - Documentação
- `refactor/` - Refatoração
- `test/` - Testes

### 4. Faça suas Alterações

- Siga os [padrões de código](#padrões-de-código)
- Escreva testes para novas funcionalidades
- Atualize a documentação quando necessário

### 5. Teste suas Alterações

```bash
# Rodar linter
npm run lint

# Verificar tipos
npm run type-check

# Rodar testes
npm test

# Verificar formatação
npm run format:check
```

### 6. Commit suas Alterações

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade X"
```

**Convenção de commits (Conventional Commits):**
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação, pontos e vírgulas, etc
- `refactor:` - Refatoração
- `test:` - Testes
- `chore:` - Tarefas de build, configuração, etc

### 7. Push e Abra um Pull Request

```bash
git push origin feature/sua-feature
```

Depois abra um Pull Request no GitHub.

## 📝 Padrões de Código

### TypeScript

- Use `strict` mode sempre
- Evite `any`, prefira tipos específicos
- Use interfaces para objetos, types para unions/intersections

```ts
// ✅ Bom
interface User {
  id: string;
  name: string;
}

// ❌ Ruim
const user: any = { id: '1', name: 'João' };
```

### Componentes React

- Use function components com hooks
- Componentes devem ser pequenos e focados
- Props devem ser tipadas

```tsx
// ✅ Bom
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} className={variant}>
      {label}
    </button>
  );
}

// ❌ Ruim
export function Button(props: any) {
  return <button>{props.label}</button>;
}
```

### Estilização

- Use Tailwind CSS para estilos
- Evite estilos inline quando possível
- Use `cn()` para combinar classes condicionalmente

```tsx
// ✅ Bom
import { cn } from '@/lib/utils';

<div className={cn('base-class', isActive && 'active-class')} />

// ❌ Ruim
<div style={{ color: isActive ? 'blue' : 'red' }} />
```

### Testes

- Um arquivo de teste para cada componente/função
- Use `describe` e `it` para organizar testes
- Teste comportamentos, não implementação

```tsx
// ✅ Bom
describe('Button', () => {
  it('deve renderizar o label corretamente', () => {
    render(<Button label="Clique aqui" />);
    expect(screen.getByText('Clique aqui')).toBeInTheDocument();
  });

  it('deve chamar onClick quando clicado', () => {
    const handleClick = jest.fn();
    render(<Button label="Teste" onClick={handleClick} />);
    fireEvent.click(screen.getByText('Teste'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Acessibilidade

- Sempre adicione `aria-label` em elementos interativos sem texto visível
- Use elementos semânticos HTML (`<button>`, `<nav>`, `<main>`, etc)
- Garanta contraste adequado de cores

```tsx
// ✅ Bom
<button aria-label="Fechar modal">
  <XIcon />
</button>

// ❌ Ruim
<div onClick={handleClose}>
  <XIcon />
</div>
```

### Nomenclatura

- Componentes: PascalCase (`UserProfile.tsx`)
- Funções: camelCase (`getUserData`)
- Constantes: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- Arquivos: kebab-case para páginas, PascalCase para componentes

## 🔄 Processo de Pull Request

### Checklist Antes de Abrir PR

- [ ] Código segue os padrões definidos
- [ ] Testes passam (`npm test`)
- [ ] Linter passa (`npm run lint`)
- [ ] Type check passa (`npm run type-check`)
- [ ] Documentação atualizada (se necessário)
- [ ] Commits seguem Conventional Commits

### Template de Pull Request

```markdown
## Descrição
Descreva brevemente o que este PR faz.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## Como testar
Passos para testar as mudanças:
1. ...
2. ...

## Screenshots (se aplicável)
[Adicione screenshots aqui]

## Checklist
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Código segue padrões do projeto
```

## 🛠 Comandos Úteis

```bash
# Desenvolvimento
npm run dev              # Inicia servidor de desenvolvimento

# Qualidade
npm run lint             # Executa ESLint
npm run lint:fix         # Corrige problemas do ESLint
npm run format           # Formata código com Prettier
npm run format:check     # Verifica formatação
npm run type-check       # Verifica tipos TypeScript

# Testes
npm test                 # Executa testes
npm test:watch           # Executa testes em modo watch
npm test:coverage        # Executa testes com cobertura

# Build
npm run build            # Build para produção
npm start                # Inicia servidor de produção
```

## 📚 Recursos

- [Conventional Commits](https://www.conventionalcommits.org/)
- [React Best Practices](https://react.dev/learn/thinking-in-react)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🤝 Código de Conduta

Seja respeitoso e profissional em todas as interações. Respeitamos todos os tipos de contribuidores e contribuições.

---

Obrigado por contribuir! 🎉
