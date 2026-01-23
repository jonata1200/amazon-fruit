// src/components/ui/toaster.tsx
'use client';

import { Toaster as Sonner } from 'sonner';
import { useAppStore } from '@/store';

export function Toaster() {
  const theme = useAppStore((state) => state.theme);

  return (
    <Sonner
      theme={theme}
      position="top-center"
      richColors
      aria-live="polite"
      className="sm:top-right"
      toastOptions={{
        classNames: {
          error: 'bg-destructive text-destructive-foreground',
          success: 'bg-green-600 text-white',
          warning: 'bg-yellow-600 text-white',
          info: 'bg-blue-600 text-white',
        },
      }}
    />
  );
}
