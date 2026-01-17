// src/components/layouts/sidebar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Apple, LineChart, DollarSign, Package, Users, Truck, UserSquare, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAppStore } from '@/store';
import { useFavorites, type DashboardId } from '@/lib/hooks/useFavorites';

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
  const { favorites, toggleFavorite, isFavorite } = useFavorites();

  // Separar itens favoritos dos demais
  const favoriteItems = menuItems.filter((item) => favorites.includes(item.id as DashboardId));
  const regularItems = menuItems.filter((item) => !favorites.includes(item.id as DashboardId));

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
        <nav className="flex-1 space-y-1 px-3 py-4 overflow-y-auto">
          {/* Favoritos */}
          {favoriteItems.length > 0 && (
            <div className="mb-4">
              <h3 className="px-3 mb-2 text-xs font-semibold text-muted-foreground uppercase">Favoritos</h3>
              {favoriteItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;

                return (
                  <div key={item.id} className="group relative">
                    <Link
                      href={item.href}
                      aria-current={isActive ? 'page' : undefined}
                      className={cn(
                        'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                        isActive
                          ? 'bg-primary text-primary-foreground'
                          : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                      )}
                    >
                      <Icon className="h-5 w-5" aria-hidden="true" />
                      <span>{item.name}</span>
                    </Link>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        toggleFavorite(item.id as DashboardId);
                      }}
                      className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-accent transition-opacity"
                      aria-label="Remover dos favoritos"
                    >
                      <Star className="h-4 w-4 fill-yellow-500 text-yellow-500" />
                    </button>
                  </div>
                );
              })}
            </div>
          )}

          {/* Itens regulares */}
          <div className={favoriteItems.length > 0 ? 'border-t pt-4' : ''}>
            {regularItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <div key={item.id} className="group relative">
                  <Link
                    href={item.href}
                    aria-current={isActive ? 'page' : undefined}
                    className={cn(
                      'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                    )}
                  >
                    <Icon className="h-5 w-5" aria-hidden="true" />
                    <span>{item.name}</span>
                  </Link>
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      toggleFavorite(item.id as DashboardId);
                    }}
                    className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-accent transition-opacity"
                    aria-label="Adicionar aos favoritos"
                  >
                    <Star className="h-4 w-4 text-muted-foreground hover:text-yellow-500" />
                  </button>
                </div>
              );
            })}
          </div>
        </nav>
      </div>
    </aside>
  );
}
