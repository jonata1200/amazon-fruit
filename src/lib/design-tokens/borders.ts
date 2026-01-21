/**
 * Design Tokens - Bordas e Border Radius
 * Sistema de bordas e raios de borda
 */

export const borderRadius = {
  none: '0',
  sm: '0.125rem', // 2px
  base: '0.25rem', // 4px
  md: '0.375rem', // 6px
  lg: '0.5rem', // 8px
  xl: '0.75rem', // 12px
  '2xl': '1rem', // 16px
  '3xl': '1.5rem', // 24px
  full: '9999px',
} as const;

// Border radius para componentes específicos
export const componentRadius = {
  button: borderRadius.md,
  input: borderRadius.md,
  card: borderRadius.lg,
  modal: borderRadius.xl,
  tooltip: borderRadius.md,
  badge: borderRadius.full,
  avatar: borderRadius.full,
} as const;

// Larguras de borda
export const borderWidth = {
  0: '0',
  1: '1px',
  2: '2px',
  4: '4px',
  8: '8px',
} as const;

// Estilos de borda
export const borderStyle = {
  solid: 'solid',
  dashed: 'dashed',
  dotted: 'dotted',
  none: 'none',
} as const;
