/**
 * Design Tokens - Breakpoints e Responsividade
 * Breakpoints alinhados com Tailwind CSS
 */

export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
} as const;

// Container widths para cada breakpoint
export const containerWidths = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
  full: '100%',
} as const;

// Media queries helpers (para uso em JavaScript/TypeScript)
export const mediaQueries = {
  sm: `(min-width: ${breakpoints.sm})`,
  md: `(min-width: ${breakpoints.md})`,
  lg: `(min-width: ${breakpoints.lg})`,
  xl: `(min-width: ${breakpoints.xl})`,
  '2xl': `(min-width: ${breakpoints['2xl']})`,
  // Max width queries
  maxSm: `(max-width: 639px)`,
  maxMd: `(max-width: 767px)`,
  maxLg: `(max-width: 1023px)`,
  maxXl: `(max-width: 1279px)`,
} as const;
