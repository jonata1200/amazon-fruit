// src/components/layouts/sidebar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Apple, LineChart, DollarSign, Package, Users, Truck, UserSquare } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAppStore } from '@/store';

const menuItems = [
  { id: 'geral', name: 'Visão Geral', icon: LineChart, href: '/geral' },
  { id: 'financas', name: 'Finanças', icon: DollarSign, href: '/financas' },
  { id: 'estoque', name: 'Estoque', icon: Package, href: '/estoque' },
  {
    id: 'publico-alvo',
    name: 'Público-Alvo',
    icon: Users,
    href: '/publico-alvo',
  },
  {
    id: 'fornecedores',
    name: 'Fornecedores',
    icon: Truck,
    href: '/fornecedores',
  },
  {
    id: 'recursos-humanos',
    name: 'Recursos Humanos',
    icon: UserSquare,
    href: '/recursos-humanos',
  },
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
      </div>
    </aside>
  );
}
