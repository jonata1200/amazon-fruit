/**
 * Tailwind CSS - Utilitários Customizados
 * Funções helper para criar utilitários baseados em design tokens
 */

import type { tokens } from '@/lib/design-tokens';

/**
 * Helper para obter valor de espaçamento do design token
 */
export function getSpacingToken(key: keyof typeof tokens.spacing.semantic): string {
  // Esta função pode ser usada em JavaScript/TypeScript para acessar tokens
  // Em CSS/Tailwind, use as classes diretamente
  const spacingMap: Record<string, string> = {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem',
    '4xl': '6rem',
    '5xl': '8rem',
  };
  return spacingMap[key] || spacingMap.md;
}

/**
 * Helper para obter cor do design token
 */
export function getColorToken(
  colorName: keyof typeof tokens.colors,
  scale: keyof typeof tokens.colors.primary = '600'
): string {
  // Esta função pode ser usada em JavaScript/TypeScript
  // Em CSS/Tailwind, use as classes como text-primary-600, bg-success-500, etc.
  const colorMap: Record<string, Record<string, string>> = {
    primary: {
      50: '#faf5ff',
      100: '#f3e8ff',
      200: '#e9d5ff',
      300: '#d8b4fe',
      400: '#c084fc',
      500: '#a855f7',
      600: '#9333ea',
      700: '#7e22ce',
      800: '#6b21a8',
      900: '#581c87',
      950: '#3b0764',
    },
    // Adicione outras cores conforme necessário
  };
  return colorMap[colorName]?.[scale] || colorMap.primary[scale];
}

/**
 * Helper para criar classes de espaçamento consistentes
 */
export const spacingUtilities = {
  // Padding
  p: (size: keyof typeof tokens.spacing.semantic) => `p-${size === 'xs' ? '1' : size === 'sm' ? '2' : size === 'md' ? '4' : size === 'lg' ? '6' : '8'}`,
  px: (size: keyof typeof tokens.spacing.semantic) => `px-${size === 'xs' ? '1' : size === 'sm' ? '2' : size === 'md' ? '4' : size === 'lg' ? '6' : '8'}`,
  py: (size: keyof typeof tokens.spacing.semantic) => `py-${size === 'xs' ? '1' : size === 'sm' ? '2' : size === 'md' ? '4' : size === 'lg' ? '6' : '8'}`,
  // Margin
  m: (size: keyof typeof tokens.spacing.semantic) => `m-${size === 'xs' ? '1' : size === 'sm' ? '2' : size === 'md' ? '4' : size === 'lg' ? '6' : '8'}`,
  mx: (size: keyof typeof tokens.spacing.semantic) => `mx-${size === 'xs' ? '1' : size === 'sm' ? '2' : size === 'md' ? '4' : size === 'lg' ? '6' : '8'}`,
  my: (size: keyof typeof tokens.spacing.semantic) => `my-${size === 'xs' ? '1' : size === 'sm' ? '2' : size === 'md' ? '4' : size === 'lg' ? '6' : '8'}`,
  // Gap
  gap: (size: keyof typeof tokens.spacing.semantic) => `gap-${size === 'xs' ? '1' : size === 'sm' ? '2' : size === 'md' ? '4' : size === 'lg' ? '6' : '8'}`,
} as const;

/**
 * Helper para criar classes de tipografia consistentes
 */
export const typographyUtilities = {
  text: (size: 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl' | '6xl') => `text-${size}`,
  font: (weight: 'light' | 'normal' | 'medium' | 'semibold' | 'bold' | 'extrabold') => `font-${weight}`,
  leading: (height: 'none' | 'tight' | 'snug' | 'normal' | 'relaxed' | 'loose') => `leading-${height}`,
} as const;

/**
 * Helper para criar classes de elevação
 */
export const elevationUtilities = {
  shadow: (level: 0 | 1 | 2 | 3 | 4 | 5) => {
    const shadowMap = {
      0: 'shadow-none',
      1: 'shadow-sm',
      2: 'shadow',
      3: 'shadow-md',
      4: 'shadow-lg',
      5: 'shadow-xl',
    };
    return shadowMap[level];
  },
} as const;
