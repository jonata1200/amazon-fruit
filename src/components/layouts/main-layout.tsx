// src/components/layouts/main-layout.tsx
'use client';

import { Sidebar } from './sidebar';
import { Header } from './header';
import { Footer } from './footer';
import { useAppStore } from '@/store';
import { cn } from '@/lib/utils';
import { AlertsPanel } from '@/components/features/alerts/alerts-panel';
import { GlobalSearch } from '@/components/features/search/global-search';
import { useKeyboardShortcuts } from '@/lib/hooks/useKeyboardShortcuts';
import { BottomNavigation } from '@/components/mobile/bottom-navigation';
import { useMobile } from '@/lib/hooks/useMobile';

interface MainLayoutProps {
  children: React.ReactNode;
  title: string;
}

export function MainLayout({ children, title }: MainLayoutProps) {
  const sidebarOpen = useAppStore((state) => state.sidebarOpen);
  const isMobile = useMobile();

  // Atalhos de teclado globais
  useKeyboardShortcuts();

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />

      <div className={cn('flex flex-1 flex-col transition-all', sidebarOpen ? 'lg:ml-64' : 'ml-0')}>
        <Header title={title} />

        <main 
          id="main-content" 
          className={cn(
            'flex-1 overflow-y-auto p-4 sm:p-6',
            isMobile && 'pb-20' // Espaço para bottom navigation
          )}
        >
          {children}
        </main>

        <Footer />
      </div>

      {/* Painéis Globais */}
      <AlertsPanel />
      <GlobalSearch />
      
      {/* Bottom Navigation (apenas mobile) */}
      <BottomNavigation />
    </div>
  );
}
