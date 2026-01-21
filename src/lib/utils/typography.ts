/**
 * Utilitários de Tipografia
 * Funções para trabalhar com tipografia do design system
 */

import { getTypography } from './design-tokens';
import type { FontSize, FontWeight } from '@/lib/design-tokens/types';

/**
 * Obtém classes Tailwind para tamanho de fonte
 * @param size - Tamanho da fonte
 * @returns Classes Tailwind
 */
export function getFontSizeClasses(size: FontSize): string {
  const sizeMap: Record<FontSize, string> = {
    xs: 'text-xs',
    sm: 'text-sm',
    base: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
    '2xl': 'text-2xl',
    '3xl': 'text-3xl',
    '4xl': 'text-4xl',
    '5xl': 'text-5xl',
    '6xl': 'text-6xl',
    '7xl': 'text-7xl',
    '8xl': 'text-8xl',
    '9xl': 'text-9xl',
  };
  return sizeMap[size] || sizeMap.base;
}

/**
 * Obtém classes Tailwind para peso da fonte
 * @param weight - Peso da fonte
 * @returns Classes Tailwind
 */
export function getFontWeightClasses(weight: FontWeight): string {
  const weightMap: Record<FontWeight, string> = {
    thin: 'font-thin',
    extralight: 'font-extralight',
    light: 'font-light',
    normal: 'font-normal',
    medium: 'font-medium',
    semibold: 'font-semibold',
    bold: 'font-bold',
    extrabold: 'font-extrabold',
    black: 'font-black',
  };
  return weightMap[weight] || weightMap.normal;
}

/**
 * Calcula line-height baseado em font-size
 * @param fontSize - Tamanho da fonte
 * @returns Line-height calculado
 */
export function calculateLineHeight(fontSize: FontSize): number {
  const fontSizeValue = getTypography('fontSize', fontSize);
  const numericValue = parseFloat(fontSizeValue.toString());
  
  // Line-height padrão: 1.5 para texto normal, 1.25 para títulos
  return numericValue >= 24 ? 1.25 : 1.5;
}

/**
 * Obtém classes Tailwind para truncar texto
 * @param lines - Número de linhas (1, 2, 3, etc)
 * @returns Classes Tailwind
 */
export function getTruncateClasses(lines: number = 1): string {
  if (lines === 1) {
    return 'truncate';
  }
  return `truncate-${lines}`;
}

/**
 * Obtém classes Tailwind para hierarquia tipográfica
 * @param level - Nível da hierarquia (h1-h6, body, small, caption)
 * @returns Classes Tailwind
 */
export function getTypeScaleClasses(
  level: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'body' | 'small' | 'caption'
): string {
  const levelMap = {
    h1: 'text-5xl font-bold leading-tight',
    h2: 'text-4xl font-bold leading-snug',
    h3: 'text-3xl font-semibold leading-snug',
    h4: 'text-2xl font-semibold leading-normal',
    h5: 'text-xl font-medium leading-normal',
    h6: 'text-lg font-medium leading-normal',
    body: 'text-base font-normal leading-relaxed',
    small: 'text-sm font-normal leading-normal',
    caption: 'text-xs font-normal leading-normal',
  };
  return levelMap[level] || levelMap.body;
}
