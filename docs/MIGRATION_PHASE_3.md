# 🎨 Fase 3: Componentes Base e Design System

**Duração Estimada**: 5-7 dias  
**Complexidade**: Média  
**Dependências**: Fases 1 e 2 concluídas

---

## 🎯 Objetivos desta Fase

1. Criar componentes de UI base reutilizáveis
2. Implementar design system consistente
3. Desenvolver layouts principais (Sidebar, Header, Footer)
4. Criar componentes de navegação
5. Implementar componentes de formulário
6. Desenvolver componentes de feedback (Loading, Error, Empty State)
7. Criar componentes de exibição de dados (Cards, KPI, Tables)

---

## 📋 Checklist de Ações

### 1. Componentes de UI Base - Botões

- [x] **1.1** Criar componente Button em `src/components/ui/button.tsx`
  ```typescript
  // src/components/ui/button.tsx
  import * as React from 'react';
  import { cva, type VariantProps } from 'class-variance-authority';
  import { cn } from '@/lib/utils';

  const buttonVariants = cva(
    'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
    {
      variants: {
        variant: {
          default: 'bg-primary text-primary-foreground hover:bg-primary/90',
          destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
          outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
          secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
          ghost: 'hover:bg-accent hover:text-accent-foreground',
          link: 'underline-offset-4 hover:underline text-primary',
        },
        size: {
          default: 'h-10 py-2 px-4',
          sm: 'h-9 px-3 rounded-md',
          lg: 'h-11 px-8 rounded-md',
          icon: 'h-10 w-10',
        },
      },
      defaultVariants: {
        variant: 'default',
        size: 'default',
      },
    }
  );

  export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement>,
      VariantProps<typeof buttonVariants> {
    asChild?: boolean;
  }

  const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant, size, ...props }, ref) => {
      return (
        <button
          className={cn(buttonVariants({ variant, size, className }))}
          ref={ref}
          {...props}
        />
      );
    }
  );
  Button.displayName = 'Button';

  export { Button, buttonVariants };
  ```

- [x] **1.2** Criar teste para Button
  ```typescript
  // src/components/ui/__tests__/button.test.tsx
  import { render, screen } from '@testing-library/react';
  import { Button } from '../button';

  describe('Button', () => {
    it('renders button with text', () => {
      render(<Button>Click me</Button>);
      expect(screen.getByText('Click me')).toBeInTheDocument();
    });

    it('applies variant classes', () => {
      render(<Button variant="destructive">Delete</Button>);
      const button = screen.getByText('Delete');
      expect(button.className).toContain('destructive');
    });
  });
  ```

---

### 2. Componentes de UI Base - Inputs

- [x] **2.1** Criar componente Input
  ```typescript
  // src/components/ui/input.tsx
  import * as React from 'react';
  import { cn } from '@/lib/utils';

  export interface InputProps
    extends React.InputHTMLAttributes<HTMLInputElement> {}

  const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, type, ...props }, ref) => {
      return (
        <input
          type={type}
          className={cn(
            'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
            className
          )}
          ref={ref}
          {...props}
        />
      );
    }
  );
  Input.displayName = 'Input';

  export { Input };
  ```

- [x] **2.2** Criar componente Label
  ```typescript
  // src/components/ui/label.tsx
  import * as React from 'react';
  import { cn } from '@/lib/utils';

  export interface LabelProps
    extends React.LabelHTMLAttributes<HTMLLabelElement> {}

  const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
    ({ className, ...props }, ref) => {
      return (
        <label
          ref={ref}
          className={cn(
            'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
            className
          )}
          {...props}
        />
      );
    }
  );
  Label.displayName = 'Label';

  export { Label };
  ```

---

### 3. Componentes de UI Base - Card

- [x] **3.1** Criar componente Card
  ```typescript
  // src/components/ui/card.tsx
  import * as React from 'react';
  import { cn } from '@/lib/utils';

  const Card = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
  >(({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'rounded-lg border bg-card text-card-foreground shadow-sm',
        className
      )}
      {...props}
    />
  ));
  Card.displayName = 'Card';

  const CardHeader = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
  >(({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('flex flex-col space-y-1.5 p-6', className)}
      {...props}
    />
  ));
  CardHeader.displayName = 'CardHeader';

  const CardTitle = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLHeadingElement>
  >(({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn('text-2xl font-semibold leading-none tracking-tight', className)}
      {...props}
    />
  ));
  CardTitle.displayName = 'CardTitle';

  const CardDescription = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLParagraphElement>
  >(({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('text-sm text-muted-foreground', className)}
      {...props}
    />
  ));
  CardDescription.displayName = 'CardDescription';

  const CardContent = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
  >(({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
  ));
  CardContent.displayName = 'CardContent';

  const CardFooter = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
  >(({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('flex items-center p-6 pt-0', className)}
      {...props}
    />
  ));
  CardFooter.displayName = 'CardFooter';

  export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
  ```

---

### 4. Componentes de Feedback - Loading

- [x] **4.1** Criar componente Spinner
  ```typescript
  // src/components/ui/spinner.tsx
  import { cn } from '@/lib/utils';

  interface SpinnerProps {
    size?: 'sm' | 'md' | 'lg';
    className?: string;
  }

  const sizeClasses = {
    sm: 'h-4 w-4 border-2',
    md: 'h-8 w-8 border-3',
    lg: 'h-12 w-12 border-4',
  };

  export function Spinner({ size = 'md', className }: SpinnerProps) {
    return (
      <div
        className={cn(
          'animate-spin rounded-full border-primary border-t-transparent',
          sizeClasses[size],
          className
        )}
        role="status"
        aria-label="Carregando"
      >
        <span className="sr-only">Carregando...</span>
      </div>
    );
  }
  ```

- [ ] **4.2** Criar componente LoadingScreen
  ```typescript
  // src/components/ui/loading-screen.tsx
  import { Spinner } from './spinner';

  interface LoadingScreenProps {
    message?: string;
  }

  export function LoadingScreen({ message = 'Carregando...' }: LoadingScreenProps) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <Spinner size="lg" />
        <p className="mt-4 text-muted-foreground">{message}</p>
      </div>
    );
  }
  ```

- [x] **4.3** Criar componente Skeleton
  ```typescript
  // src/components/ui/skeleton.tsx
  import { cn } from '@/lib/utils';

  function Skeleton({
    className,
    ...props
  }: React.HTMLAttributes<HTMLDivElement>) {
    return (
      <div
        className={cn('animate-pulse rounded-md bg-muted', className)}
        {...props}
      />
    );
  }

  export { Skeleton };
  ```

---

### 5. Componentes de Feedback - Empty State

- [x] **5.1** Criar componente EmptyState
  ```typescript
  // src/components/ui/empty-state.tsx
  import { LucideIcon } from 'lucide-react';
  import { cn } from '@/lib/utils';

  interface EmptyStateProps {
    icon?: LucideIcon;
    title: string;
    description?: string;
    action?: React.ReactNode;
    className?: string;
  }

  export function EmptyState({
    icon: Icon,
    title,
    description,
    action,
    className,
  }: EmptyStateProps) {
    return (
      <div
        className={cn(
          'flex flex-col items-center justify-center py-12 text-center',
          className
        )}
      >
        {Icon && <Icon className="h-12 w-12 text-muted-foreground mb-4" />}
        <h3 className="text-lg font-semibold">{title}</h3>
        {description && (
          <p className="mt-2 text-sm text-muted-foreground max-w-md">
            {description}
          </p>
        )}
        {action && <div className="mt-6">{action}</div>}
      </div>
    );
  }
  ```

---

### 6. Layout - Sidebar

- [x] **6.1** Criar componente Sidebar
  ```typescript
  // src/components/layouts/sidebar.tsx
  'use client';

  import Link from 'next/link';
  import { usePathname } from 'next/navigation';
  import { Apple, LineChart, DollarSign, Package, Users, Truck, UserTie } from 'lucide-react';
  import { cn } from '@/lib/utils';
  import { useAppStore } from '@/store';

  const menuItems = [
    { id: 'geral', name: 'Visão Geral', icon: LineChart, href: '/geral' },
    { id: 'financas', name: 'Finanças', icon: DollarSign, href: '/financas' },
    { id: 'estoque', name: 'Estoque', icon: Package, href: '/estoque' },
    { id: 'publico-alvo', name: 'Público-Alvo', icon: Users, href: '/publico-alvo' },
    { id: 'fornecedores', name: 'Fornecedores', icon: Truck, href: '/fornecedores' },
    { id: 'recursos-humanos', name: 'Recursos Humanos', icon: UserTie, href: '/recursos-humanos' },
  ];

  export function Sidebar() {
    const pathname = usePathname();
    const sidebarOpen = useAppStore((state) => state.sidebarOpen);

    return (
      <aside
        className={cn(
          'fixed left-0 top-0 z-40 h-screen w-64 bg-card border-r transition-transform',
          !sidebarOpen && '-translate-x-full lg:translate-x-0'
        )}
      >
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center gap-2 border-b px-6">
            <Apple className="h-6 w-6 text-primary" />
            <span className="text-lg font-bold">Amazon Fruit</span>
          </div>

          {/* Menu */}
          <nav className="flex-1 space-y-1 px-3 py-4">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.id}
                  href={item.href}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="border-t p-4 text-xs text-muted-foreground">
            <p>&copy; 2026 Amazon Fruit</p>
            <p>v2.0.0</p>
          </div>
        </div>
      </aside>
    );
  }
  ```

---

### 7. Layout - Header

- [ ] **7.1** Criar componente Header
  ```typescript
  // src/components/layouts/header.tsx
  'use client';

  import { Bell, Moon, Sun, Search, Menu, Keyboard } from 'lucide-react';
  import { Button } from '@/components/ui/button';
  import { useAppStore } from '@/store';

  interface HeaderProps {
    title: string;
  }

  export function Header({ title }: HeaderProps) {
    const theme = useAppStore((state) => state.theme);
    const toggleTheme = useAppStore((state) => state.toggleTheme);
    const toggleSidebar = useAppStore((state) => state.toggleSidebar);
    const toggleAlerts = useAppStore((state) => state.toggleAlerts);
    const toggleSearch = useAppStore((state) => state.toggleSearch);

    return (
      <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b bg-background px-6">
        {/* Mobile Menu Toggle */}
        <Button
          variant="ghost"
          size="icon"
          className="lg:hidden"
          onClick={toggleSidebar}
        >
          <Menu className="h-5 w-5" />
        </Button>

        {/* Title */}
        <h1 className="text-xl font-semibold">{title}</h1>

        <div className="ml-auto flex items-center gap-2">
          {/* Search */}
          <Button variant="ghost" size="icon" onClick={toggleSearch} title="Busca (Ctrl+F)">
            <Search className="h-5 w-5" />
          </Button>

          {/* Alerts */}
          <Button variant="ghost" size="icon" onClick={toggleAlerts} title="Alertas">
            <Bell className="h-5 w-5" />
          </Button>

          {/* Theme Toggle */}
          <Button variant="ghost" size="icon" onClick={toggleTheme} title="Tema (Ctrl+T)">
            {theme === 'light' ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5" />
            )}
          </Button>

          {/* Keyboard Shortcuts */}
          <Button variant="ghost" size="icon" title="Atalhos (Ctrl+?)">
            <Keyboard className="h-5 w-5" />
          </Button>
        </div>
      </header>
    );
  }
  ```

---

### 8. Layout - Footer

- [x] **8.1** Criar componente Footer
  ```typescript
  // src/components/layouts/footer.tsx
  export function Footer() {
    return (
      <footer className="border-t py-4 px-6">
        <p className="text-center text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} Amazon Fruit - Sistema de Análise de Dados
        </p>
      </footer>
    );
  }
  ```

---

### 9. Layout - Main Layout

- [ ] **9.1** Criar componente MainLayout
  ```typescript
  // src/components/layouts/main-layout.tsx
  'use client';

  import { Sidebar } from './sidebar';
  import { Header } from './header';
  import { Footer } from './footer';
  import { useAppStore } from '@/store';
  import { cn } from '@/lib/utils';

  interface MainLayoutProps {
    children: React.ReactNode;
    title: string;
  }

  export function MainLayout({ children, title }: MainLayoutProps) {
    const sidebarOpen = useAppStore((state) => state.sidebarOpen);

    return (
      <div className="flex h-screen overflow-hidden">
        <Sidebar />

        <div
          className={cn(
            'flex flex-1 flex-col transition-all',
            sidebarOpen ? 'lg:ml-64' : 'ml-0'
          )}
        >
          <Header title={title} />

          <main className="flex-1 overflow-y-auto p-6">
            {children}
          </main>

          <Footer />
        </div>
      </div>
    );
  }
  ```

---

### 10. Componente KPI Card

- [x] **10.1** Criar componente KPICard
  ```typescript
  // src/components/dashboards/kpi-card.tsx
  import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
  import { cn } from '@/lib/utils';
  import { formatCurrency, formatNumber, formatPercentage } from '@/lib/utils';

  interface KPICardProps {
    title: string;
    value: number;
    change?: number;
    changeType?: 'increase' | 'decrease' | 'neutral';
    format?: 'currency' | 'number' | 'percentage';
    icon?: LucideIcon;
    className?: string;
  }

  export function KPICard({
    title,
    value,
    change,
    changeType = 'neutral',
    format = 'number',
    icon: Icon,
    className,
  }: KPICardProps) {
    const formattedValue =
      format === 'currency'
        ? formatCurrency(value)
        : format === 'percentage'
        ? formatPercentage(value)
        : formatNumber(value);

    const TrendIcon =
      changeType === 'increase'
        ? TrendingUp
        : changeType === 'decrease'
        ? TrendingDown
        : Minus;

    const trendColor =
      changeType === 'increase'
        ? 'text-green-600'
        : changeType === 'decrease'
        ? 'text-red-600'
        : 'text-muted-foreground';

    return (
      <Card className={className}>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
          {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{formattedValue}</div>
          {change !== undefined && (
            <div className={cn('flex items-center text-xs', trendColor)}>
              <TrendIcon className="mr-1 h-3 w-3" />
              <span>{formatPercentage(Math.abs(change))}</span>
            </div>
          )}
        </CardContent>
      </Card>
    );
  }
  ```

---

### 11. Componente de Período

- [x] **11.1** Criar componente PeriodSelector
  ```typescript
  // src/components/dashboards/period-selector.tsx
  'use client';

  import { useState } from 'react';
  import { Calendar } from 'lucide-react';
  import { Button } from '@/components/ui/button';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import { useAppStore } from '@/store';

  export function PeriodSelector() {
    const dateRange = useAppStore((state) => state.dateRange);
    const setDateRange = useAppStore((state) => state.setDateRange);

    const [startDate, setStartDate] = useState(dateRange.start);
    const [endDate, setEndDate] = useState(dateRange.end);

    const handleApply = () => {
      setDateRange(startDate, endDate);
    };

    const handleReset = () => {
      // Implementar lógica de reset
    };

    return (
      <div className="flex flex-wrap items-end gap-4 rounded-lg border bg-card p-4">
        <div className="flex-1 min-w-[200px]">
          <Label htmlFor="start-date">Data Inicial</Label>
          <Input
            id="start-date"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>

        <div className="flex-1 min-w-[200px]">
          <Label htmlFor="end-date">Data Final</Label>
          <Input
            id="end-date"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>

        <Button onClick={handleApply}>
          <Calendar className="mr-2 h-4 w-4" />
          Aplicar Período
        </Button>

        <Button variant="outline" onClick={handleReset}>
          Resetar
        </Button>
      </div>
    );
  }
  ```

---

### 12. Testes dos Componentes

- [x] **12.1** Criar testes para Card
- [ ] **12.2** Criar testes para KPICard
- [ ] **12.3** Criar testes para Sidebar
- [ ] **12.4** Criar testes para Header
- [ ] **12.5** Criar testes para PeriodSelector

---

### 13. Storybook (Opcional mas Recomendado)

- [ ] **13.1** Instalar Storybook
  ```bash
  npx storybook@latest init
  ```

- [ ] **13.2** Criar stories para componentes principais
  - Button.stories.tsx
  - Card.stories.tsx
  - KPICard.stories.tsx

---

### 14. Documentação de Componentes

- [ ] **14.1** Documentar cada componente com JSDoc
- [ ] **14.2** Criar README de componentes
- [ ] **14.3** Documentar props e variantes

---

### 15. Verificação

- [x] **15.1** Executar testes
  ```bash
  npm test
  ```

- [x] **15.2** Verificar linting
  ```bash
  npm run lint
  ```

- [x] **15.3** Verificar build
  ```bash
  npm run build
  ```

---

## ✅ Critérios de Conclusão da Fase 3

A Fase 3 está completa quando:

- [x] Todos os componentes de UI base criados
- [x] Layout principal funcional (Sidebar, Header, Footer)
- [x] Componentes de feedback implementados
- [x] Componente KPICard criado
- [x] PeriodSelector funcional
- [x] Design system consistente aplicado
- [x] Testes passando
- [x] Documentação atualizada

---

## 📝 Notas e Observações

### Próximos Passos

- Prosseguir para [Fase 4: Dashboards - Parte 1](./MIGRATION_PHASE_4.md)

---

**Status**: ⏳ Pendente  
**Responsável**: [Nome]  
**Data de Início**: [Data]  
**Data de Conclusão**: [Data]
