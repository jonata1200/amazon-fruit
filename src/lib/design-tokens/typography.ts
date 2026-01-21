/**
 * Design Tokens - Sistema de Tipografia
 * Fontes, tamanhos, pesos e espaçamentos tipográficos
 */

export const typography = {
  fontFamilies: {
    sans: ['var(--font-geist-sans)', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
    mono: ['var(--font-geist-mono)', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
    serif: ['Georgia', 'Times New Roman', 'serif'],
  },
  fontSizes: {
    xs: '0.75rem', // 12px
    sm: '0.875rem', // 14px
    base: '1rem', // 16px
    lg: '1.125rem', // 18px
    xl: '1.25rem', // 20px
    '2xl': '1.5rem', // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem', // 36px
    '5xl': '3rem', // 48px
    '6xl': '3.75rem', // 60px
    '7xl': '4.5rem', // 72px
    '8xl': '6rem', // 96px
    '9xl': '8rem', // 128px
  },
  fontWeights: {
    thin: 100,
    extralight: 200,
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
  lineHeights: {
    none: 1,
    tight: 1.25,
    snug: 1.375,
    normal: 1.5,
    relaxed: 1.625,
    loose: 2,
  },
  letterSpacing: {
    tighter: '-0.05em',
    tight: '-0.025em',
    normal: '0em',
    wide: '0.025em',
    wider: '0.05em',
    widest: '0.1em',
  },
} as const;

// Hierarquia tipográfica
export const typeScale = {
  // Display/Título principal
  display: {
    fontSize: typography.fontSizes['6xl'],
    lineHeight: typography.lineHeights.tight,
    fontWeight: typography.fontWeights.bold,
    letterSpacing: typography.letterSpacing.tight,
  },
  // H1
  h1: {
    fontSize: typography.fontSizes['5xl'],
    lineHeight: typography.lineHeights.tight,
    fontWeight: typography.fontWeights.bold,
    letterSpacing: typography.letterSpacing.tight,
  },
  // H2
  h2: {
    fontSize: typography.fontSizes['4xl'],
    lineHeight: typography.lineHeights.snug,
    fontWeight: typography.fontWeights.bold,
    letterSpacing: typography.letterSpacing.tight,
  },
  // H3
  h3: {
    fontSize: typography.fontSizes['3xl'],
    lineHeight: typography.lineHeights.snug,
    fontWeight: typography.fontWeights.semibold,
    letterSpacing: typography.letterSpacing.normal,
  },
  // H4
  h4: {
    fontSize: typography.fontSizes['2xl'],
    lineHeight: typography.lineHeights.normal,
    fontWeight: typography.fontWeights.semibold,
    letterSpacing: typography.letterSpacing.normal,
  },
  // H5
  h5: {
    fontSize: typography.fontSizes.xl,
    lineHeight: typography.lineHeights.normal,
    fontWeight: typography.fontWeights.medium,
    letterSpacing: typography.letterSpacing.normal,
  },
  // H6
  h6: {
    fontSize: typography.fontSizes.lg,
    lineHeight: typography.lineHeights.normal,
    fontWeight: typography.fontWeights.medium,
    letterSpacing: typography.letterSpacing.normal,
  },
  // Body text
  body: {
    fontSize: typography.fontSizes.base,
    lineHeight: typography.lineHeights.relaxed,
    fontWeight: typography.fontWeights.normal,
    letterSpacing: typography.letterSpacing.normal,
  },
  // Small text
  small: {
    fontSize: typography.fontSizes.sm,
    lineHeight: typography.lineHeights.normal,
    fontWeight: typography.fontWeights.normal,
    letterSpacing: typography.letterSpacing.normal,
  },
  // Caption
  caption: {
    fontSize: typography.fontSizes.xs,
    lineHeight: typography.lineHeights.normal,
    fontWeight: typography.fontWeights.normal,
    letterSpacing: typography.letterSpacing.wide,
  },
} as const;
