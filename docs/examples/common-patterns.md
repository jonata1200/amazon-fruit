# 📚 Exemplos de Padrões Comuns

## Visão Geral

Este documento contém exemplos práticos de uso comum do design system em situações reais.

## Formulários

### Formulário Simples

```tsx
import { Input, Label, Button } from '@/components/ui';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);

  return (
    <Card className="max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Login</CardTitle>
      </CardHeader>
      <CardContent>
        <form className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              state={error ? 'error' : 'default'}
              showStateIcon={error}
              placeholder="seu@email.com"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Senha</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Digite sua senha"
            />
          </div>
          <Button type="submit" className="w-full">
            Entrar
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
```

### Formulário com Validação

```tsx
import { Input, Label, Button } from '@/components/ui';
import { useDebounce } from '@/lib/hooks/useDebounce';

function SearchForm() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      // Buscar...
    }
  }, [debouncedQuery]);

  return (
    <div className="space-y-2">
      <Label htmlFor="search">Buscar</Label>
      <Input
        id="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Digite para buscar..."
      />
    </div>
  );
}
```

## Cards e Layouts

### Grid de Cards

```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

function ProductGrid({ products }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product) => (
        <Card key={product.id} variant="elevated" className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle>{product.name}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{product.description}</p>
            <Button className="mt-4 w-full">Comprar</Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```

### Card com Ações

```tsx
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

function ActionCard({ title, description, onAction }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{description}</p>
      </CardContent>
      <CardFooter className="flex justify-end gap-2">
        <Button variant="outline">Cancelar</Button>
        <Button onClick={onAction}>Confirmar</Button>
      </CardFooter>
    </Card>
  );
}
```

## Modais e Diálogos

### Modal Simples

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

function ConfirmDialog({ open, onOpenChange, onConfirm }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent size="sm">
        <DialogHeader>
          <DialogTitle>Confirmar ação</DialogTitle>
        </DialogHeader>
        <p>Tem certeza que deseja continuar?</p>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancelar
          </Button>
          <Button variant="destructive" onClick={onConfirm}>
            Confirmar
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

### Modal com Formulário

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input, Label, Button } from '@/components/ui';

function EditDialog({ open, onOpenChange, data }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent size="lg">
        <DialogHeader>
          <DialogTitle>Editar</DialogTitle>
        </DialogHeader>
        <form className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Nome</Label>
            <Input id="name" defaultValue={data.name} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" defaultValue={data.email} />
          </div>
          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancelar
            </Button>
            <Button type="submit">Salvar</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

## Tabelas

### Tabela de Dados

```tsx
import { DataTable } from '@/components/ui/data-table';

function UsersTable({ users }) {
  const columns = [
    { key: 'name', header: 'Nome', align: 'left' as const },
    { key: 'email', header: 'Email', align: 'left' as const },
    { key: 'role', header: 'Função', align: 'center' as const },
    {
      key: 'actions',
      header: 'Ações',
      align: 'right' as const,
      render: (_, row) => (
        <Button size="sm" variant="ghost">
          Editar
        </Button>
      ),
    },
  ];

  return (
    <DataTable
      title="Usuários"
      columns={columns}
      data={users}
      variant="striped"
      size="md"
    />
  );
}
```

## Dropdowns e Menus

### Menu de Ações

```tsx
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { MoreVertical } from 'lucide-react';

function ActionsMenu({ onEdit, onDelete }) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <MoreVertical className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={onEdit}>Editar</DropdownMenuItem>
        <DropdownMenuItem variant="destructive" onClick={onDelete}>
          Excluir
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

## Estados de Loading

### Loading com Skeleton

```tsx
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

function LoadingCard() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-6 w-32" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-4 w-full mb-2" />
        <Skeleton className="h-4 w-3/4" />
      </CardContent>
    </Card>
  );
}
```

### Loading com Spinner

```tsx
import { Spinner } from '@/components/ui/spinner';

function LoadingState() {
  return (
    <div className="flex items-center justify-center p-8">
      <Spinner size="lg" />
    </div>
  );
}
```

## Estados Vazios

```tsx
import { EmptyState } from '@/components/ui/empty-state';
import { Button } from '@/components/ui/button';

function EmptyList({ onAdd }) {
  return (
    <EmptyState
      title="Nenhum item encontrado"
      description="Comece adicionando um novo item"
      action={
        <Button onClick={onAdd}>Adicionar Item</Button>
      }
    />
  );
}
```

## Tooltips

```tsx
import { Tooltip } from '@/components/ui/tooltip';
import { Button } from '@/components/ui/button';

function TooltipExample() {
  return (
    <Tooltip content="Clique para salvar" position="top">
      <Button>Salvar</Button>
    </Tooltip>
  );
}
```

## Padrões Responsivos

### Layout Responsivo

```tsx
function ResponsiveLayout() {
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Conteúdo */}
      </div>
    </div>
  );
}
```

### Navegação Responsiva

```tsx
function ResponsiveNav() {
  return (
    <nav className="flex flex-col md:flex-row gap-4 p-4">
      <a href="/">Home</a>
      <a href="/about">Sobre</a>
      <a href="/contact">Contato</a>
    </nav>
  );
}
```

## Integração com Hooks

### Usando Design Tokens

```tsx
import { useColor, useSpacing } from '@/lib/hooks/use-design-token';

function ThemedComponent() {
  const primaryColor = useColor('primary', 600);
  const padding = useSpacing('md');

  return (
    <div style={{ backgroundColor: primaryColor, padding }}>
      Conteúdo
    </div>
  );
}
```

### Usando Breakpoints

```tsx
import { useBreakpoint } from '@/lib/hooks/use-breakpoint';

function ResponsiveComponent() {
  const isMobile = useBreakpoint('md', 'below');

  return (
    <div>
      {isMobile ? <MobileView /> : <DesktopView />}
    </div>
  );
}
```

---

**Mais exemplos**: Veja os componentes em `src/components/` para mais padrões de uso.
