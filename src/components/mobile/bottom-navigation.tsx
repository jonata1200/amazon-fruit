/**
 * Componente Bottom Navigation - Navegação inferior para mobile
 * Acesso rápido aos dashboards principais
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LineChart, DollarSign, Package, Users } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useMobile } from '@/lib/hooks/useMobile';

const bottomNavItems = [
  { id: 'geral', name: 'Geral', icon: LineChart, href: '/geral' },
  { id: 'financas', name: 'Finanças', icon: DollarSign, href: '/financas' },
  { id: 'estoque', name: 'Estoque', icon: Package, href: '/estoque' },
  { id: 'publico-alvo', name: 'Público', icon: Users, href: '/publico-alvo' },
];

export function BottomNavigation() {
  const pathname = usePathname();
  const isMobile = useMobile();

  // Só mostrar em mobile
  if (!isMobile) return null;

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 lg:hidden">
      <div className="flex items-center justify-around h-16">
        {bottomNavItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.id}
              href={item.href}
              aria-current={isActive ? 'page' : undefined}
              className={cn(
                'flex flex-col items-center justify-center gap-1 flex-1 h-full min-h-[44px] transition-colors',
                isActive
                  ? 'text-primary'
                  : 'text-muted-foreground hover:text-foreground'
              )}
            >
              <Icon className={cn('h-5 w-5', isActive && 'scale-110')} aria-hidden="true" />
              <span className="text-xs font-medium">{item.name}</span>
              {isActive && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
