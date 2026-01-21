/**
 * Design Tokens - Sistema de Sombras e Elevação
 * Sistema de elevação com sombras para modo claro e escuro
 */

// Sombras para modo claro
export const shadows = {
  none: 'none',
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
  base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
} as const;

// Sombras para modo escuro (mais sutis)
export const shadowsDark = {
  none: 'none',
  sm: '0 1px 2px 0 rgb(0 0 0 / 0.3)',
  base: '0 1px 3px 0 rgb(0 0 0 / 0.4), 0 1px 2px -1px rgb(0 0 0 / 0.4)',
  md: '0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4)',
  lg: '0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.4)',
  xl: '0 20px 25px -5px rgb(0 0 0 / 0.4), 0 8px 10px -6px rgb(0 0 0 / 0.4)',
  '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.5)',
  inner: 'inset 0 2px 4px 0 rgb(0 0 0 / 0.3)',
} as const;

// Níveis de elevação (0-5)
export const elevation = {
  0: shadows.none,
  1: shadows.sm,
  2: shadows.base,
  3: shadows.md,
  4: shadows.lg,
  5: shadows.xl,
} as const;

// Sombras específicas para componentes
export const componentShadows = {
  card: shadows.base,
  cardHover: shadows.md,
  modal: shadows['2xl'],
  dropdown: shadows.lg,
  tooltip: shadows.md,
  button: shadows.sm,
  buttonHover: shadows.base,
  input: shadows.inner,
  inputFocus: shadows.base,
} as const;
