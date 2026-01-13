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
      <Button variant="ghost" size="icon" className="lg:hidden" onClick={toggleSidebar}>
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
          {theme === 'light' ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
        </Button>

        {/* Keyboard Shortcuts */}
        <Button variant="ghost" size="icon" title="Atalhos (Ctrl+?)">
          <Keyboard className="h-5 w-5" />
        </Button>
      </div>
    </header>
  );
}
