/**
 * Hook useColorMode - Hook para gerenciar modo de cor (dark/light)
 * Hook React para trabalhar com dark mode
 */

'use client';

import { useAppStore } from '@/store';

/**
 * Hook para acessar e controlar o modo de cor
 * @returns Objeto com theme, setTheme e toggleTheme
 */
export function useColorMode() {
  const theme = useAppStore((state) => state.theme);
  const setTheme = useAppStore((state) => state.setTheme);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const isDark = theme === 'dark';
  const isLight = theme === 'light';

  return {
    theme,
    setTheme,
    toggleTheme,
    isDark,
    isLight,
  };
}
