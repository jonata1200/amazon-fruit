/**
 * Helpers para Design Tokens
 * Funções type-safe para acessar design tokens
 */

import { tokens } from '@/lib/design-tokens';
import type {
  ColorName,
  ColorScale,
  SpacingKey,
  FontSize,
  FontWeight,
  ShadowKey,
  BorderRadius,
  TransitionDuration,
  Breakpoint,
} from '@/lib/design-tokens/types';

/**
 * Obtém uma cor do design system
 * @param name - Nome da cor (primary, secondary, success, etc)
 * @param scale - Escala da cor (50-950)
 * @returns Valor da cor em formato hex
 */
export function getColor(name: ColorName, scale: ColorScale = 600): string {
  const color = tokens.colors[name];
  if (!color) {
    if (process.env.NODE_ENV === 'development') {
      console.warn(`Color "${name}" not found in design tokens`);
    }
    return tokens.colors.primary[600];
  }
  return color[scale] || color[600] || '#000000';
}

/**
 * Obtém um valor de espaçamento do design system
 * @param key - Chave do espaçamento (xs, sm, md, lg, etc)
 * @returns Valor do espaçamento em rem
 */
export function getSpacing(key: SpacingKey): string {
  return tokens.spacing.semantic[key] || tokens.spacing[key] || '1rem';
}

/**
 * Obtém um valor tipográfico do design system
 * @param type - Tipo de valor tipográfico
 * @param key - Chave do valor
 * @returns Valor tipográfico
 */
export function getTypography(
  type: 'fontSize' | 'fontWeight' | 'lineHeight' | 'letterSpacing',
  key: FontSize | FontWeight | string
): string | number {
  switch (type) {
    case 'fontSize':
      return tokens.typography.fontSizes[key as FontSize] || tokens.typography.fontSizes.base;
    case 'fontWeight':
      return tokens.typography.fontWeights[key as FontWeight] || tokens.typography.fontWeights.normal;
    case 'lineHeight':
      return tokens.typography.lineHeights[key as keyof typeof tokens.typography.lineHeights] || tokens.typography.lineHeights.normal;
    case 'letterSpacing':
      return tokens.typography.letterSpacing[key as keyof typeof tokens.typography.letterSpacing] || tokens.typography.letterSpacing.normal;
    default:
      return '';
  }
}

/**
 * Obtém uma sombra do design system
 * @param key - Chave da sombra (sm, base, md, lg, xl, etc)
 * @returns Valor da sombra
 */
export function getShadow(key: ShadowKey): string {
  return tokens.shadows.light[key] || tokens.shadows.light.base;
}

/**
 * Obtém um border-radius do design system
 * @param key - Chave do border-radius (none, sm, base, md, lg, etc)
 * @returns Valor do border-radius
 */
export function getRadius(key: BorderRadius): string {
  return tokens.borderRadius[key] || tokens.borderRadius.base;
}

/**
 * Obtém uma transição do design system
 * @param type - Tipo de transição (duration, easing, delay)
 * @param key - Chave da transição
 * @returns Valor da transição
 */
export function getTransition(
  type: 'duration' | 'easing' | 'delay',
  key: TransitionDuration | string
): string {
  switch (type) {
    case 'duration':
      return tokens.transitions.duration[key as TransitionDuration] || tokens.transitions.duration.base;
    case 'easing':
      return tokens.transitions.easing[key as keyof typeof tokens.transitions.easing] || tokens.transitions.easing.inOut;
    case 'delay':
      return tokens.transitions.delay[key as keyof typeof tokens.transitions.delay] || tokens.transitions.delay.none;
    default:
      return '';
  }
}

/**
 * Obtém um breakpoint do design system
 * @param key - Chave do breakpoint (sm, md, lg, xl, 2xl)
 * @returns Valor do breakpoint em pixels
 */
export function getBreakpoint(key: Breakpoint): string {
  return tokens.breakpoints[key] || tokens.breakpoints.md;
}

/**
 * Obtém um z-index do design system
 * @param key - Chave do z-index
 * @returns Valor do z-index
 */
export function getZIndex(key: keyof typeof tokens.zIndex): number | string {
  return tokens.zIndex[key] ?? 0;
}
