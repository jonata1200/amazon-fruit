// src/components/features/keyboard/keyboard-shortcuts-help.tsx
'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function KeyboardShortcutsHelp() {
  const shortcuts = [
    { key: 'Ctrl + K', description: 'Abrir busca global' },
    { key: 'Ctrl + T', description: 'Alternar tema' },
    { key: 'ESC', description: 'Fechar painéis' },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Atalhos de Teclado</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {shortcuts.map((shortcut, index) => (
            <div key={index} className="flex justify-between items-center">
              <span className="text-muted-foreground">{shortcut.description}</span>
              <kbd className="rounded border px-2 py-1 text-sm font-mono bg-muted">
                {shortcut.key}
              </kbd>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
