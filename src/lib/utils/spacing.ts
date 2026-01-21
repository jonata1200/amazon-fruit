/**
 * Utilitários de Espaçamento
 * Funções para trabalhar com espaçamento do design system
 */

import { getSpacing } from './design-tokens';
import type { SpacingKey } from '@/lib/design-tokens/types';

/**
 * Calcula espaçamento baseado em múltiplos
 * @param base - Espaçamento base (chave do token)
 * @param multiplier - Multiplicador
 * @returns Espaçamento calculado
 */
export function calculateSpacing(base: SpacingKey, multiplier: number): string {
  const baseValue = getSpacing(base);
  const numericValue = parseFloat(baseValue);
  const unit = baseValue.replace(numericValue.toString(), '');
  return `${numericValue * multiplier}${unit}`;
}

/**
 * Obtém classes Tailwind para padding
 * @param size - Tamanho do padding
 * @returns Classes Tailwind
 */
export function getPaddingClasses(size: SpacingKey): string {
  const sizeMap: Record<SpacingKey, string> = {
    xs: 'p-1',
    sm: 'p-2',
    md: 'p-4',
    lg: 'p-6',
    xl: 'p-8',
    '2xl': 'p-12',
    '3xl': 'p-16',
    '4xl': 'p-24',
    '5xl': 'p-32',
  };
  return sizeMap[size] || sizeMap.md;
}

/**
 * Obtém classes Tailwind para margin
 * @param size - Tamanho do margin
 * @returns Classes Tailwind
 */
export function getMarginClasses(size: SpacingKey): string {
  const sizeMap: Record<SpacingKey, string> = {
    xs: 'm-1',
    sm: 'm-2',
    md: 'm-4',
    lg: 'm-6',
    xl: 'm-8',
    '2xl': 'm-12',
    '3xl': 'm-16',
    '4xl': 'm-24',
    '5xl': 'm-32',
  };
  return sizeMap[size] || sizeMap.md;
}

/**
 * Obtém classes Tailwind para gap
 * @param size - Tamanho do gap
 * @returns Classes Tailwind
 */
export function getGapClasses(size: SpacingKey): string {
  const sizeMap: Record<SpacingKey, string> = {
    xs: 'gap-1',
    sm: 'gap-2',
    md: 'gap-4',
    lg: 'gap-6',
    xl: 'gap-8',
    '2xl': 'gap-12',
    '3xl': 'gap-16',
    '4xl': 'gap-24',
    '5xl': 'gap-32',
  };
  return sizeMap[size] || sizeMap.md;
}

/**
 * Cria espaçamento responsivo
 * @param mobile - Espaçamento para mobile
 * @param desktop - Espaçamento para desktop
 * @returns Classes Tailwind responsivas
 */
export function getResponsiveSpacing(mobile: SpacingKey, desktop: SpacingKey): string {
  const mobileClass = getPaddingClasses(mobile);
  const desktopClass = getPaddingClasses(desktop);
  return `${mobileClass} md:${desktopClass.replace('p-', 'md:p-')}`;
}
